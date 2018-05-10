"""
Student portion of Zombie Apocalypse mini-project
"""

import random
import poc_grid
import poc_queue
import poc_zombie_gui

# global constants
EMPTY = 0
FULL = 1
FOUR_WAY = 0
EIGHT_WAY = 1
OBSTACLE = 5
HUMAN = 6
ZOMBIE = 7


class Apocalypse(poc_grid.Grid):
    """
    Class for simulating zombie pursuit of human on grid with
    obstacles
    """

    def __init__(self, grid_height, grid_width, obstacle_list = None,
                 zombie_list = None, human_list = None):
        """
        Create a simulation of given size with given obstacles,
        humans, and zombies
        """
        poc_grid.Grid.__init__(self, grid_height, grid_width)
        if obstacle_list != None:
            for cell in obstacle_list:
                self.set_full(cell[0], cell[1])
        if zombie_list != None:
            self._zombie_list = list(zombie_list)
        else:
            self._zombie_list = []
        if human_list != None:
            self._human_list = list(human_list)
        else:
            self._human_list = []

    def clear(self):
        """
        Set cells in obstacle grid to be empty
        Reset zombie and human lists to be empty
        """
        self._cells = [[EMPTY for dummy_col in range(self._grid_width)]
                       for dummy_row in range(self._grid_height)]
        self._zombie_list = []
        self._human_list = []

    def add_zombie(self, row, col):
        """
        Add zombie to the zombie list
        """
        zombie = (row, col)
        self._zombie_list.append(zombie)

    def num_zombies(self):
        """
        Return number of zombies
        """
        return len(self._zombie_list)

    def zombies(self):
        """
        Generator that yields the zombies in the order they were
        added.
        """
        for zombie in self._zombie_list:
            yield tuple(zombie)

    def add_human(self, row, col):
        """
        Add human to the human list
        """
        human = (row, col)
        self._human_list.append(human)

    def num_humans(self):
        """
        Return number of humans
        """
        return len(self._human_list)

    def humans(self):
        """
        Generator that yields the humans in the order they were added.
        """
        for human in self._human_list:
            yield human

    def compute_distance_field(self, entity_type):
        """
        Function computes and returns a 2D distance field
        Distance at member of entity_list is zero
        Shortest paths avoid obstacles and use four-way distances
        """
        _height = self.get_grid_height()
        _width = self.get_grid_width()
        visited = poc_grid.Grid(_height, _width)
        distance_field = [[(_width * _height) for dummy_col in range(_width)] for dummy_row in range(_height)]
        boundary = poc_queue.Queue()
        if entity_type == ZOMBIE:
            for zombie in self._zombie_list:
                boundary.enqueue(zombie)
        elif entity_type == HUMAN:
            for human in self._human_list:
                boundary.enqueue(human)

        # inicialize the visieted and distance_field
        for element in boundary:
            visited.set_full(element[0], element[1])
            distance_field[element[0]][element[1]] = 0

        # BFS
        while len(boundary) > 0:
            current_cell = boundary.dequeue()
            neighbors = visited.four_neighbors(current_cell[0], current_cell[1])
            for neighbor in neighbors:
                if visited.is_empty(neighbor[0], neighbor[1]) and self.is_empty(neighbor[0], neighbor[1]):
                    boundary.enqueue(neighbor)
                    visited.set_full(neighbor[0], neighbor[1])
                    distance_field[neighbor[0]][neighbor[1]] = distance_field[current_cell[0]][current_cell[1]] + 1

        return distance_field

    def move_humans(self, zombie_distance_field):
        """
        Function that moves humans away from zombies, diagonal moves
        are allowed
        """
        idx = 0
        for human in list(self._human_list):
            neighbors = self.eight_neighbors(human[0], human[1])
            max_distance = -1
            new_position = list(human)
            for neighbor in neighbors:
                value = zombie_distance_field[neighbor[0]][neighbor[1]]
                if max_distance < value and self.is_empty(neighbor[0], neighbor[1]) and value != 0:
                    max_distance = zombie_distance_field[neighbor[0]][neighbor[1]]
                    new_position = list(neighbor)
                self._human_list[idx] = tuple(new_position)
            idx += 1
    
    def move_zombies(self, human_distance_field):
        """
        Function that moves zombies towards humans, no diagonal moves
        are allowed
        """
        idx = 0
        for zombie in list(self._zombie_list):
            neighbors = self.four_neighbors(zombie[0], zombie[1])
            max_distance = 1200
            new_position = list(zombie)
            if human_distance_field[zombie[0]][zombie[1]] == 0:
                return
            for neighbor in neighbors:
                value = human_distance_field[neighbor[0]][neighbor[1]]
                if max_distance > value and self.is_empty(neighbor[0], neighbor[1]):
                    max_distance = value
                    new_position = list(neighbor)
                self._zombie_list[idx] = list(new_position)
            idx += 1

# Start up gui for simulation - You will need to write some code above
# before this will work without errors

poc_zombie_gui.run_gui(Apocalypse(30, 40, [], [(1,1)], [(1,1)]))
