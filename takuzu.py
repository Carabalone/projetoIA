# takuzu.py: Template para implementação do projeto de Inteligência Artificial 2021/2022.
# Devem alterar as classes e funções neste ficheiro de acordo com as instruções do enunciado.
# Além das funções e classes já definidas, podem acrescentar outras que considerem pertinentes.

# Grupo 00:
# 00000 Nome1
# 00000 Nome2

import sys

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
        #print("read " + read + " from stdin")
        board = [[] for x in range(int(read.split("\n")[0]))]
        #print(read.split("\n"))
        #print(read.split('\n')[1:-1])
        for index, line in enumerate(read.split('\n')[1:-1]):
            #print(index, line.split('\t'))
            board[index] += [int(x) for x in line.split('\t')]
        return Board(tuple(board))

    def __str__(self):
        #print(self.board)
        string = ""
        for row in self.board:
            for element in row:
                string += str(element) + '\t'
            string += '\n'
        return string
    # TODO: outros metodos da classe
    
    def check_lines(self):
        board = numpy.transpose(self.board)
        u, c = numpy.unique(board, axis=0, return_counts=True)
        return (c>1).any()
    
    def check_cols(self):
        board = numpy.transpose(self.board)
        u, c = numpy.unique(board, axis=1, return_counts=True)
        return (c>1).any()
    
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
        
    def check_zero_one(self):
        count, board = {}, numpy.matrix(self.board)
        n = board[0].size
        
        for row in self.board:
            row = numpy.array(row)
            zeros, ones = (row==0).sum(), (row==1).sum()
            if (n%2 == 0 and zeros != ones) or (n%2 != 0 and abs(zeros-ones != 1)):
                return False
        
        count, board = {}, numpy.transpose(self.board)
        
        for col in board:
            col = numpy.array(col)
            zeros, ones = (row==0).sum(), (row==1).sum()
            if (n%2 == 0 and zeros != ones) or (n%2 != 0 and abs(zeros-ones != 1)):
                return False
            
        return True

class Takuzu(Problem):
    def __init__(self, board: Board):
        """O construtor especifica o estado inicial."""
        self.initial = board

    def actions(self, state: TakuzuState):
        """Retorna uma lista de ações que podem ser executadas a
        partir do estado passado como argumento."""
        # TODO
        pass

    def result(self, state: TakuzuState, action):
        """Retorna o estado resultante de executar a 'action' sobre
        'state' passado como argumento. A ação a executar deve ser uma
        das presentes na lista obtida pela execução de
        self.actions(state)."""
        row, col, val = action[0], action[1], action[2]
        state.board[row][col] = val
        return state

    def goal_test(self, state: TakuzuState):
        """Retorna True se e só se o estado passado como argumento é
        um estado objetivo. Deve verificar se todas as posições do tabuleiro
        estão preenchidas com uma sequência de números adjacentes."""
        board = state.board
        if not (board.check_cols() and board.check_lines()):
            return False

        if not board.check_zero_one():
            return False

        if not board.check_adjacent():
            return False


            

    def h(self, node: Node):
        """Função heuristica utilizada para a procura A*."""
        # TODO
        pass

    # TODO: outros metodos da classe


if __name__ == "__main__":
    # TODO:
    # Ler o ficheiro de input de sys.argv[1],
    # Usar uma técnica de procura para resolver a instância,
    # Retirar a solução a partir do nó resultante,
    # Imprimir para o standard output no formato indicado.
    board = Board.parse_instance_from_stdin()
    #print(str(board))
    #print(type(board))
    takuzu = Takuzu(board)
    state = TakuzuState(board)

    #uncomment this if you're testing
    #for i in range(1000):
        #assert(takuzu.goal_test(state) == False)
