"""
Clone of 2048 game.
"""

import poc_2048_gui
import random

# Directions, DO NOT MODIFY
UP = 1
DOWN = 2
LEFT = 3
RIGHT = 4

# Offsets for computing tile indices in each direction.
# DO NOT MODIFY this dictionary.
OFFSETS = {UP: (1, 0),
           DOWN: (-1, 0),
           LEFT: (0, 1),
           RIGHT: (0, -1)}

def merge(line):
    """
    Helper function that merges a single row or column in 2048
    """
    tam_line = len(line)
    new_line = tam_line * [0]
    index_line = 0
    
    for index in range(tam_line):
        if line[index] != 0:
            tam = index + 1
            while tam < len(line) and line[tam] == 0:
                tam += 1
            if tam < len(line) and line[index] == line[tam]:
                new_line[index_line] = line[index] * 2
                line[tam] = 0
            else:
                new_line[index_line] = line[index]
            index_line += 1
            
    return new_line

class TwentyFortyEight:
    """
    Class to run the game logic.
    """

    def __init__(self, grid_height, grid_width):
        self.height = grid_height
        self.width = grid_width
        self.dic = {UP: [(0, index) for index in range(self.width)],
                   DOWN: [(self.height - 1, index) for index in range(self.width)],
                   LEFT: [(index, 0) for index in range(self.height)],
                   RIGHT: [(index, self.width - 1) for index in range(self.height)]}
        self.num = self.height * self.width - 1
        self.reset()

    def reset(self):
        """
        Reset the game so the grid is empty except for two
        initial tiles.
        """
        self.grid = [[0 for row in range(self.width)]
                    for column in range(self.height)]
        self.new_tile()
        self.new_tile()

    def count_num(self):
        """
        Update the variable count_num
        """
        self.num = 0
        for row in self.grid:
            for value in row:
                if value == 0:
                    self.num += 1
        
    def __str__(self):
        """
        Return a string representation of the grid for debugging.
        """
        msg = "["
        for row in self.grid[:self.height-1]:
            msg += "["
            for value in row[:self.width-1]:
                msg += str(value) + ", "
            msg += str(row[self.width-1]) + "]\n"
            
        
        msg += "["
        for value in self.grid[self.height-1][:self.width-1]:
            msg += str(value) + ", "
        msg += str(self.grid[self.height-1][self.width-1]) + "]"
        msg += "]"
        return msg
        
    def get_grid_height(self):
        """
        Get the height of the board.
        """
        return self.height

    def get_grid_width(self):
        """
        Get the width of the board.
        """
        return self.width

    def move(self, direction):
        """
        Move all tiles in the given direction and add
        a new tile if any tiles moved.
        """
        if direction == LEFT or direction == RIGHT:
            tam = self.width
        else:
            tam = self.height

        in_play = False
        for pos in self.dic[direction]:
            lst = []
            for step in range(tam):
                posx = pos[0] + step * OFFSETS[direction][0]
                posy = pos[1] + step * OFFSETS[direction][1]
                lst.append(self.grid[posx][posy])
            lst = merge(lst)

            for step in range(tam):
                posx = pos[0] + step * OFFSETS[direction][0]
                posy = pos[1] + step * OFFSETS[direction][1]
                if self.grid[posx][posy] != lst[step]:
                    in_play = True
                self.grid[posx][posy] = lst[step]
                
        if in_play:
            self.new_tile()

    def new_tile(self):
        """
        Create a new tile in a randomly selected empty
        square.  The tile should be 2 90% of the time and
        4 10% of the time.
        """
        prob = random.randint(1, 10)
        if prob < 10:
            value = 2
        else:
            value = 4
        
        self.count_num()
        if self.num > 0:
            pos = [random.randrange(self.height), random.randrange(self.width)]
            while self.grid[pos[0]][pos[1]] != 0:
                pos = [random.randrange(self.height), random.randrange(self.width)]
            self.grid[pos[0]][pos[1]] = value
        
        
    def set_tile(self, row, col, value):
        """
        Set the tile at position row, col to have the given value.
        """
        self.grid[row][col] = value
        self.count_num()

    def get_tile(self, row, col):
        """
        Return the value of the tile at position row, col.
        """
        return self.grid[row][col]


#poc_2048_gui.run_gui(TwentyFortyEight(4, 4))
