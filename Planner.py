from GameCharacter import DIRECTIONS
from Ghost import GHOST_INTERVAL, Ghost

class Planner(Ghost):
    def ghost_choice(self, options):
        # Find a move toward a predicted place
        (player_col, player_row) = self.maze_data.player_trail[-1]
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

        # Take a break
        self.break_time = 1 / GHOST_INTERVAL
        return None
