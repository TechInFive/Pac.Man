import math
import time
import pygame
from Direction import Direction
from GameCharacter import GameCharacter

from constants import BACKGROUND_COLOR, MOVE_EVENT, PAC_MAN_COLOR, SCALE

PAC_MAN_RADIUS = 6 * SCALE
PAC_MAN_INTERVAL = 0.15 # 150ms
PAC_MAN_STEP = 2 * SCALE

class PacMan(GameCharacter):
    def __init__(self, x, y):
        super().__init__(x, y)

        self.radius = PAC_MAN_RADIUS

        self.color = PAC_MAN_COLOR
        self.eye_color = BACKGROUND_COLOR
        self.step = PAC_MAN_STEP

        self.mouth_open = False

        self.instruction = None

    def run(self):
        self.apply_direction()

        while self.running:
            self.toggle_mouth()
            self.move()

            time.sleep(PAC_MAN_INTERVAL)

    def toggle_mouth(self):
        self.mouth_open = not self.mouth_open

    def check_new_direction(self):
        new_direction = self.make_a_decision()
        if new_direction is not None:
            self.change_direction(new_direction)

    def make_a_decision(self):
        if self.face_a_wall(self.direction):
            match self.direction:
                case Direction.RIGHT:
                    return Direction.LEFT
                case Direction.DOWN:
                    return Direction.UP
                case Direction.LEFT:
                    return Direction.RIGHT
                case Direction.UP:
                    return Direction.DOWN
        return None

    def apply_direction(self):
        match self.direction:
            case Direction.RIGHT:
                self.eye_offset_x = 0
                self.eye_offset_y = - self.radius // 2
                self.mouth_close_start_angle = 1
                self.mouth_close_end_angle = -1
                self.mouth_open_start_angle = 30
                self.mouth_open_end_angle = -30
            case Direction.DOWN:
                self.eye_offset_x = - self.radius // 2
                self.eye_offset_y = 0
                self.mouth_close_start_angle = 269
                self.mouth_close_end_angle = 271
                self.mouth_open_start_angle = 240
                self.mouth_open_end_angle = 300
            case Direction.LEFT:
                self.eye_offset_x = 0
                self.eye_offset_y = - self.radius // 2
                self.mouth_close_start_angle = 179
                self.mouth_close_end_angle = 181
                self.mouth_open_start_angle = 210
                self.mouth_open_end_angle = 150
            case Direction.UP:
                self.eye_offset_x = self.radius // 2
                self.eye_offset_y = 0
                self.mouth_close_start_angle = 89
                self.mouth_close_end_angle = 91
                self.mouth_open_start_angle = 60
                self.mouth_open_end_angle = 120

    def receive_instruction(self, instruction):
        if self.verify_instruction(instruction):
            self.change_direction(instruction)

    def verify_instruction(self, instruction):
        if (instruction is not None
            and instruction != self.direction
            and not self.face_a_wall(instruction)):
            return True
        return False

    def on_enter_new_cell(self):
        event = pygame.event.Event(MOVE_EVENT, message=(self.__class__.__name__, self.col, self.row, self.direction))
        pygame.event.post(event)
        pass

    def draw_filled_pie(self, screen, color, center, radius, start_degree, end_degree, num_segments):
        # Convert angles to radians and calculate the angle step for each segment
        start_angle = math.radians(start_degree)
        end_angle = math.radians(end_degree)
        angle_step = (end_angle - start_angle) / num_segments

        # Calculate points along the arc
        arc_points = [center]
        for segment in range(num_segments + 1):
            angle = start_angle + segment * angle_step
            point_x = center[0] + radius * math.cos(angle)
            point_y = center[1] - radius * math.sin(angle)
            arc_points.append((point_x, point_y))

        # Draw the filled pie shape (polygon)
        pygame.draw.polygon(screen, color, arc_points)
        
    def draw(self, screen):
        # Draw the main circle for the body
        pygame.draw.circle(screen, self.color, (self.x, self.y), self.radius)

        # Draw the eye
        eye_x = self.x + self.eye_offset_x
        eye_y = self.y + self.eye_offset_y
        pygame.draw.circle(screen, self.eye_color, (eye_x, eye_y), 3)

        # Draw the mouth
        if self.mouth_open:
            start_degree = self.mouth_close_start_angle
            end_degree = self.mouth_close_end_angle
            num_segments = 4
        else:
            start_degree = self.mouth_open_start_angle
            end_degree = self.mouth_open_end_angle
            num_segments = 20
        self.draw_filled_pie(screen, BACKGROUND_COLOR, (self.x, self.y), self.radius, start_degree, end_degree, num_segments)

