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
        above_value = self.get_value(row-1,col) if row > 0 else None
        below_value = self.get_value(row+1,col) if row < self.size else None
        return above_value,below_value


    def adjacent_horizontal_values(self, row: int, col: int) -> (str, str): # type: ignore
        """Devolve os valores imediatamente à esquerda e à direita,
        respectivamente."""
        self.get_value(row,col)
        left_value = self.get_value(row,col-1) if col > 0 else None
        right_value = self.get_value(row,col+1) if col < self.size else None
        return left_value,right_value

    def print_grid(self):
        # TODO
        
        for i in range(self.size):
            aux = "" 
            for j in range(self.size):
                aux = aux + self.get_value(i, j)[:2] + " "
            print(aux)
        return
    
    def piece_corrected(self, row: int,  col: int): 
        return self.get_value(self, row,col)[2] == '1'

    """ Ve se a peca em cima da dada esta conectada ou nao. 
    Devolve 0 se nao tiver, 1 se tiver e 2 se for inconclusivo  """
    def connected_cima(self, row: int, col: int):  
        connected_pieces = np.array(["BC","BE","BD","VC","VD","LV","FC"])#verificar
        piece = self.get_value(row, col)
        cima_neighbor = self.adjacent_vertical_values(row, col)[0] # maybe errado
        if cima_neighbor== None: return 0
        elif piece[2] == '0': return 2
        elif np.isin(piece,connected_pieces): return 1
        else: return 0

    """ Ve se a peca a baixo da dada esta conectada ou nao. 
    Devolve 0 se nao tiver, 1 se tiver e 2 se for inconclusivo  """
    def connected_baixo(self, row: int, col: int):  
        connected_pieces = np.array(["BB","BE","BD","VE","VB","LV","FB"])#verificar
        piece = self.get_value(row, col)
        baixo_neighbor = self.adjacent_vertical_values(row, col)[1] # maybe errado
        if baixo_neighbor== None: return 0
        elif piece[2] == '0': return 2
        elif np.isin(piece,connected_pieces): return 1
        else: return 0
   
    """ Ve se a peca a esquerda da dada esta conectada ou nao. 
    Devolve 0 se nao tiver, 1 se tiver e 2 se for inconclusivo  """
    def connected_esq(self, row: int, col: int):  
        connected_pieces = np.array(["BC","BB","BD","VC","VE","LH","FE"]) #verificar
        piece = self.get_value(row, col)
        cima_neighbor = self.adjacent_horizontal_values(row, col)[0] # maybe errado
        if cima_neighbor== None: return 0
        elif piece[2] == '0': return 2
        elif np.isin(piece,connected_pieces): return 1
        else: return 0


    """ Ve se a peca a direita da dada esta conectada ou nao. 
    Devolve 0 se nao tiver, 1 se tiver e 2 se for inconclusivo  """
    def connected_dir(self, row: int, col: int):  
        connected_pieces = np.array(["BC","BB","BE","VB","VD","LH","FD"]) #verificar
        piece = self.get_value(row, col)
        cima_neighbor = self.adjacent_horizontal_values(row, col)[1] # maybe errado
        if cima_neighbor== None: return 0
        elif piece[2] == '0': return 2
        elif np.isin(piece,connected_pieces): return 1
        else: return 0


    


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


    """devolve as possiveis orientacoes da peca com base nos seus vizinhos
        nao altera a peça"""
    def comparisons(self, row: int, col: int):
        piece = self.get_value(row, col)
        if(piece[2] == '1'):
            return [piece]

        connections= np.array([self.connected_cima(row,col),self.connected_dir(row,col),
                              self.connected_baixo(row,col),self.connected_esq(row,col)])
        keys = np.array(['C','D','B','E'])
        opposite_keys = np.array(['B','E'])
        dict = dict(zip(keys, connections))
        if(piece[0] == 'F'):
            if np.count_nonzero(connections = 1) == 1:
                """mudar esta merda pa lista o dict  n vale a pena"""
                key_with_value_1 = [key for key, value in dict.items() if value == 1]
                return ['F'+key_with_value_1+'1']    
            elif np.count_nonzero(connections = 0) > 0:
                keys_with_value_0 = [key for key, value in dict.items() if value == 0]

                return np.setdiff1d(keys,keys_with_value_0)
            else:
                return["FC1","FD1","FB1","FE1"]


        elif(piece[0] == 'B'):
            """"maybe desnecessaario esta cena de cima logo se ve"""
            if np.count_nonzero(connections = 0) == 1:
                index_value_0 = connections.index(0)
                return ['B'+opposite_keys[index_value_0+'1']]

            elif np.count_nonzero(connections = 1) > 0:
                index_values1 = np.where(connections == 1)[0]
                return np.setdiff1d(keys,index_values1)
            else:
                return["BC1","BD1","BB1","BE1"]
        

        elif(piece[0] == 'V'):
            #TODO
            return

        else: # é ligação, L
            #ver quais ligam
            index_values1 = np.where(connections = 1)[0]
            if(len(index_values1) != 0 ):
                if np.isin(index_values1,0) or np.isin(index_values0,2): return "LV1"
                else: return "LH1"

            index_values0 = np.where(connections = 0)[0]
            if(len(index_value_0)!=0):
                if np.isin(index_value_0,0) or np.isin(index_value_0,2): return "LH1"
                else: return "LV1"
            
            return ["LV1","LH1"]

    




        

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
        self.goal = self.board.size


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

        dfs_nodes_count = 0
        
        
        return False

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

