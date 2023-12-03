import random
import time
from Ghost import GHOST_INTERVAL, Ghost

class Trickster(Ghost):
    def ghost_choice(self, options):
        # Teleport
        (target_col, target_row) = self.maze_data.get_random_path_cell()
        (target_x, target_y) = self.maze_data.get_center(target_col, target_row)

        time.sleep(GHOST_INTERVAL * 5)

        self.x, self.y = target_x, target_y
        self.col, self.row = target_col, target_row
        new_options = self.get_options()
        self.direction = random.choice(new_options)

        time.sleep(GHOST_INTERVAL * 1)

        # Take a break
        self.break_time = 5 / GHOST_INTERVAL

        return self.direction

