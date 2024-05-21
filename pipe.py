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

convert_piece = {"FC": "1000", "FB": "0010", "FE": "0001", "FD": "0100",
                  "BC": "1101", "BB": "0111", "BE": "1011", "BD": "1110",
                  "VC": "1001", "VB": "0110", "VE": "0011", "VD": "1100",
                  "LH": "0101", "LV": "1010"}


convert_piece_F = ["1000", "0100", "0010", "0001"]
convert_piece_B = ["1101", "1110", "0111", "1011"]
convert_piece_V = ["1001", "1100", "0110", "0011"]
convert_piece_L = ["0101", "1010"]

flag = {"pre_process": True}


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


    def get_value(self, row: int, col: int) -> str:
        """Devolve o valor na respetiva posição do tabuleiro e
        se a peça foi vista"""
        return self.grid[row][col]
    
    def get_piece(self, row: int, col: int) -> str:
        """Devolve o valor na respetiva posição do tabuleiro"""
        return self.grid[row][col][0:2]
    
    def set_value(self,row: int, col: int, value: str):
        self.grid[row][col] = value

    def rotate_piece(self,row: int, col: int, rotation: str):
        #C B E D, H V
        newpiece = self.get_value(row,col)[0] + rotation + '1'
        self.grid[row][col] = newpiece
        return
    

    def adjacent_vertical_values(self, row: int, col: int) -> (str, str): # type: ignore
        """Devolve os valores imediatamente acima e abaixo,
        respectivamente."""
        above_value = self.get_value(row-1,col) if row > 0 else None
        below_value = self.get_value(row+1,col) if row < self.size - 1 else None
        return above_value,below_value


    def adjacent_horizontal_values(self, row: int, col: int) -> (str, str): # type: ignore
        """Devolve os valores imediatamente à esquerda e à direita,
        respectivamente."""
        self.get_value(row,col)
        left_value = self.get_value(row, col-1) if col > 0 else None
        right_value = self.get_value(row, col+1) if col < self.size - 1 else None
        return left_value,right_value

    def get_adjacent_values(self, row: int, col: int):
        
        (cima,baixo) = self.adjacent_vertical_values(row,col)
        (esquerda,direita) = self.adjacent_horizontal_values(row,col)
        return (cima,direita,baixo,esquerda)


    def print_grid(self):
        # TODO
        
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
        return self.get_value(row,col)[2] == '1'


    def connections(self, row: int, col: int):
        
        vizinho_cima,vizinho_direita,vizinho_baixo,vizinho_esquerda = self.get_adjacent_values(row,col)
        vizinhos = (vizinho_cima,vizinho_direita,vizinho_baixo,vizinho_esquerda)
        res = [2,2,2,2] # =inicializar como desconhecido
        num_ones = 0
        piece = self.get_piece(row,col) #ver o caso de duas fontes uma contra a outra
        for i in range(4):
            if (vizinhos[i] == None) or (piece[0] == 'F' and vizinhos[i][0] == 'F'): res[i] = 0 #ve se o visinho e none
            elif vizinhos[i][2] == '0' : res[i] = 2 # vê se ainda nao foi tratado
            elif convert_piece[vizinhos[i][0:2]][(i + 2) % 4] == '1': #converte para bits e vê se o vizinho aponta para a peça
                    res [i] = 1 
                    num_ones +=1
            else: res[i] = 0 #senao nao aponta
        return (res, num_ones)
            
        
            
    


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
        connections, num_ones = self.connections(row, col)
        '''
        No connections, devolve um array de len = 4 com o seguinte formato:
            -> Se for 0, ou o adjacente é None ou foi visto e não aponta
                - CASO ESPECÍFICO: Se estivermos a tratar uma peça que seja um 
                'F', retorna 0 se o adjacente também o for
            -> Se for 1, o adjacente já foi visto e aponta para a peça
            -> Se for 2, o adjacente já foi visto, mas não aponta para a peça
        '''
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
                j+= 1

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
                j+= 1

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
                j+= 1
            return rotations

        else:   # é ligação (L)
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
                j+=1

            return rotations



    '''
    def talvez_funcione_comparisons(self, row: int, col: int):
        piece = self.get_piece(row, col)
        adjacents = self.get_adjacent_values(row, col)

        rotations = []

        keys = np.array(['C','D','B','E'])
        opposite_keys = np.array(['B','E','C','D'])
        completed = False

        if(piece[0] == 'F'):
            for i in range(4):
                if(adjacents[i] != None and adjacents[i][0] != 'F'):
                    if(completed == False and adjacents[i][2] == '1'):
                       if(convert_piece[adjacents[i][0:2]][(i + 2) % 4] == '1'):
                        rotations = ['F' + keys[i] + '1']
                        completed = True
                       else:
                           pass

                    elif(adjacents[i][2] == '0'):
                        if(completed == False):
                            rotations.append('F' + keys[i] + '1')
                        else:
                            pass
                    else:
                        return []

        elif(piece[0] == 'B'):
            indexs = []

            for i in range(4):
                if adjacents[i][2] == '1':
                    if(convert_piece[adjacents[i][0:2]][(i + 2) % 4] == '0'):
                        if(completed == False):
                            rotations = ['B' + opposite_keys[i] + '1']
                            completed = True
                        else:
                            return []
                    else:
                        if(completed == False):
                            rotations.append(['B' + keys[i] + '1'])

                    else:

                else:
                    if(completed == False):
                        rotations.append(['B' + keys[i] + '1'])

        elif(piece[0] == 'V'):

        else: #é uma ligação (L)
            binary_piece = convert_piece[piece]
            for i in range(4):
                if adjacents[i] == None:

        return rotations



    def comparisons(self, row: int, col: int):
        piece = self.get_value(row, col)

        connections= self.connections(row, col)
        index_values_2 = []
        index_values_1 = []
        index_values_0 = []

        num_zeros = 0   # 0 significa que ou o adjacente em questão é None ou não aponta para a peça
        num_ones = 0    # 1 significa que o vizinho aponta para a peça
        num_twos =  0   # 2 significa que não temos a certeza da posição do adjacente
        for index in range(len(connections)):
            if index == 0:               
                index_values_0.append(index) 
                num_zeros+=1
            elif index == 1:
                index_values_1.append(index)
                num_ones+=1 
            else: 
                index_values_2.append(index) 
                num_twos+=1

        keys = np.array(['C','D','B','E'])
        opposite_keys = np.array(['B','E','C','D'])


        if(piece[0] == 'F'):
            if num_ones == 1:    
                return ['F'+keys[index_values_1[0]]+'1']   
            
            elif(num_ones < 1 and num_zeros != 4): #no caso de duas fontes estarem adjacentes sao resolvidas no connections dando 0                 
                return ['F' + keys[item] + '1' for item in index_values_2]
        

        elif(piece[0] == 'B'):
            
            if num_zeros == 1:
                return ['B'+opposite_keys[item] + '1' for item in index_values_0]

            elif(num_zeros < 1):
                return ['B' + keys[item] + '1' for item in index_values_1+index_values_2]


        elif(piece[0] == 'V'):
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
                if num_zeros > 0 and num_zeros < 3:
                    if (index_values_0[0] == 0 or index_values_0[0] == 2) and \
                        (index_values_0[1] != 1 or index_values_0[1] != 3): return ["LH1"]
                    
                    if(0 in index_values_0 and 1 not in index_values_0): return ["LH1"]
                    else: return ["LV1"]

                elif num_ones > 0 and num_ones < 3:
                    if index_values_1[0] == 0 or index_values_1[0] == 2: return ["LV1"]
                    elif index_values_1[0] == 1 or index_values_1[0] : return ["LH1"]
                elif(num_ones == 0 and num_zeros == 0):   return ["LV1","LH1"]          
                

        return None
        '''



        

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


class PipeMania(Problem):

    def __init__(self, board: Board):
        """O construtor especifica o estado inicial."""
        self.board = board
        self.goal = self.board.size


    def actions(self, state: PipeManiaState):
        """Retorna uma lista de ações que podem ser executadas a
        partir do estado passado como argumento."""

        size = state.board.size
        altered = False
        if(flag["pre_process"] == True): 
            for row in range(size):
                for col in range(size):
                    piece_value = state.board.get_value(row, col)
                    if(piece_value[2] == '1'):
                        continue                
                    rotations = state.board.comparisons(row, col)
                    if len(rotations) == 1:
                        altered = True
                        state.board.set_value(row, col, rotations[0])
            if(altered == False):
                flag["pre_process"] = False
        return


                    
                
                
                
                    
                

                
                

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



        #perguntar sobre collections deque
        

        pieces_seen_count = 0
        board_grid = state.board.grid, board_size = state.board.size
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
                pieces_adjacent = state.board.get_adjacent_values() #definir C D B E, isto tem os valores

                for i in range(4):
                    if convert_piece[piece_value][i] == 1:
                        #falta colocar para verificar os Nones, porque caso seja um None,
                        #não é preciso comparar com nada
                        if (i == 0 and pieces_adjacent[0] != None and \
                            convert_piece[pieces_adjacent[0]][2] == 1):

                            stack_pieces.append((current_piece[0]+1, current_piece[1]))

                        
                        elif i == 1 and pieces_adjacent[i] != None and \
                            convert_piece[pieces_adjacent[i]][3] == 1:

                            stack_pieces.append((current_piece[0], current_piece[1]+1))


                        elif i == 2 and pieces_adjacent[i] != None and \
                            convert_piece[pieces_adjacent[i]][0] == 1:

                            stack_pieces.append((current_piece[0]-1, current_piece[1]))


                        elif i == 3 and pieces_adjacent[i] != None and \
                            convert_piece[pieces_adjacent[i]][1] == 1:

                            stack_pieces.append((current_piece[0], current_piece[1]-1))
                        

                        else:
                            return False
                        

                    else:
                        continue

                    


        if(pieces_seen_count < self.goal):
            return False
        return True

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
    #s0.board.print_grid()
    while(flag["pre_process"]):
        problem.actions(s0)
    s0.board.print_grid()

    # Ler o ficheiro do standard input,
    # Usar uma técnica de procura para resolver a instância,
    # Retirar a solução a partir do nó resultante,
    # Imprimir para o standard output no formato indicado.
    pass

