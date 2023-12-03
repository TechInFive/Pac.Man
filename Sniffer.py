from Ghost import GHOST_INTERVAL, Ghost

class Sniffer(Ghost):
    def ghost_choice(self, options):
        # Find a move toward player
        (player_col, player_row) = self.maze_data.player_trail[-1]

        toward_direction = self.find_direction_to_target(options, player_col, player_row)
        if toward_direction is not None:
            self.target_cell = (player_col, player_row)
            return toward_direction

        self.target_cell = None

        # Take a break
        self.break_time = 1 / GHOST_INTERVAL
        return None
