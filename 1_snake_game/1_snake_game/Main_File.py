import pygame
import sys
import random
import subprocess
import psutil

# Initialize pygame
pygame.init()

# Constants
WIDTH, HEIGHT = 800, 600
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
BLACK = (0, 0, 0)
BUTTON_COLOR = (50, 150, 250)
BUTTON_HOVER = (30, 100, 200)
SNAKE_COLOR = (0, 200, 0) 
APPLE_COLOR = (200, 0, 0)

# Create window
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Snake Game")

# Load background image
background = pygame.image.load("background_original.jpg")  # Ensure you have a background image

# Font
font = pygame.font.Font(None, 40)

# Button function
def draw_button(text, x, y, w, h, action=None):
    mouse = pygame.mouse.get_pos()
    click = pygame.mouse.get_pressed()
    color = BUTTON_HOVER if x < mouse[0] < x + w and y < mouse[1] < y + h else BUTTON_COLOR
    pygame.draw.rect(screen, color, (x, y, w, h))
    
    text_surface = font.render(text, True, WHITE)
    text_rect = text_surface.get_rect(center=(x + w // 2, y + h // 2))
    screen.blit(text_surface, text_rect)
    
    if click[0] == 1 and action:
        pygame.time.delay(1)  # Avoid multiple clicks
        action()
        # Function to check if test.py is already running
def is_game_running():
    for process in psutil.process_iter(attrs=["pid", "name", "cmdline"]):
        cmdline = process.info.get("cmdline", [])
        if cmdline and "test.py" in cmdline:
            return True  # Game is already running
    return False  # Game is not running

# Open the game only if it's not already running
def start_game():
    if not is_game_running():  # Check if test.py is already running
        subprocess.Popen(["python", "test.py"])  # Start test.py (your game file)

# Main Menu function
def main_menu():
    running = True
    while running:
        screen.fill((0, 0, 0))

        draw_button("Start Game", WIDTH // 3, HEIGHT // 3, 200, 50, start_game)
        draw_button("Instruction", WIDTH // 3, HEIGHT // 3, 200, 50, open_instructions)
        draw_button("Quit", WIDTH // 3, HEIGHT // 3 + 70, 200, 50, quit_game)

        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
               quit_game()

# Track if game process is running
game_process = None

# Function to open instructions in a separate file
def open_instructions():
    print("Instructions button clicked!")  # Debugging output
    if not is_instructions_running():
        subprocess.Popen(["python", "instructions.py"])

# Function to check if instructions.py is already running
def is_instructions_running():
    for process in psutil.process_iter(attrs=["pid", "name", "cmdline"]):
        cmdline = process.info.get("cmdline", [])
        if cmdline and "instructions.py" in cmdline:
            return True  # Instruction window is already open
    return False  # Not running

# Settings Page
def settings():
    running = True
    while running:
        screen.fill(BLACK)
        text_surface = font.render("Settings: Customize game here.", True, WHITE)
        screen.blit(text_surface, (WIDTH // 6, HEIGHT // 3))
        draw_button("Back", WIDTH // 3, HEIGHT // 2, 200, 50, main_menu, )
        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

# Main Menu
def main_menu():
    running = True
    while running:
        screen.blit(background, (0, 0))
        

        draw_button("Start Game", WIDTH // 3, HEIGHT // 3, 200, 50, start_game)
        draw_button("Instructions", WIDTH // 3, HEIGHT // 3 + 70, 200, 50, open_instructions)
        draw_button("Settings", WIDTH // 3, HEIGHT // 3 + 140, 200, 50, settings)
        draw_button("Quit", WIDTH // 3, HEIGHT // 3 + 210, 200, 50, pygame.quit)

        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

# Quit Game Function
def quit_game():
    global game_process
    # Terminate test.py if running
    if game_process and game_process.poll() is None:
        game_process.terminate()  # Try to terminate gracefully
        game_process.wait()  # Wait for the process to exit

    pygame.quit()  # Quit Pygame
    sys.exit()  # Ensure script fully exits

# Run the main menu
main_menu()

