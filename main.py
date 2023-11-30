import pygame
import sys
from Direction import Direction
from Ghost import Ghost
from Maze import Maze

from PacMan import PacMan
from constants import WINDOW_HEIGHT, WINDOW_WIDTH

# Initialize PyGame
pygame.init()

# Set the dimensions of the game window
window = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption('PyGame Drawing: Pac-Man and Elements')

# Create game elements
pacman = PacMan(320, 239, Direction.RIGHT)
pacman.start()

maze = Maze()

ghosts = [
    Ghost(295, 305, (255, 192, 203), maze.maze_data.cell_width, maze.maze_data.cell_height),  # Pink ghost
    Ghost(345, 305, (255, 215, 0), maze.maze_data.cell_width, maze.maze_data.cell_height),  # Gold ghost
    Ghost(370, 305, (255, 0, 0), maze.maze_data.cell_width, maze.maze_data.cell_height),  # Red ghost
    Ghost(420, 305, (0, 255, 255), maze.maze_data.cell_width, maze.maze_data.cell_height),  # Aque ghost
]
for ghost in ghosts:
    ghost.start()

# Game loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            pacman.stop()
            for ghost in ghosts:
                ghost.stop()

    window.fill((0, 0, 0))  # Clear screen with black background

    # Animate Pac-Man's mouth
    # pacman.toggle_mouth()

    # Draw game elements
    pacman.draw(window)

    for ghost in ghosts:
        ghost.draw(window)
    maze.draw(window)

    pygame.display.flip()  # Update the display
    # pygame.time.wait(200)  # Wait a bit before the next frame

# Quit PyGame
pygame.quit()
sys.exit()
