from constants import MARGIN_X, MARGIN_Y, MAZE_HEIGHT, MAZE_WIDTH

class MazeData:
    def __init__(self, maze_data):
        self.maze_data = maze_data

        self.rows = len(self.maze_data)
        self.cols = len(self.maze_data[0])

        self.cell_width = MAZE_WIDTH // self.cols 
        self.cell_height = MAZE_HEIGHT // self.rows 

        self.player_trail = []

    def is_wall(self, col, row):
        return self.maze_data[row][col] == 1

    def is_pellet(self, col, row):
        return self.maze_data[row][col] == 2

    def remove_pellet(self, col, row):
        if self.is_pellet(col, row):
            self.maze_data[row][col] = 0

    def get_cell_x_y(self, col, row):
        return (MARGIN_X + self.cell_width * col, MARGIN_Y + self.cell_height * row)

    def get_center(self, col, row):
        (cell_x, cell_y) = self.get_cell_x_y(col, row) 
        return (cell_x + self.cell_width // 2, cell_y + self.cell_height // 2)

    def at_cell(self, x, y):
        col = (x - MARGIN_X ) // self.cell_width
        row = (y - MARGIN_Y ) // self.cell_height
        return (col, row)

    def update_player_trail(self, current_cell):
        if current_cell in self.player_trail:
            return
        self.player_trail.append(current_cell)
        if len(self.player_trail) > 3:  # Keep only the last 3 positions
            self.player_trail.pop(0)
