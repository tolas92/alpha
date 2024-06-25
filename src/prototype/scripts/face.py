import pygame
import time
import random
from pygame.locals import *

# Initialize Pygame
pygame.init()

# Set up the screen
screen_width, screen_height = 800, 600
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Blinking and Smiling Robot Face")

# Load pixelated eye and mouth images
eye_image = pygame.Surface((50, 30), pygame.SRCALPHA)
pygame.draw.circle(eye_image, (0, 0, 0), (25, 15), 15)

mouth_image = pygame.Surface((50, 20), pygame.SRCALPHA)
pygame.draw.arc(mouth_image, (0, 0, 0), (15, 0, 20, 20), 0, 3.14, 2)

# Initial position of eyes and mouth
eye_y = 200
mouth_x, mouth_y = 200, 350

# Function to draw the face
def draw_face():
    # Draw eyes and mouth
    screen.blit(eye_image, (200, eye_y))
    screen.blit(eye_image, (350, eye_y))
    screen.blit(mouth_image, (mouth_x, mouth_y))

# Main loop
running = True
while running:
    # Handle events
    for event in pygame.event.get():
        if event.type == QUIT:
            running = False

    # Clear the screen
    screen.fill((255, 255, 255))

    # Draw the face
    draw_face()

    # Update the display
    pygame.display.flip()

    # Wait for a random amount of time (between 1 to 3 seconds) to simulate blinking
    time.sleep(random.uniform(1, 3))

    # Move mouth up to simulate smiling
    for _ in range(10):
        screen.fill((255, 255, 255))  # Clear the screen
        mouth_y -= 1  # Move the mouth up
        draw_face()  # Redraw the face
        pygame.display.flip()  # Update the display
        time.sleep(0.05)  # Add a small delay for smooth animation

    # Move mouth down to simulate going back to normal
    for _ in range(10):
        screen.fill((255, 255, 255))  # Clear the screen
        mouth_y += 1  # Move the mouth down
        draw_face()  # Redraw the face
        pygame.display.flip()  # Update the display
        time.sleep(0.05)  # Add a small delay for smooth animation

# Quit Pygame
pygame.quit()
