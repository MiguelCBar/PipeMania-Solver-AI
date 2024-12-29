import sys

import copy
import numpy as np
from search import (
    Problem,
    Node,
    astar_search,
    breadth_first_tree_search,
    depth_first_tree_search,
    greedy_search,
    recursive_best_first_search,
)

convert_piece = {"FC": "1000", "FB": "0010", "FE": "0001", "FD": "0100",
                  "BC": "1101", "BB": "0111", "BE": "1011", "BD": "1110",
                  "VC": "1001", "VB": "0110", "VE": "0011", "VD": "1100",
                  "LH": "0101", "LV": "1010"}


convert_piece_F = ["1000", "0100", "0010", "0001"]
convert_piece_B = ["1101", "1110", "0111", "1011"]
convert_piece_V = ["1001", "1100", "0110", "0011"]
convert_piece_L = ["0101", "1010"]


class PipeManiaState:
    state_id = 0

    def __init__(self, board):
        self.board = board
        self.id = PipeManiaState.state_id
        PipeManiaState.state_id += 1

    def __lt__(self, other):
        return self.id < other.id

    # TODO: Other methods for this class


class Board:
    """Internal representation of a PipeMania board."""
    def __init__(self, grid):
        self.grid = grid
        self.size = len(grid) 


    def get_value(self, row: int, col: int) -> str:
        """Returns the value at the respective position on the board."""
        return self.grid[row][col]
    

    def get_piece(self, row: int, col: int) -> str:
        """Returns the piece at the respective position on the board."""
        return self.grid[row][col][0:2]
    

    def set_value(self,row: int, col: int, value: str):
        """Sets the value at the respective position on the board."""
        self.grid[row][col] = value
    

    def adjacent_vertical_values(self, row: int, col: int) -> (str, str): # type: ignore
        """Returns the values immediately above and below the specified position."""
        above_value = self.get_value(row-1,col) if row > 0 else None
        below_value = self.get_value(row+1,col) if row < self.size - 1 else None
        return above_value,below_value


    def adjacent_horizontal_values(self, row: int, col: int) -> (str, str): # type: ignore
        """Returns the values immediately to the left and right of the specified position."""
        self.get_value(row,col)
        left_value = self.get_value(row, col-1) if col > 0 else None
        right_value = self.get_value(row, col+1) if col < self.size - 1 else None
        return left_value,right_value


    def get_adjacent_values(self, row: int, col: int):
        """Returns all adjacent values (top, right, bottom, left)."""
        (top, bottom) = self.adjacent_vertical_values(row, col)
        (left, right) = self.adjacent_horizontal_values(row, col)
        return (top, right, bottom, left)


    def print_grid(self):
        """Prints the board grid."""
        for i in range(self.size):
            aux = "" 
            for j in range(self.size):
                if(j == self.size - 1):
                    aux = aux + self.get_value(i, j)[:2]
                else:
                    aux = aux + self.get_value(i, j)[:2] + "\t"
            print(aux)
        return
    
    

    def piece_corrected(self, row: int,  col: int): 
        """Checks if a piece has been processed correctly."""
        return self.get_value(row,col)[2] == '1'


    def connections(self, row: int, col: int):
        """Checks connections for the piece at the specified position."""
        neighbor_top, neighbor_right, neighbor_bottom, neighbor_left = self.get_adjacent_values(row, col)
        neighbors = (neighbor_top, neighbor_right, neighbor_bottom, neighbor_left)
        res = [2, 2, 2, 2]  # Initialize as unknown
        num_ones = 0
        piece = self.get_piece(row, col)
        for i in range(4):
            if (neighbors[i] == None) or (piece[0] == 'F' and neighbors[i][0] == 'F'):
                res[i] = 0  # Neighbor is None or an invalid connection for F
            elif neighbors[i][2] == '0':
                res[i] = 2  # Neighbor not yet processed
            elif convert_piece[neighbors[i][0:2]][(i + 2) % 4] == '1':  # Valid connection
                res[i] = 1 
                num_ones += 1
            else:
                res[i] = 0  # Invalid connection
        return (res, num_ones)


    def comparisons(self, row: int, col: int):
        """Determines possible rotations for the piece at the specified position."""
        piece = self.get_value(row, col)
        connections, num_ones = self.connections(row, col)

        rotations = []
        possible_piece = True
        keys = ['C','D','B','E']
        keys_L = ['H', 'V']

        j = 0
        if(piece[0] == 'F'):
            if(num_ones > 1):
                return rotations
            for binary_piece in convert_piece_F:
                possible_piece = True
                for i in range(4):
                    if (binary_piece[i] == '1' and connections[i] == 0) or (binary_piece[i] == '0' and connections[i] == 1):
                        possible_piece = False
                        break
                
                if possible_piece:
                    rotations.append('F' + keys[j] + '1')
                j += 1

            return rotations

        elif(piece[0] == 'B'):
            if(num_ones > 3):
                return rotations
            for binary_piece in convert_piece_B:
                possible_piece = True
                
                for i in range(4):
                    if (binary_piece[i] == '1' and connections[i] == 0) or (binary_piece[i] == '0' and connections[i] == 1):
                        possible_piece = False
                        break
                
                if possible_piece:
                    rotations.append('B' + keys[j] + '1')
                j += 1

            return rotations

        elif(piece[0] == 'V'):
            if(num_ones > 2):
                return rotations
            for binary_piece in convert_piece_V:
                possible_piece = True
                for i in range(4):
                    if (binary_piece[i] == '1' and connections[i] == 0) or (binary_piece[i] == '0' and connections[i] == 1):
                        possible_piece = False
                        break
                
                if possible_piece:
                    rotations.append('V' + keys[j] + '1')
                j += 1
            return rotations

        else:   # It is a connection piece (L)
            if(num_ones > 2):
                return rotations
            for binary_piece in convert_piece_L:
                possible_piece = True
                for i in range(4):
                    if (binary_piece[i] == '1' and connections[i] == 0) or (binary_piece[i] == '0' and connections[i] == 1):
                        possible_piece = False
                        break
                
                if possible_piece:
                    rotations.append('L' + keys_L[j] + '1')
                j += 1

            return rotations
    
    def pre_process(self):
        """
        Performs initial operations on the board.
        """
        size = self.size
        altered = False
        for row in range(size):
            for col in range(size):
                piece_value = self.get_value(row, col)
                if(piece_value[2] == '1'):
                    continue                
                rotations = self.comparisons(row, col)
                if len(rotations) == 1:
                    altered = True
                    self.set_value(row, col, rotations[0])
        return altered
    
    @staticmethod
    def parse_instance():
        """
        Reads the input from standard input (stdin) and returns an instance of the Board class.
        """
        rows = []
        line = input()
        rows.append(np.array([i + '0' for i in line.split()]))
        for i in range(len(line.split()) - 1):
            line = input()
            rows.append(np.array([i + '0' for i in line.split()]))
        
        grid = np.array(rows)
        board = Board(grid)
        while(board.pre_process()):
            continue

        return board

class PipeMania(Problem):

    def __init__(self, board: Board):
        """Constructor specifies the initial state."""
        self.initial = PipeManiaState(board)
        self.goal = board.size ** 2


    def actions(self, state: PipeManiaState):
        """Returns a list of actions that can be executed from the given state."""
        
        actions = []
        best_action = 5
        size = state.board.size
        for row in range(size):
            for col in range(size):
                piece_value = state.board.get_value(row, col)
                if(piece_value[2] == 1):
                    continue
                rotations = state.board.comparisons(row, col)
                number_actions = len(rotations)
                if number_actions == 0:
                    return []
                
                elif number_actions == 1:
                    state.board.set_value(row, col, rotations[0])

                elif(best_action > number_actions):
                    actions = [(row, col, i) for i in rotations]
                    best_action = number_actions
        return actions

                
    def result(self, state: PipeManiaState, action) -> PipeManiaState:
        """Returns the resulting state after executing the given action on the given state."""
        copied_board = copy.deepcopy(state.board)

        copied_board.set_value(action[0], action[1], action[2])
        new_state = PipeManiaState(copied_board)
        return new_state                    


    def goal_test(self, state: PipeManiaState):
        """Returns True if and only if the given state is a goal state.
        Checks if all board positions are filled according to the problem rules.
        """        
        pieces_seen_count = 0
        seen_pieces = set()
        stack_pieces = []
        stack_pieces.append((0, 0))
        while stack_pieces:
            current_piece = stack_pieces.pop()
            if current_piece in seen_pieces:
                continue
            else:
                pieces_seen_count +=1
                seen_pieces.add((current_piece[0], current_piece[1]))
                piece_value = state.board.get_piece(current_piece[0], current_piece[1])
                pieces_adjacent = state.board.get_adjacent_values(current_piece[0], current_piece[1]) # Define connections

                adjacents_position = [(current_piece[0] - 1, current_piece[1]),
                                      (current_piece[0], current_piece[1] + 1),
                                      (current_piece[0] + 1, current_piece[1]),
                                      (current_piece[0], current_piece[1] - 1)]

                connected = 0

                for i in range(4):
                    if convert_piece[piece_value][i] == '1':
                        if(pieces_adjacent[i] != None and \
                           convert_piece[pieces_adjacent[i][0:2]][(i + 2) % 4] == '1'):
                            connected = 1
                            stack_pieces.append((adjacents_position[i][0], adjacents_position[i][1]))
                        
                        elif(i == 3 and connected == 0):
                            return False

                        
                    else:
                        continue
        if(pieces_seen_count < self.goal):
            return False
        return True

    def h(self, node: Node):
        """Heuristic function used for A* search."""
        # TODO
        pass


if __name__ == "__main__":
    # TODO:

    board = Board.parse_instance()
    
    problem = PipeMania(board)
    goal_node = depth_first_tree_search(problem)
    goal_node.state.board.print_grid()

    # Read the file from standard input,
    # Use a search technique to solve the instance,
    # Extract the solution from the resulting node,
    # Print to standard output in the specified format.
