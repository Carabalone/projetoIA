# takuzu.py: Template para implementação do projeto de Inteligência Artificial 2021/2022.
# Devem alterar as classes e funções neste ficheiro de acordo com as instruções do enunciado.
# Além das funções e classes já definidas, podem acrescentar outras que considerem pertinentes.

# Grupo 00:
# 00000 Nome1
# 00000 Nome2

from copy import deepcopy
import sys
import math

import numpy
from search import (
    Problem,
    Node,
    astar_search,
    breadth_first_tree_search,
    depth_first_tree_search,
    greedy_search,
    recursive_best_first_search,
)


class TakuzuState:
    state_id = 0

    def __init__(self, board):
        self.board = board
        self.id = TakuzuState.state_id
        TakuzuState.state_id += 1

    def __lt__(self, other):
        return self.id < other.id

    # TODO: outros metodos da classe


class Board:
    """Representação interna de um tabuleiro de Takuzu."""
    def __init__(self, board: tuple):
        self.board = board
        self.len = len(board)
    
    def get_number(self, row: int, col: int) -> int:
        """Devolve o valor na respetiva posição do tabuleiro."""
        return self.board[row][col]
    
    def adjacent_vertical_numbers(self, row: int, col: int) -> (int, int):
        """Devolve os valores imediatamente abaixo e acima,
        respectivamente."""
        lines = self.len
        if row == 1:
            return self.board[row + 1][col], None
        elif row == lines:
            return None, self.board[row - 1][col]
        return self.board[row + 1][col], self.board[row - 1][col]

    def adjacent_horizontal_numbers(self, row: int, col: int) -> (int, int):
        """Devolve os valores imediatamente à esquerda e à direita,
        respectivamente."""
        cols = self.len
        if col == 1:
            return None, self.board[row][col + 1]
        elif col == cols:
            return self.board[row][col - 1], None
        return self.board[row][col - 1], self.board[row][col + 1]

    @staticmethod
    def parse_instance_from_stdin():
        """Lê o test do standard input (stdin) que é passado como argumento
        e retorna uma instância da classe Board.

        Por exemplo:
            $ python3 takuzu.py < input_T01

            > from sys import stdin
            > stdin.readline()
        """
        # TODO

        #not ready yet
        read = sys.stdin.read()
        board = [[] for x in range(int(read.split("\n")[0]))]
        for index, line in enumerate(read.split('\n')[1:-1]):
            board[index] += [int(x) for x in line.split('\t')]
        return Board(tuple(board))

    def __str__(self):
        string = ""
        for row in self.board:
            for element in row:
                string += str(element) + '\t'
            string += '\n'
        return string
    # TODO: outros metodos da classe
    
    def check_lines(self):
        u, c = numpy.unique(board.board, axis=0, return_counts=True)
        return (c>1).any()
    
    def check_cols(self):
        u, c = numpy.unique(board.board, axis=1, return_counts=True)
        return (c>1).any()
    
    def check_row_and_col(self):
        for i in range(board.len):  # generate pairs
            for j in range(i + 1, board.len): 
                if numpy.array_equal(board.board[i], board.board[j]):  # compare rows
                    if numpy.array_equal(board.board[:,i], board.board[:,j]):  # compare columns
                        return False
        return True

    def check_adjacent(self):
        for line in self.board:
            for i in range(self.len - 2):
                if (line[i]==1 or line[i] == 2) and line[i] == line[i + 1] == line[i + 2]:
                    return False
        for line in range(self.len):
            for i in range(self.len - 2):
                if (self.board[line][i]==1 or self.board[line][i] == 2) and\
                     self.board[line][i] == self.board[line][i + 1] == self.board[line][i + 2]:
                    return False
        return True
        
    def check_zero_one(self, full=True):
        board = numpy.matrix(self.board)
        n = board[0].size
        
        if (full):
            for row in board:
                zeros, ones = numpy.where(row==0)[0].size, numpy.where(row==1)[0].size
                if (n%2 == 0 and zeros != ones) or (n%2 != 0 and abs(zeros-ones != 1)):
                    return False
        
            for col in board.T:
                zeros, ones = numpy.where(col==0)[0].size, numpy.where(col==1)[0].size
                if (n%2 == 0 and zeros != ones) or (n%2 != 0 and abs(zeros-ones != 1)):
                    return False
        else:
            for row in board:
                zeros, ones = numpy.where(row==0)[0].size, numpy.where(row==1)[0].size
                #print(f"row: {row}, zeros {zeros}, ones {ones}")
                if (n%2 == 0 and (zeros > n//2 or ones > n//2)):
                    return False
        
            for col in board.T:
                zeros, ones = numpy.where(col==0)[0].size, numpy.where(col==1)[0].size
                #print(f"col: {col}, zeros {zeros}, ones {ones}")
                if ((zeros > math.ceil(n/2) or ones > math.ceil(n/2))):
                    return False
            
        return True

    def generate_possibilities(self):
        result = numpy.argwhere(numpy.array(board.board) == 2)
        actions = [(x[0], x[1], y) for y in (0,1) for x in result]
        return actions

class Takuzu(Problem):
    def __init__(self, board: Board):
        """O construtor especifica o estado inicial."""
        self.initial = board

    def actions(self, state: TakuzuState):
        """Retorna uma lista de ações que podem ser executadas a
        partir do estado passado como argumento."""
        actions = state.board.generate_possibilities()
        print(f"actions before patch: \n{actions}")
        actions = self.patch_illegal(state, actions)
        return actions

    def result(self, state: TakuzuState, action):
        """Retorna o estado resultante de executar a 'action' sobre
        'state' passado como argumento. A ação a executar deve ser uma
        das presentes na lista obtida pela execução de
        self.actions(state)."""
        row, col, val = action[0], action[1], action[2]
        result_board = deepcopy(state.board.board)
        result_board[row][col] = val
        return TakuzuState(Board(result_board))

    def goal_test(self, state: TakuzuState):
        """Retorna True se e só se o estado passado como argumento é
        um estado objetivo. Deve verificar se todas as posições do tabuleiro
        estão preenchidas com uma sequência de números adjacentes."""
        board = state.board
        return 2 not in state.board.board and board.check_row_and_col \
            and board.check_zero_one() and board.check_adjacent()

    def h(self, node: Node):
        """Função heuristica utilizada para a procura A*."""
        # TODO
        pass
    
    def patch_illegal(self, state: TakuzuState, arr: list):
        """Given a list containing actions, it removes the illegal moves."""
        arr = list(arr)
        for action in arr:
            res = self.result(state, action)
            board_res = res.board
            #print(board_res, action)
            #print(f"check_zero_one: {board_res.check_zero_one(full=False)}, check_col {board_res.check_row_and_col()}")
            if (not (board_res.check_zero_one(full=False) and board_res.check_row_and_col())):
                #print("entrou")
                arr.remove(action)

        return arr
    # TODO: outros metodos da classe


if __name__ == "__main__":
    # TODO:
    # Ler o ficheiro de input de sys.argv[1],
    # Usar uma técnica de procura para resolver a instância,
    # Retirar a solução a partir do nó resultante,
    # Imprimir para o standard output no formato indicado.
    board = Board.parse_instance_from_stdin()
    takuzu = Takuzu(board)
    state = TakuzuState(board)

    print("Board:")
    print(state.board)
    print(f"actions after patch: \n{takuzu.actions(state)}")
