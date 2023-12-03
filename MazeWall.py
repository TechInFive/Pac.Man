import pygame
from constants import WALL_COLOR

class MazeWall:
    def __init__(self, maze_data):
        self.maze_data = maze_data

        self.wall_points = {}
        self.calculate_wall_points()

        self.wall_color = WALL_COLOR

    def is_wall(self, col, row):
        if col <= 0 or row <= 0 or col >= self.maze_data.cols - 1 or row >= self.maze_data.rows - 1:
            return True
        return self.maze_data.is_wall(col, row)

    def calculate_wall_points(self):
        cell_width = self.maze_data.cell_width 
        cell_height = self.maze_data.cell_height
        span_x = cell_width // 3
        span_y = cell_height // 3

        cell_points = [
            (0, cell_height - span_y),
            (0, span_y),
            (span_x, span_y),
            (span_x, 0),
            (cell_width - span_x, 0),
            (cell_width - span_x, span_y),
            (cell_width,  span_y),
            (cell_width, cell_height - span_y),
            (cell_width - span_x, cell_height - span_y),
            (cell_width - span_x, cell_height),
            (span_x, cell_height),
            (span_x, cell_height - span_y)
        ]

        for row in range(self.maze_data.rows):
            for col in range(self.maze_data.cols):
                if self.is_wall(col, row):
                    (cell_x, cell_y) = self.maze_data.get_cell_x_y(col, row)
                    points = [(cell_x + cell_point[0], cell_y + cell_point[1]) for cell_point in cell_points]
                    self.wall_points[(col, row)]  = self.calculate_cell_points(col, row, points)

    def calculate_cell_points(self, col, row, points):
        is_left_wall = self.is_wall(col - 1, row)
        is_up_wall = self.is_wall(col, row - 1)
        is_right_wall = self.is_wall(col + 1, row)
        is_down_wall = self.is_wall(col, row + 1)

        if is_left_wall and is_right_wall and is_up_wall and is_down_wall:
            if not self.is_wall(col - 1, row - 1):
                return [ points[0], points[1], points[2], points[3], points[4], points[8] ]
                
            if not self.is_wall(col - 1, row + 1):
                return [ points[0], points[1], points[5], points[9], points[10], points[11] ]

            if not self.is_wall(col + 1, row - 1):
                return [ points[3], points[4], points[5], points[6], points[7], points[11] ]

            if not self.is_wall(col + 1, row + 1):
                return [ points[6], points[7], points[8], points[9], points[10], points[2] ]

            else:
                return None
            
        if is_left_wall and is_right_wall:
            return [ points[0], points[1], points[6], points[7] ]
 
        if is_up_wall and is_down_wall:
            return [ points[3], points[4], points[9], points[10] ]

        wall_points = []
        if is_left_wall:
            wall_points.append(points[0])
            wall_points.append(points[1])
        wall_points.append(points[2])

        if is_up_wall:
            wall_points.append(points[3])
            wall_points.append(points[4])
        wall_points.append(points[5])

        if is_right_wall:
            wall_points.append(points[6])
            wall_points.append(points[7])
        wall_points.append(points[8])

        if is_down_wall:
            wall_points.append(points[9])
            wall_points.append(points[10])
        wall_points.append(points[11])
        return wall_points

    def draw_wall(self, screen, col, row):
        if (col, row) in self.wall_points:
            if self.wall_points[(col, row)] != None:
                pygame.draw.polygon(screen, self.wall_color, self.wall_points[(col, row)])
