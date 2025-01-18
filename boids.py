import pygame
import random
import math

# Constants
WIDTH, HEIGHT = 800, 600  # Screen dimensions
NUM_BOIDS = 50           # Number of boids
MAX_SPEED = 4.0          # Maximum speed of boids
VIEW_RADIUS = 50         # Radius within which boids interact
FOV_ANGLE = 270          # Field of view in degrees (-1 for 360 degrees)
WIND_FORCE = pygame.Vector2(0.1, 0.05)  # Wind force vector

# Boid class
class Boid:
    def __init__(self, x, y):
        self.position = pygame.Vector2(x, y)
        self.velocity = pygame.Vector2(random.uniform(-1, 1), random.uniform(-1, 1)).normalize() * MAX_SPEED

    def edges(self):
        """Wrap around screen edges."""
        if self.position.x > WIDTH:
            self.position.x = 0
        elif self.position.x < 0:
            self.position.x = WIDTH
        if self.position.y > HEIGHT:
            self.position.y = 0
        elif self.position.y < 0:
            self.position.y = HEIGHT

    def move(self):
        """Move the boid based on its velocity."""
        self.position += self.velocity

    def draw(self, screen):
        """Draw the boid as a triangle pointing in its direction of movement."""
        angle = math.atan2(self.velocity.y, self.velocity.x)
        tip = self.position + self.velocity.normalize() * 10
        left = self.position + pygame.Vector2(math.cos(angle + math.pi * 2 / 3), math.sin(angle + math.pi * 2 / 3)) * 6
        right = self.position + pygame.Vector2(math.cos(angle - math.pi * 2 / 3), math.sin(angle - math.pi * 2 / 3)) * 6
        pygame.draw.polygon(screen, (255, 255, 255), [tip, left, right])

# Utility functions
def distance(b1, b2):
    """Compute Euclidean distance between two boids."""
    return b1.position.distance_to(b2.position)

def within_fov(b1, b2):
    """Check if b2 is within the field of view of b1."""
    if FOV_ANGLE == -1:  # 360 degrees
        return True
    direction = b1.velocity.angle_to(b2.position - b1.position)
    return abs(direction) <= FOV_ANGLE / 2

def update_boids(boids):
    """Update the position and velocity of each boid based on the three rules."""
    for boid in boids:
        # Collect neighbors within the view radius
        neighbors = [b for b in boids if b != boid and distance(boid, b) < VIEW_RADIUS and within_fov(boid, b)]

        if neighbors:
            # Rule 1: Collision Avoidance
            avoid_vector = pygame.Vector2(0, 0)
            for neighbor in neighbors:
                if distance(boid, neighbor) < VIEW_RADIUS / 2:  # Tighter radius for avoidance
                    avoid_vector -= (neighbor.position - boid.position)

            # Rule 2: Velocity Matching
            match_velocity = pygame.Vector2(0, 0)
            for neighbor in neighbors:
                match_velocity += neighbor.velocity
            match_velocity /= len(neighbors)

            # Rule 3: Flock Centering
            center_of_mass = pygame.Vector2(0, 0)
            for neighbor in neighbors:
                center_of_mass += neighbor.position
            center_of_mass /= len(neighbors)
            cohesion_vector = (center_of_mass - boid.position) * 0.01

            # Combine forces with weights
            boid.velocity += avoid_vector * 0.05 + match_velocity * 0.05 + cohesion_vector

        # Apply wind force
        boid.velocity += WIND_FORCE

        # Limit speed
        if boid.velocity.length() > MAX_SPEED:
            boid.velocity.scale_to_length(MAX_SPEED)

        # Move boid
        boid.move()
        boid.edges()

# Main program
def main():
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    clock = pygame.time.Clock()

    # Create boids
    boids = [Boid(random.randint(0, WIDTH), random.randint(0, HEIGHT)) for _ in range(NUM_BOIDS)]

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # Update boids
        update_boids(boids)

        # Draw everything
        screen.fill((0, 0, 0))
        for boid in boids:
            boid.draw(screen)
        pygame.display.flip()

        clock.tick(60)

    pygame.quit()

if __name__ == "__main__":
    main()
