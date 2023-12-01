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
maze = Maze()

ghost_start_points = maze.ghost_start_points()
ghosts = [
    Ghost(ghost_start_points[0][0], ghost_start_points[0][1], (255, 192, 203), Direction.RIGHT),
    Ghost(ghost_start_points[1][0], ghost_start_points[1][1], (255, 215, 0), Direction.DOWN),
    Ghost(ghost_start_points[2][0], ghost_start_points[2][1], (255, 0, 0), Direction.UP),
    Ghost(ghost_start_points[3][0], ghost_start_points[3][1], (0, 255, 255), Direction.LEFT)
]

for ghost in ghosts:
    ghost.start(maze.maze_data)

(pacman_x, pacman_y) = maze.pac_man_start_point()
pacman = PacMan(pacman_x, pacman_y, Direction.RIGHT)
pacman.start(maze.maze_data)

# Game loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            pacman.stop()
            for ghost in ghosts:
                ghost.stop()

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                pacman.instruction = Direction.LEFT
            elif event.key == pygame.K_RIGHT:
                pacman.instruction = Direction.RIGHT
            elif event.key == pygame.K_UP:
                pacman.instruction = Direction.UP
            elif event.key == pygame.K_DOWN:
                pacman.instruction = Direction.DOWN

        if event.type == pygame.KEYUP:
            pacman.instruction = None

    window.fill((0, 0, 0))  # Clear screen with black background

    # Draw game elements
    maze.draw(window)
    pacman.draw(window)
    for ghost in ghosts:
        ghost.draw(window)

    pygame.display.flip()  # Update the display

# Quit PyGame
pygame.quit()
sys.exit()
