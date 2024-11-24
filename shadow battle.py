import pygame
import sys

# Initialize Pygame
pygame.init()

# Screen dimensions
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

# Create the game window
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Shadow Battle")

# Set frame rate
clock = pygame.time.Clock()
FPS = 60

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# Load resources (images)
background_image = pygame.image.load("images/bg.png")
background_image = pygame.transform.scale(background_image, (SCREEN_WIDTH, SCREEN_HEIGHT))

# Player class
class Player:
    def __init__(self, x, y):
        self.image = pygame.image.load("images/player.png")  # Load the player sprite
        self.image = pygame.transform.scale(self.image, (50, 50))  # Resize if needed
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)
        self.speed = 5
        self.health = 100

    def move(self, keys):
        if keys[pygame.K_LEFT]:
            self.rect.x -= self.speed
        if keys[pygame.K_RIGHT]:
            self.rect.x += self.speed
        if keys[pygame.K_UP]:
            self.rect.y -= self.speed
        if keys[pygame.K_DOWN]:
            self.rect.y += self.speed

    def draw(self, surface):
        surface.blit(self.image, self.rect)

# Enemy class
class Enemy:
    def __init__(self, x, y):
        self.image = pygame.image.load("images/enemy.png")  # Load enemy sprite
        self.image = pygame.transform.scale(self.image, (50, 50))  # Resize if needed
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)
        self.speed = 2
        self.health = 100

    def move_towards_player(self, player):
        if self.rect.x < player.rect.x:
            self.rect.x += self.speed
        if self.rect.x > player.rect.x:
            self.rect.x -= self.speed
        if self.rect.y < player.rect.y:
            self.rect.y += self.speed
        if self.rect.y > player.rect.y:
            self.rect.y -= self.speed

    def draw(self, surface):
        surface.blit(self.image, self.rect)

# Attack class
class Attack:
    def __init__(self, x, y):
        self.image = pygame.image.load("images/attack.png")  # Load attack sprite
        self.image = pygame.transform.scale(self.image, (20, 10))  # Resize if needed
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)
        self.speed = 10

    def move(self):
        self.rect.x += self.speed

    def draw(self, surface):
        surface.blit(self.image, self.rect)

# Main game loop
def main():
    player = Player(100, 300)
    enemy = Enemy(600, 300)
    attacks = []  # List to store active attacks

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            # Player attack
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    attacks.append(Attack(player.rect.right, player.rect.centery))

        # Get key presses
        keys = pygame.key.get_pressed()
        player.move(keys)

        # Enemy logic
        enemy.move_towards_player(player)

        # Move and draw attacks
        for attack in attacks[:]:
            attack.move()
            if attack.rect.colliderect(enemy.rect):  # Check collision with enemy
                enemy.health -= 10
                attacks.remove(attack)  # Remove attack after collision
            elif attack.rect.x > SCREEN_WIDTH:  # Remove if off-screen
                attacks.remove(attack)

        # Draw everything
        screen.blit(background_image, (0, 0))  # Draw the background
        player.draw(screen)
        enemy.draw(screen)
        for attack in attacks:
            attack.draw(screen)

        # Update the display
        pygame.display.flip()
        clock.tick(FPS)

    pygame.quit()
    sys.exit()

main()