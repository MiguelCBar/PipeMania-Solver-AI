# pipe.py: Implementação do projeto de Inteligência Artificial 2023/2024.

# Grupo 45:
# 106064 Miguel Casimiro Barbosa
# 107095 David Costa Quintino

import sys
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

    def get_value(self, row: int, col: int) -> str:
        """Devolve o valor na respetiva posição do tabuleiro."""
        return self.grid[row][col]
        

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
                aux = aux + self.get_value(i, j) + " "
            print(aux)
                

        
        return

        

    @staticmethod
    def parse_instance(file_name):
        """
        Lê o test do standard input (stdin) que é passado como argumento
        e retorna uma instância da classe Board.
        """
        rows = []
        with open(file_name, 'r') as file:
            for line in file:
                rows.append(np.array(line.split()))

        grid = np.stack(rows)
        return Board(grid)

        

    # TODO: outros metodos da classe


class PipeMania(Problem):
    def __init__(self, board: Board):
        """O construtor especifica o estado inicial."""
        # TODO
        pass

    def actions(self, state: PipeManiaState):
        """Retorna uma lista de ações que podem ser executadas a
        partir do estado passado como argumento."""
        # TODO
        pass

    def result(self, state: PipeManiaState, action):
        """Retorna o estado resultante de executar a 'action' sobre
        'state' passado como argumento. A ação a executar deve ser uma
        das presentes na lista obtida pela execução de
        self.actions(state)."""
        # TODO
        pass

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
    board.print_grid()
    # Ler o ficheiro do standard input,
    # Usar uma técnica de procura para resolver a instância,
    # Retirar a solução a partir do nó resultante,
    # Imprimir para o standard output no formato indicado.
    pass

