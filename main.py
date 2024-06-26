import pygame
import math
import random

pygame.init()
WIDTH = 1100
HEIGHT = 600

clock = pygame.time.Clock()
frame_rate_per_second = 60

pygame.display.set_caption("Dino Game")
screen = pygame.display.set_mode((WIDTH, HEIGHT))

background = pygame.image.load("Track.png")

DinoRun1 = pygame.image.load("DinoRun1.png")
DinoRun2 = pygame.image.load("DinoRun2.png")
DinoDuck1 = pygame.image.load("DinoDuck1.png")
DinoJump = pygame.image.load("DinoJump.png")
LargeCactus1 = pygame.image.load("LargeCactus1.png").convert_alpha()
LargeCactus2 = pygame.image.load("LargeCactus2.png").convert_alpha()
LargeCactus3 = pygame.image.load("LargeCactus3.png").convert_alpha()
Bird1 = pygame.image.load("Bird1.png")
Bird2 = pygame.image.load("Bird2.png")

bird_images = [Bird1, Bird2]
birds = []

ground_y = 478  # Y position of the ground

cactus_images = [LargeCactus1, LargeCactus2, LargeCactus3]
cactus_positions = []

cloud_images = [pygame.image.load("Cloud.png"), pygame.image.load("Cloud.png")]
clouds = []

class Cloud:
    def __init__(self):
        self.x = WIDTH + random.randint(800, 1000)
        self.y = random.randint(50, 100)
        self.image = random.choice(cloud_images)
        self.width = self.image.get_width()

    def update(self):
        self.x -= game_speed
        if self.x < -self.width:
            self.x = WIDTH + random.randint(2500, 3000)
            self.y = random.randint(50, 100)
            self.image = random.choice(cloud_images)

    def draw(self, screen):
        screen.blit(self.image, (self.x, self.y))


def generate_clouds():
    global clouds
    for i in range(3):  # Generate 3 initial clouds
        cloud = Cloud()
        clouds.append(cloud)


generate_clouds()


class Cactus:
    def __init__(self, x):
        self.x = x
        self.image = random.choice(cactus_images)
        self.width = self.image.get_width()
        self.height = self.image.get_height()
        self.y = ground_y  # Ensure cactus is placed on the ground

    def update(self):
        self.x -= game_speed

    def draw(self, screen):
        screen.blit(self.image, (self.x, self.y))


class Bird:
    def __init__(self):
        self.x = WIDTH + random.randint(1000, 1500)
        self.y = random.randint(370, 445)
        self.images = bird_images
        self.frame = 0
        self.image = self.images[self.frame]

    def update(self):
        self.x -= game_speed
        self.frame = (self.frame + 1) % 20  # Change frame every 10 ticks
        self.image = self.images[self.frame // 10]
        if self.x < -self.image.get_width():
            self.x = WIDTH + random.randint(1000, 1500)
            self.y = random.randint(370, 445)
            birds.remove(self)  # Remove the bird from the list when off screen

    def draw(self, screen):
        screen.blit(self.image, (self.x, self.y))



def generate_cacti_and_birds():
    global cactus_positions, birds
    num_cacti = random.randint(1, 2)  # Generate 1 to 2 cacti
    cactus_positions = []
    birds = []

    for _ in range(num_cacti):
        x = WIDTH + random.randint(100, 400)  # Random x position off screen
        cactus = Cactus(x)
        cactus_positions.append(cactus)

    for _ in range(2):  # Generate 2 initial birds
        x = WIDTH + random.randint(1000, 1500)
        bird = Bird()
        bird.x = x

        # Ensure bird is not too close to any cactus
        while any(abs(bird.x - cactus.x) < 300 for cactus in cactus_positions):
            bird.x = WIDTH + random.randint(1000, 1500)

        birds.append(bird)


generate_cacti_and_birds()

scroll = 0
bg_width = background.get_width()
tiles = math.ceil(WIDTH / bg_width) + 1

frame_count = 0
dino_images = [DinoRun1, DinoRun2]

is_ducking = False
is_jumping = False
jump_velocity = 0
jump_height = 20
gravity = 1
dino_y = 478  # Initial y position of the dino

# Initialize start time
start_time = pygame.time.get_ticks()

def display_score(elapsed_time):
    font = pygame.font.Font(None, 36)
    score_text = font.render(f"Survival seconds: {elapsed_time}", True, (255, 0, 0))
    screen.blit(score_text, (WIDTH - 250, 50))

def display_game_over():
    font = pygame.font.Font(None, 32)
    game_over_text = font.render(f"Click SPACE button to restart. You survived {elapsed_time} seconds", True, (255, 0, 0))
    GameOver = pygame.image.load("GameOver.png")
    text_rect = game_over_text.get_rect(center=(WIDTH // 2, HEIGHT // 2))
    text_rect2 = game_over_text.get_rect(center=(WIDTH // 2, HEIGHT // 2 - 100))
    screen.blit(game_over_text, text_rect)
    screen.blit(GameOver, text_rect2)

run = True
game_speed = 14
game_over = False

while run:
    clock.tick(frame_rate_per_second)

    # Clear the screen
    screen.fill((0, 0, 0))

    # Draw the background
    for i in range(0, tiles):
        screen.blit(background, (i * bg_width + scroll, 562))

    # Update the scroll position
    scroll -= 5
    if abs(scroll) > bg_width:
        scroll = 0

    if not game_over:
        # Calculate elapsed time in seconds
        elapsed_time = (pygame.time.get_ticks() - start_time) // 1000

        # Handle jumping mechanics
        if is_jumping:
            dino_y -= jump_velocity
            jump_velocity -= gravity
            if dino_y >= ground_y:
                dino_y = ground_y
                is_jumping = False
                jump_velocity = jump_height

        # Select the current dino image based on the frame count and ducking/jumping status
        if is_ducking:
            current_dino_image = DinoDuck1
            dino_y = 510
        elif is_jumping:
            current_dino_image = DinoJump
        else:
            current_dino_image = dino_images[frame_count // 10 % 2]

        # Draw the current dino image
        screen.blit(current_dino_image, (15, dino_y))

        # Reset dino_y after ducking
        if not is_ducking and not is_jumping:
            dino_y = ground_y

        # Increment the frame count
        frame_count += 1

        # Draw clouds, cacti, and birds
        for cloud in clouds:
            cloud.draw(screen)
            cloud.update()

        for cactus in cactus_positions:
            cactus.update()
            cactus.draw(screen)
            if pygame.Rect(cactus.x, cactus.y, cactus.width, cactus.height).colliderect(
                    pygame.Rect(15, dino_y, current_dino_image.get_width(), current_dino_image.get_height())):
                game_over = True
            # If cactus moves off the screen, remove it
            if cactus.x < -cactus.width:
                cactus_positions.remove(cactus)

        for bird in birds:
            bird.update()
            bird.draw(screen)
            if pygame.Rect(bird.x, bird.y, bird.image.get_width(), bird.image.get_height()).colliderect(
                    pygame.Rect(15, dino_y, current_dino_image.get_width(), current_dino_image.get_height())):
                game_over = True
            # If bird moves off the screen, remove it
            if bird.x < -bird.image.get_width():
                birds.remove(bird)

        # Generate new cacti and birds if necessary
        if len(cactus_positions) == 0 and len(birds) == 0:
            generate_cacti_and_birds()

        # Display the score
        display_score(elapsed_time)

    else:
        display_game_over()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_DOWN and not game_over:
                is_ducking = True
            elif event.key == pygame.K_UP and not is_jumping and not game_over:
                is_jumping = True
                jump_velocity = jump_height
            elif event.key == pygame.K_SPACE and game_over:  # Restart the game with spacebar
                game_over = False
                generate_cacti_and_birds()  # Regenerate cacti and birds
                frame_count = 0  # Reset frame count
                dino_y = ground_y  # Reset dino position
                start_time = pygame.time.get_ticks()  # Reset start time
        elif event.type == pygame.KEYUP:
            if event.key == pygame.K_DOWN and not game_over:
                is_ducking = False

    pygame.display.update()

pygame.quit()
