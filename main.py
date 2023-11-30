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
pacman1 = PacMan(320, 239, Direction.RIGHT)
pacman2 = PacMan(345, 239, Direction.RIGHT)
pacman2.toggle_mouth()
pacman3 = PacMan(370, 239, Direction.LEFT)
pacman4 = PacMan(395, 239, Direction.LEFT)
pacman4.toggle_mouth()
pacman5 = PacMan(420, 239, Direction.UP)
pacman6 = PacMan(445, 239, Direction.UP)
pacman6.toggle_mouth()
pacman7 = PacMan(270, 239, Direction.DOWN)
pacman8 = PacMan(295, 239, Direction.DOWN)
pacman8.toggle_mouth()

maze = Maze()
print(maze.maze_data.get_center(14, 10))
print(maze.maze_data.get_center(12, 13))
print(maze.maze_data.get_center(14, 13))
print(maze.maze_data.get_center(16, 13))

ghosts = [
    Ghost(295, 305, (255, 192, 203), maze.maze_data.cell_width, maze.maze_data.cell_height),  # Red ghost
    Ghost(345, 305, (255, 215, 0), maze.maze_data.cell_width, maze.maze_data.cell_height),  # Red ghost
    Ghost(370, 305, (255, 0, 0), maze.maze_data.cell_width, maze.maze_data.cell_height),  # Gold ghost
    Ghost(420, 305, (0, 255, 255), maze.maze_data.cell_width, maze.maze_data.cell_height),  # Aque ghost
]
ghosts[1].move_state = 1
ghosts[1].direction = Direction.DOWN
ghosts[2].direction = Direction.LEFT
ghosts[3].move_state = 1
ghosts[3].direction = Direction.UP

# Game loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    window.fill((0, 0, 0))  # Clear screen with black background

    # Animate Pac-Man's mouth
    # pacman.toggle_mouth()

    # Draw game elements
    pacman1.draw(window)
    pacman2.draw(window)
    pacman3.draw(window)
    pacman4.draw(window)
    pacman5.draw(window)
    pacman6.draw(window)
    pacman7.draw(window)
    pacman8.draw(window)
    for ghost in ghosts:
        ghost.draw(window)
    maze.draw(window)

    pygame.display.flip()  # Update the display
    # pygame.time.wait(200)  # Wait a bit before the next frame

# Quit PyGame
pygame.quit()
sys.exit()
