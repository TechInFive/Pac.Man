import random
import time
from GameCharacter import DIRECTIONS
from Ghost import GHOST_INTERVAL, Ghost

class Trickster(Ghost):
    def __init__(self, x, y, color):
        super().__init__(x, y, color)

        self.current_trick = None

    def ghost_choice(self, options):
        if self.current_trick is None:
            random_number = random.randint(1, 9)
            if random_number <= 4:
                self.current_trick = 1
            elif random_number <= 7:
                self.current_trick = 2
            else:
                self.current_trick = 3

        # Teleport
        if self.current_trick == 3:
            (target_col, target_row) = self.maze_data.get_random_path_cell()
            (target_x, target_y) = self.maze_data.get_center(target_col, target_row)

            time.sleep(GHOST_INTERVAL * 5)

            self.x = target_x
            self.y = target_y
            self.col = target_col
            self.row = target_row
            new_options = self.get_options()
            self.direction = random.choice(new_options)

            time.sleep(GHOST_INTERVAL * 1)

            self.current_trick = None
            return self.direction

        (player_col, player_row) = self.maze_data.player_trail[-1]

        if self.current_trick == 1:
            target_col = player_col
            target_row = player_row
        else:
            player_direction = self.maze_data.player_direction
            (col_adjust, row_adjust) = DIRECTIONS.get(player_direction)
            target_col = player_col + 5 * col_adjust
            target_row = player_row + 5 * row_adjust

            target_col = max(0, min(target_col, self.maze_data.cols - 1))
            target_row = max(0, min(target_row, self.maze_data.rows - 1))

        toward_direction = self.find_direction_to_target(options, target_col, target_row)
        if toward_direction is not None:
            self.target_cell = (target_col, target_row)
            return toward_direction

        self.target_cell = None
        self.current_trick = None

        # Take a break
        self.break_time = 1 / GHOST_INTERVAL
        return None
