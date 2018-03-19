import numpy as np

class Board(object):

    def __init__(self,board_width = 4,four_probability = 0.1):
        # Intialize the game parameters
        self.board_width = board_width
        self.four_probability = four_probability
        self.grid = np.zeros((self.board_width,self.board_width),np.int64)

    def start(self):
        # Returns a representation of the starting state of the game.
        self.grid = np.zeros((self.board_width,self.board_width),np.int64)
        # Define the state as a tuple of the current player and grid
        state = (0,self.grid)
        return state

    def current_player(self, state):
        # Takes the game state and returns the current player's
        # number.
        return state[0]

    def next_state(self, state, play):
        # Takes the game state, and the move to be applied.
        # Returns the new game state.
        player, grid = state

        if(player==0):
            i = play//self.board_width
            j = play%self.board_width
            new_tile = np.random.rand()<self.four_probability?4:2
            grid[i,j] = new_tile
            state = (1,grid)
        elif(player==1):
            grid = move_grid(grid,play)
            state = (0,grid)

        return state

    def legal_plays(self, state_history):
        # Takes a sequence of game states representing the full
        # game history, and returns the full list of moves that
        # are legal plays for the current player.
        state = state_history[-1]
        player, grid = state
        legal_moves = []

        if(player==0):
            flat_grid = np.flatten(grid)
            legal_moves = [i for i, e in enumerate(flat_grid) if e == 0]
        if(player==1):
            legal_moves = player_legal_moves(grid)

        return legal_moves

    def winner(self, state_history):
        # Takes a sequence of game states representing the full
        # game history.  If the game is now won, return the player
        # number.  If the game is still ongoing, return zero.  If
        # the game is tied, return a different distinct value, e.g. -1.
        state = state_history[-1]
        player, grid = state

        if np.maximum(grid)>=2048:
            return 1
        elif len(legal_plays(state_history))==0
            return -1
        else
            return 0

## Helper Functions for state calculation

    def move_grid(self, grid, play):
        # This function moves the grid in accordance to the action chosen
        assert(play<4)
        grid = rotate_grid(grid,play)
        grid = compress_grid(grid)
        grid = merge_grid(grid)
        grid = compress_grid(grid)
        grid = rotate_grid(grid,4-play)
        return grid

    def rotate_grid(self, grid, play):
        # This function rotates the grid into the correct orientation for compress -> merge -> compress
        # Implicitly this would imply the following mapping
        # 0 -> "left"
        # 1 -> "up"
        # 2 -> "right"
        # 3 -> "down"
        grid = np.rot90(grid,k=play)
        return grid

    def compress_grid(self, grid):
        # This function compresses a grid row-wise as if there was a "left" operation
        for rownum in range(self.board_width):
            row = grid[rownum,:]
            compressed_row = np.concatenate(row[row!=0],row[row==0])
            grid[rownum,:] = compressed_row
        return grid

    def merge_grid(self, grid):
        # This fucntion merges a grid row-wise as if there was a "left" operation
        for i in range(self.board_width):
            for j in range(self.board_width-1):
                if grid[i,j]==grid[i,j+1]:
                    grid[i,j] = grid[i,j]*2
                    grid[i,j+1] = 0
        return grid

    def player_legal_moves(self,grid):
        legal_moves = []
        for play in range(4):
            if grid != move_grid(grid,play):
                legal_moves.append(play)
        return legal_moves
