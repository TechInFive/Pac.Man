import time
import pygame
import threading

from Direction import Direction

from constants import SCALE

GHOST_INTERVAL = 0.2 # 200ms
GHOST_STEP = 2 * SCALE

class Ghost(threading.Thread):
    def __init__(self, x, y, color, width, height):
        super().__init__()
        self.running = False

        self.x = x
        self.y = y
        self.color = color
        self.eye_color = (0, 0, 0)
        self.eye_ball_color = (255, 255, 255)
        self.width = width
        self.height = height
        self.move_state = 0
        self.direction = Direction.RIGHT

    def start(self):
        self.running = True
        super().start()

    def stop(self):
        self.running = False

    def run(self):
        while self.running:
            self.wiggle()
            self.move()
            time.sleep(GHOST_INTERVAL)

    def wiggle(self):
        self.move_state = 0 if self.move_state == 1 else 1

    def move(self):
        # Logic to move PacMan
        match self.direction:
            case Direction.RIGHT:
                self.x += GHOST_STEP
            case Direction.DOWN:
                self.y += GHOST_STEP
            case Direction.LEFT:
                self.x -= GHOST_STEP
            case Direction.UP:
                self.y -= GHOST_STEP

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
