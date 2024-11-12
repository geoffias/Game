import pygame
from pygame.locals import *
from os.path import join
from pygame import mixer
import pytmx

# Initialize Pygame and mixer
pygame.mixer.pre_init(44100, -16, 2, 512)
mixer.init()
pygame.init()

# Initialize variables
clock = pygame.time.Clock()
fps = 60

screen_width = 1152  # Game screen width
screen_height = 640  # Game screen height

# Set up the display
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption('Platformer')

# Define fonts
font = pygame.font.SysFont('Bauhaus 93', 70)
font_score = pygame.font.SysFont('Bauhaus 93', 30)
font_menu = pygame.font.SysFont('Bauhaus 93', 50)  # Define the menu font

# Game variables
tile_size = 64  # Size of each tile
game_over = 0
main_menu = True
score = 0
score_incrementing = False  # To manage score increment

# Define colors
white = (255, 255, 255)
black = (0, 0, 0)

# Player class
class Player:
    def __init__(self, x, y):
        self.reset(x, y)
        self.speed = 300  # Horizontal speed in pixels per second

    def update(self, delta_time):
        dx = 0
        dy = 0

        # Get key presses
        key = pygame.key.get_pressed()
        if key[pygame.K_SPACE] and not self.jumped and not self.in_air:
            self.vel_y = -15  # Jump velocity
            self.jumped = True
            self.in_air = True  # Set in air on jump

        if key[pygame.K_LEFT]:
            dx -= self.speed * delta_time  # Move left
        if key[pygame.K_RIGHT]:
            dx += self.speed * delta_time  # Move right

        # Add gravity
        self.vel_y += 1
        dy += self.vel_y

        # Update player coordinates
        self.rect.x += dx
        self.rect.y += dy

        # Reset if the player hits the ground
        if self.rect.y >= screen_height - self.rect.height:
            self.rect.y = screen_height - self.rect.height
            self.vel_y = 0
            self.in_air = False
            self.jumped = False  # Reset jumped status when hitting the ground

        # Draw player
        screen.blit(self.image, self.rect)

    def reset(self, x, y):
        try:
            self.image = pygame.image.load('ASSETS\SPRITES\Owlet_Monster.png')
            self.image = pygame.transform.scale(self.image, (32, 32))  # Scale to the desired size
            self.rect = self.image.get_rect()
            self.rect.x = x
            self.rect.y = y
            self.vel_y = 0
            self.jumped = False
            self.in_air = False
        except pygame.error as e:
            print(f"Failed to load image: {e}")

# World class
class World:
    def __init__(self, tmx_file):
        tmx_data = pytmx.load_pygame(tmx_file)
        self.tile_list = []
        
        # Load the tiles from the TMX file
        for layer in tmx_data.visible_layers:
            for x, y, gid in layer:
                if gid != 0:  # Check for non-empty tiles
                    tile = tmx_data.get_tile_image_by_gid(gid)
                    if tile:  # Ensure tile is valid
                        img_rect = tile.get_rect()
                        img_rect.x = x * tile_size  # Use tile_size here
                        img_rect.y = y * tile_size  # Use tile_size here
                        self.tile_list.append((tile, img_rect))

    def draw(self):
        for tile, rect in self.tile_list:
            screen.blit(tile, rect)

# Main game loop
player = Player(100, screen_height - 130)
world = World(join('TMX FILES', 'LEVEL2GAME!.tmx'))  # Adjust the path to your TMX file

run = True
while run:
    delta_time = clock.tick(fps) / 1000.0  # Calculate delta time
    for event in pygame.event.get():
        if event.type == QUIT:
            run = False

    screen.fill(black)  # Clear the screen
    world.draw()        # Draw the world
    player.update(delta_time )  # Update player with delta time
    pygame.display.update()  # Update the display

pygame.quit()