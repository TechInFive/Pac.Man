import pygame
import sys

from Cruiser import Cruiser
from Direction import Direction
from Ghost import Ghost
from Maze import Maze
from Planner import Planner
from Sniffer import Sniffer

from PacMan import PacMan
from Trickster import Trickster
from constants import FONT_COLOR, GAME_OVER, MOVE_EVENT, WINDOW_HEIGHT, WINDOW_WIDTH

# Initialize PyGame
pygame.init()

# Set the dimensions of the game screen
screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption('PyGame Drawing: Pac-Man and Elements')
font = pygame.font.Font(None, 24)  # Default font with size 24

# Create game elements
maze = Maze()

ghost_start_points = maze.ghost_start_points()
ghosts = [
    Cruiser(ghost_start_points[0][0], ghost_start_points[0][1], (255, 192, 203)),
    Sniffer(ghost_start_points[1][0], ghost_start_points[1][1], (255, 215, 0)),
    Planner(ghost_start_points[2][0], ghost_start_points[2][1], (255, 0, 0)),
    Trickster(ghost_start_points[3][0], ghost_start_points[3][1], (0, 255, 255))
]

for ghost in ghosts:
    ghost.start(maze.maze_data, Direction.RIGHT)

(pacman_x, pacman_y) = maze.pac_man_start_point()
pacman = PacMan(pacman_x, pacman_y)
pacman.start(maze.maze_data, Direction.RIGHT)

show_target = False

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
                pacman.receive_instruction(Direction.LEFT)
            elif event.key == pygame.K_RIGHT:
                pacman.receive_instruction(Direction.RIGHT)
            elif event.key == pygame.K_UP:
                pacman.receive_instruction(Direction.UP)
            elif event.key == pygame.K_DOWN:
                pacman.receive_instruction(Direction.DOWN)

        if event.type == MOVE_EVENT:
            maze.handle_event(event)

        if event.type == GAME_OVER:
            running = False
            pacman.stop()
            for ghost in ghosts:
                ghost.stop()

    screen.fill((0, 0, 0))  # Clear screen with black background

    # Draw game elements
    maze.draw(screen)
    pacman.draw(screen)
    for ghost in ghosts:
        ghost.draw(screen)
        if ghost.target_cell is not None and show_target == True:
            (target_x, target_y) = maze.maze_data.get_center(ghost.target_cell[0], ghost.target_cell[1])
            pygame.draw.circle(screen, ghost.color, (target_x, target_y), ghost.width, 1)
            pygame.draw.line(screen, ghost.color, (target_x, target_y - ghost.height // 2), (target_x, target_y + ghost.height // 2), 1)
            pygame.draw.line(screen, ghost.color, (target_x - ghost.width // 2, target_y), (target_x + ghost.width // 2, target_y), 1)

    # Display score
    score_text = font.render(f"Score: {maze.player_score}", True, FONT_COLOR)
    screen.blit(score_text, (10, WINDOW_HEIGHT - 30))  # Position the score in the top-left corner

    pygame.display.flip()  # Update the display

# Quit PyGame
pygame.quit()
sys.exit()
