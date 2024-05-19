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

point_up = ["BC","BE","BD","VC","VD","LV","FC"]
point_down = ["BB","BE","BD","VE","VB","LV","FB"]
point_left = ["BC","BB","BD","VC","VE","LH","FE"]
point_right = ["BC","BB","BE","VB","VD","LH","FD"]

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

    def rotate_piece(self,row: int, col: int, rotation: str):
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
        elif cima_neighbor[2] == '0': return 2
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
        index_values_2 = []
        index_values_1 = []
        index_values_0 = []

        num_zeros = 0
        num_ones = 0
        num_twos =  0
        for item in connections:
            if item == 0: 
                index_values_0.append(item) 
                num_zeros+=1
            elif item == 1:
                index_values_1.append(item)
                num_ones+=1 
            else: 
                index_values_2.append(item) 
                num_twos+=1

                        
        num_zeros = len(index_values_0)
        num_ones = len(index_values_1)
        num_twos = len(index_values_2)
        keys = np.array(['C','D','B','E'])
        opposite_keys = np.array(['B','E','C','D'])

        if(piece[0] == 'F'):
            if num_ones == 1:
                """feito, creio"""
                return ['F'+keys[item]+'1' for item in index_values_1]    
            elif num_zeros > 0:
                return ['F' + keys[item] + '1' for item in index_values_2]
            else:
                return["FC1","FD1","FB1","FE1"]


        elif(piece[0] == 'B'):
            """feito, creio"""
            if num_zeros == 1:
                return ['B'+opposite_keys[item] +'1' for item in index_values_0]

            elif num_ones > 0:
                return ['B' + keys[item] + '1' for item in index_values_1+index_values_2]
            else:
                return["BC1","BD1","BB1","BE1"]
        

        elif(piece[0] == 'V'):
            #TODO
            if num_ones == 2: #se tem 2 pecas a apontarem lhe
                if index_values_1[0] == 0 and index_values_1 [1] == 3: #e preciso caso especifico porque os numeros nao tem diferença de 1
                    return  ["VC1"]
                else:
                    return 'V' + keys[index_values_1[1]] + '1'
            elif num_zeros == 2: #se tem duas pecas 
                if index_values_0[0] == 0 and index_values_0 [1] == 3:
                    return ["VB1"]
                else:
                    return 'V' + opposite_keys[index_values_0[1]] + '1'
            elif num_zeros == 1 and num_ones == 1:
                if(index_values_0[0] + index_values_1[0]) % 2 == 0: #se os valores forem opostos ha duas hipoteses
                    return ['V' + keys[index_values_1[0]] + '1', 'V' + keys[index_values_1[0] -1 ] + '1']
                elif index_values_0[0] == (index_values_1[0] + 1) % 4:
                    return ['V' + keys[index_values_1[0]] + '1']
                elif index_values_0[0] == (index_values_1[0] - 1) % 4:
                    return ['V' + keys[index_values_1[0] - 1] + '1']
            elif num_zeros == 0 and num_ones == 1: #neste ponto so ha um conected, duas hipoteses    
                indexes = [index_values_1[0], (index_values_1[0] + 1)%4]
                return ['V' + keys[item] + '1' for item in indexes]
            elif num_zeros == 1 and num_ones == 0: #
                indexes =[(index_values_0[0] + 2) % 4 , (index_values_0[0] + 3) % 4]
                return ['V' + keys[item] + '1' for item in indexes]            
            else:
                return["VC1","VD1","VB1","VE1"]

        else: # é ligação, L
            #ver quais ligam
            if num_zeros > 0:
                if index_values_0[0] == 0 or index_values_0[0] ==2: return "LH1"
                else: return ["LV1"]
            elif num_ones > 0:
                if index_values_1[0] == 0 or index_values_1[0] ==2: return "LV1"
                else: return ["LH1"]
            else:   return ["LV1","LH1"]          
          

    




        

    @staticmethod
    def parse_instance(file_name):
        """
        Lê o test do standard input (stdin) que é passado como argumento
        e retorna uma instância da classe Board.
        """

        rows = []
        with open(file_name, 'r') as file:
            for line in file:
                rows.append(np.array([i + '00' for i in line.split()]))
                

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

        dfs_max_depth = 0
        
        state.board = copy.deepcopy(self.board)
        stack = [(0,0), 0] # the position and depth of the piece
        while stack:
            row, col, depth = stack.pop()
            value = state.board.get_value(row,col)
            if value[3] != '1':
                state.board[row][col][3] = '1'
                dfs_max_depth = max(dfs_max_depth, depth)
                above_value, below_value = state.board.adjaceWnt_vertical_values(row, col)
                right_value, left_value = state.board.adjacent_horizontal_values(row, col)

                if(value[0] == 'F'):
                    if(value[1] == 'C'):
                        if (above_value != None and np.isin(above_value[0:2], point_down)):
                            #lista para saber os que estão ligados por cima


                    elif(value[1] == 'B'):
                        if (below_value != None and np.isin(below_value[0:2], point_up)):
                            #lista para saber os que estão ligados por baixo

                    elif(value[1] == 'E'):
                        if(left_value != None and np.isin(left_value[0:2], point_right)):
                            #lista para saber os que estão ligados pela esquerda


                    else: # é direita D
                        
                        if(right_value != None and np.isin(right_value[0:2], point_left)):
                            #lista para saber os que estão ligados pela direita


                elif(value[0] == 'B'):
                    if(value[1] == 'C' or value[1] == 'B' or value[1] == 'E'):
                        if(left_value != None and np.isin(left_value[0:2], point_right)):

                    if(value[1] == 'C' or value[1] == 'E' or value[1] == 'D'):
                        if(above_value != None and np.isin(above_value[0:2], point_down)):
                    
                    if(value[1] == 'C' or value[1] == 'B' or value[1] == 'D'):
                        if(right_value != None and np.isin(right_value[0:2], point_left)):

                    if(value[1] == 'B' or value[1] == 'E' or value[1] == 'D'):
                        if(below_value != None and np.isin(below_value[0:2], point_up)):

                         

                elif(value[0] == 'V'):
                    if(value[1] == 'C' or value[1] == 'D'):
                        if(above_value != None and np.isin(above_value[0:2], point_down)):
                        
                    if(value[1] == 'B' or value[1] == 'D'):
                        if(right_value != None and np.isin(right_value[0:2], point_left)):

                    if(value[1] == 'B' or value[1] == 'E'):
                        if(below_value != None and np.isin(below_value[0:2], point_up)):

                    if(value[1] == 'C' or value[1] == 'E'):
                        if(left_value != None and np.isin(left_value[0:2], point_right)):

                else: # é ligação L
                    if(value[1] == 'H'):
                        if(above_value != None and np.isin(above_value[0:2], point_down)):
                        
                        if(below_value != None and np.isin(below_value[0:2], point_up)):
                        
                    elif(value[1] == 'V'):

                        if(right_value != None and np.isin(right_value[0:2], point_left)):

                        if(left_value != None and np.isin(left_value[0:2], point_right)):







        '''
        conditions:
        --- para sabermos se as peças adjacentes estão corretamente 
        colocadas, testamos com as listas que criámos

        --- ao passarmos para um novo node, colocamos as peças adjacentes
        ligadas dentro da Stack

        --- sempre que passamos para um novo node, verificamos se a
        current_height > max_height, se sim, atualizamos

        --- caso não seja possível andar mais porque não estão corretamente
        ligadas, paramos e goal_test = False

        --- caso cheguemos a uma fonte/node que já visitámos, continuamos só

        --- IMPORTANTE -> caso a DFS acabe e max_height < goal_test, significa
        que temos um mini ciclo dentro do board, por isso goal_test = False
            NÃO SEI SE É POSSÍVEL FAZER, MAS NESTE ÚLTIMO CASO, DEVIAS LOGO DIZER QUE
            ESTÁS NO CAMINHO ERRADO, OU SEJA, CAGAS NESTA RAMIFICAÇÃO

        '''










        
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

