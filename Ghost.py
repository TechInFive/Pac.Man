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
        self.width = maze_data.cell_width
        self.height = maze_data.cell_height

        self.head_radius = self.width // 2
        self.eye_width = self.width // 3
        self.eye_height = self.width // 2

        super().start(maze_data)

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

        # 80% of chance keep moving
        if self.direction in options:
            if random.random() < 0.8:
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

    def apply_direction(self):
        self.eye_offset_y = - self.height // 4

        self.pupil_offset_x = self.eye_width // 2
        self.pupil_offset_y = self.eye_height // 2

        self.left_eye_offset = - self.width // 3 - 1
        self.right_eye_offset = 1

        match self.direction:
            case Direction.UP:
                self.eye_offset_y -=  SCALE
                self.pupil_offset_y -= SCALE
            case Direction.DOWN:
                self.eye_offset_y += SCALE
                self.pupil_offset_y += SCALE
            case Direction.LEFT:
                self.left_eye_offset -= SCALE
                self.right_eye_offset -= SCALE
                self.pupil_offset_x -= SCALE
            case Direction.RIGHT:
                self.left_eye_offset += SCALE
                self.right_eye_offset += SCALE
                self.pupil_offset_x += SCALE
  
    def draw(self, screen):
        # head
        pygame.draw.circle(screen, self.color, (self.x, self.y), self.head_radius, draw_top_left=True, draw_top_right=True)

        # body
        pygame.draw.rect(screen, self.color, (self.x - self.head_radius, self.y, self.width, self.height // 2))

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

        left_eye_x = self.x + self.left_eye_offset
        right_eye_x = self.x + self.right_eye_offset
        eye_y = self.y + self.eye_offset_y

        pygame.draw.ellipse(screen, self.eye_ball_color, (left_eye_x, eye_y, self.eye_width, self.eye_height))
        pygame.draw.circle(screen, self.eye_color, (left_eye_x + self.pupil_offset_x, eye_y + self.pupil_offset_y), 2)

        pygame.draw.ellipse(screen, self.eye_ball_color, (right_eye_x, eye_y, self.eye_width, self.eye_height))
        pygame.draw.circle(screen, self.eye_color, (right_eye_x + self.pupil_offset_x, eye_y + self.pupil_offset_y), 2)
