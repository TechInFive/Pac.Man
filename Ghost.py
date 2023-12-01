import random
import time
import pygame

from Direction import Direction
from GameCharacter import GameCharacter

from constants import SCALE

GHOST_INTERVAL = 0.2 # 200ms
GHOST_STEP = 2 * SCALE

class Ghost(GameCharacter):
    def __init__(self, x, y, color, direction):
        super().__init__(x, y, direction)

        self.color = color
        self.eye_color = (0, 0, 0)
        self.eye_ball_color = (255, 255, 255)
        self.move_state = 0
        self.step = GHOST_STEP

    def start(self, maze_data):
        super().start(maze_data)

        self.width = maze_data.cell_width
        self.height = maze_data.cell_height


    def run(self):
        self.apply_direction()

        while self.running:
            self.wiggle()
            self.move()
            time.sleep(GHOST_INTERVAL)

    def wiggle(self):
        self.move_state = 0 if self.move_state == 1 else 1

    def make_a_decision(self):
        options = self.get_options()

        # First check if Pac-Man is nearby
        for direction in options:
            if self.is_player_in_direction(direction):
                return direction

        # 75% of chance keep moving
        if self.direction in options:
            if random.random() < 0.75:
                return None

        # Randomly choose a direction
        return random.choice(options)

    def is_player_in_direction(self, direction):
        (col, row) = self.at_cell()

        while not self.maze_data.is_wall(col, row):
            (col, row) = self.next_cell(col, row, direction)
            if (col, row) in self.maze_data.player_trail:
                return True

        return False

    def draw(self, screen):
        # head
        head_radius = self.width // 2
        pygame.draw.circle(screen, self.color, (self.x, self.y), head_radius, draw_top_left=True, draw_top_right=True)

        # body
        pygame.draw.rect(screen, self.color, (self.x - self.width // 2, self.y, self.width, self.height // 2))

        # draw leg
        left_x = self.x - self.width // 2
        leg_xs = [left_x + self.width // 4 * leg for leg in range(5)]
        leg_top = self.y + self.height // 2
        leg_bottom = self.y + self.height * 3 // 4

        for leg in range(4):
            top_left = leg_xs[leg]
            top_right = leg_xs[leg + 1]
            bottom_x = (top_left + top_right) // 2
            shift = self.width // 10
            if leg % 2 == 0:
                shift = -shift

            if self.move_state == 1:
                shift = - (shift // 2)

            leg_points = [
                (top_left, leg_top),
                (top_right, leg_top),
                (bottom_x + shift, leg_bottom),
            ]
            pygame.draw.polygon(screen, self.color, leg_points)

        # Draw eyes
        eye_width = self.width // 3
        eye_height = self.width // 2

        eye_ball_y = self.y - self.height // 4

        left_eye_x = self.x - self.width // 3 - 1
        right_eye_x = self.x + 1

        eye_offset_x = eye_width // 2
        eye_offset_y = eye_height // 2

        match self.direction:
            case Direction.UP:
                eye_ball_y -=  SCALE
                eye_offset_y -= SCALE
            case Direction.DOWN:
                eye_ball_y += SCALE
                eye_offset_y += SCALE
            case Direction.LEFT:
                left_eye_x -= SCALE
                right_eye_x -= SCALE
                eye_offset_x -= SCALE
            case Direction.RIGHT:
                left_eye_x += SCALE
                right_eye_x += SCALE
                eye_offset_x += SCALE
            # case _:
    
        pygame.draw.ellipse(screen, self.eye_ball_color, (left_eye_x, eye_ball_y, eye_width, eye_height))
        pygame.draw.circle(screen, self.eye_color, (left_eye_x + eye_offset_x, eye_ball_y + eye_offset_y), 2)

        pygame.draw.ellipse(screen, self.eye_ball_color, (right_eye_x, eye_ball_y, eye_width, eye_height))
        pygame.draw.circle(screen, self.eye_color, (right_eye_x + eye_offset_x, eye_ball_y + eye_offset_y), 2)
