# pipe.py: Implementação do projeto de Inteligência Artificial 2023/2024.

# Grupo 45:
# 106064 Miguel Casimiro Barbosa
# 107095 David Costa Quintino

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



class PipeManiaState:
    state_id = 0

    def __init__(self, board):
        self.board = board
        self.id = PipeManiaState.state_id
        PipeManiaState.state_id += 1

    def __lt__(self, other):
        return self.id < other.id

    # TODO: outros metodos da classe


class Board:
    """Representação interna de um tabuleiro de PipeMania."""
    def __init__(self, grid):
        self.grid = grid
        self.size = len(grid)

    def is_F(self, row: int, col: int) -> bool:
        return self.grid(row, col)[0] == 'F'

    def is_B(self, row: int, col: int) -> bool:
        return self.grid(row, col)[0] == 'B'

    def is_V(self, row: int, col: int) -> bool: 
        return self.grid(row, col)[0] == 'V'
        
    def is_L(self, row: int, col: int) -> bool:
        return self.grid(row, col)[0] == 'L'      


    def get_value(self, row: int, col: int) -> str:
        """Devolve o valor na respetiva posição do tabuleiro."""
        return self.grid[row][col]
    
    def set_value(self,row: int, col: int, value: int):
        self.grid[row][col][1] = value

    def rotate_piece(self,row: int, col: int, rotation: int):
        #C B E D, H V
        newpiece = self.get_value(row,col)[0] + rotation + '1'
        self.grid[row][col] = newpiece
        return

    def adjacent_vertical_values(self, row: int, col: int) -> (str, str): # type: ignore
        """Devolve os valores imediatamente acima e abaixo,
        respectivamente."""
        above_value = self.grid[row - 1][col] if row > 0 else None
        below_value = self.grid[row + 1][col] if row < self.size else None
        return above_value,below_value


    def adjacent_horizontal_values(self, row: int, col: int) -> (str, str): # type: ignore
        """Devolve os valores imediatamente à esquerda e à direita,
        respectivamente."""
        left_value = self.grid[row][col - 1] if col > 0 else None
        right_value = self.grid[row][col + 1] if col < self.size else None
        return left_value,right_value

    def print_grid(self):
        # TODO
        
        for i in range(self.size):
            aux = "" 
            for j in range(self.size):
                aux = aux + self.get_value(i, j)[:2] + " "
            print(aux)
        return
    


    def correct_border_pieces(self): 

        if(self.is_V(0, 0)):
            self.grid(0,0)[1] = 'B'

        if(self.is_V(0, self.size)):
            self.grid(0,0)[1] = 'E'

        if(self.is_V(self.size, self.size)):
            self.grid(0,0)[1] = 'C'

        if(self.is_V(self.size, 0)):
            self.grid(0,0)[1] = 'D'


        for col in range(1, self.size - 1):
            if(self.is_L(0, col)):
                self.grid(0, col)[1] = 'H'
            elif(self.is_B(0, col)):
                self.grid(0, col)[1] = 'B'
            
            if(self.is_L(self.size, col)):
                self.grid(self.size,col)[1] = 'H'
            elif(self.is_B(self.size, col)):
                self.grid(self.size, col)[1] = 'C'
            
            
            
        for row in range(1, self.size - 1):
            if(self.is_L(row,0)):
                self.grid(row,0)[1] = 'V'
                self.grid(row,0)[2] = '1' 
            elif(self.is_B(row,0)):
                self.grid(row,0)[1] = 'D' 
                self.grid(row,0)[2] = '1'
            if(self.is_L(row,self.size)):
                self.grid(row,self.size)[1] = 'V' 
                self.grid(row,0)[2] = '1'
            elif(self.is_B(row,self.size)):
                self.grid(row,self.size)[1] = 'E'



    def comparisons(self, row: int, col: int):
        piece = self.get_value(row, col)
        if(piece[2] == '1'):
            return
        above_piece, below_piece = self.adjacent_vertical_values(row, col)
        left_piece, right_piece = self.adjacent_horizontal_values(row, col)


        if(piece[0] == 'F'):
            if(above_piece == None and left_piece == None):
                if
                
                

        elif(piece[0] == 'B'):


        elif(piece[0] == 'V'):


        else: # é ligação, L


        




        

    @staticmethod
    def parse_instance(file_name):
        """
        Lê o test do standard input (stdin) que é passado como argumento
        e retorna uma instância da classe Board.
        """

        rows = []
        with open(file_name, 'r') as file:
            for line in file:
                rows.append(np.array([i + '0' for i in line.split()]))
                

        grid = np.stack(rows)
        return Board(grid)

        

    # TODO: outros metodos da classe


class PipeMania(Problem):

    def __init__(self, board: Board):
        """O construtor especifica o estado inicial."""
        self.board = board
        # TODO
        pass

    def actions(self, state: PipeManiaState):
        """Retorna uma lista de ações que podem ser executadas a
        partir do estado passado como argumento."""
        # TODO
        pass

    def result(self, state: PipeManiaState, action) -> PipeManiaState:
        """Retorna o estado resultante de executar a 'action' sobre
        'state' passado como argumento. A ação a executar deve ser uma
        das presentes na lista obtida pela execução de
        self.actions(state)."""
        # TODO
        #action(row,col, orientation )
        newstate = PipeManiaState(state.board) # prolly n copia ptt depois fzr copia a serio
        newstate.board.rotate_piece(action[0],action[1],action[2])

        return(newstate)

    def goal_test(self, state: PipeManiaState):
        """Retorna True se e só se o estado passado como argumento é
        um estado objetivo. Deve verificar se todas as posições do tabuleiro
        estão preenchidas de acordo com as regras do problema."""
        # TODO
        
        pass

    def h(self, node: Node):
        """Função heuristica utilizada para a procura A*."""
        # TODO
        pass

    # TODO: outros metodos da classe


if __name__ == "__main__":
    # TODO:

    if len(sys.argv) != 2:
        print("Usage: python pipe_mania.py input_file.txt")
        sys.exit(1)

    input_file = sys.argv[1]
    board = Board.parse_instance(input_file)
    
    problem = PipeMania(board)

    s0 = PipeManiaState(board)
    s0.board.print_grid()
    s1 = problem.result(s0, (2,2,'D'))
    s1.board.print_grid()

    # Ler o ficheiro do standard input,
    # Usar uma técnica de procura para resolver a instância,
    # Retirar a solução a partir do nó resultante,
    # Imprimir para o standard output no formato indicado.
    pass

