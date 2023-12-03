import threading

import pygame

from Direction import Direction
from constants import MOVE_EVENT

DIRECTIONS = {
    Direction.RIGHT: (1, 0),
    Direction.LEFT: (-1, 0),
    Direction.UP: (0, -1),
    Direction.DOWN: (0, 1)
}

class GameCharacter(threading.Thread):
    def __init__(self, x, y):
        super().__init__()
        self.x = x
        self.y = y
        self.step = 0

        self.running = False

    def start(self, maze_data, direction):
        self.maze_data = maze_data
        self.direction = direction

        (col, row) = self.maze_data.at_cell(self.x, self.y)
        self.col = col
        self.row = row

        self.running = True
        super().start()

    def stop(self):
        self.running = False

    def at_cell(self):
        return (self.col, self.row)

    def at_cell_center(self):
        (col, row) = self.at_cell()
        (center_x, center_y) = self.maze_data.get_center(col, row)
        return center_x == self.x and abs(center_y - self.y) < self.step or center_y == self.y and abs(center_x - self.x) < self.step

    def next_cell(self, col, row, direction):
        (col_adjust, row_adjust) = DIRECTIONS.get(direction)
        return (col + col_adjust, row + row_adjust)

    def move_to_cell_center(self):
        (col, row) = self.at_cell()
        (center_x, center_y) = self.maze_data.get_center(col, row)
        self.x = center_x
        self.y = center_y

    def face_a_wall(self, direction):
        (col, row) = self.at_cell()
        (next_col, next_row) = self.next_cell(col, row, direction)
        return self.maze_data.is_wall(next_col, next_row)

    def get_options(self):
        options = []

        for direction in Direction:
            if not self.face_a_wall(direction):
                options.append(direction)
        return options

    def check_new_direction(self):
        if self.at_cell_center():
            new_direction = self.make_a_decision()
            if new_direction is not None:
                self.change_direction(new_direction)

    def change_direction(self, new_direction):
        self.direction = new_direction
        self.move_to_cell_center()

        self.apply_direction()

    def move(self):
        self.check_new_direction()
 
        match self.direction:
            case Direction.RIGHT:
                self.x += self.step
            case Direction.DOWN:
                self.y +=  self.step
            case Direction.LEFT:
                self.x -=  self.step
            case Direction.UP:
                self.y -=  self.step

        (col, row) = self.maze_data.at_cell(self.x, self.y)
        if col != self.col or row != self.row:
            self.col, self.row = col, row
            self.on_enter_new_cell()

    def make_a_decision(self):
        return None

    def apply_direction(self):
        pass

    def on_enter_new_cell(self):
        event = pygame.event.Event(MOVE_EVENT, message=(self.__class__.__name__, self.col, self.row, self.direction))
        pygame.event.post(event)

