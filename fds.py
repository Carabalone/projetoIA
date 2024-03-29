# takuzu.py: Template para implementação do projeto de Inteligência Artificial 2021/2022.
# Devem alterar as classes e funções neste ficheiro de acordo com as instruções do enunciado.
# Além das funções e classes já definidas, podem acrescentar outras que considerem pertinentes.

# Grupo xx:
# 99095 João Furtado
# 99078 Guilherme Carabalone

from copy import deepcopy
import sys
import math

import numpy
# from regex import P
from search import (
    Problem,
    Node,
    astar_search,
    breadth_first_tree_search,
    depth_first_tree_search,
    greedy_search,
    recursive_best_first_search,
)

#COMI O CU DE QUEM TA LENDO

class TakuzuState:
    state_id = 0

    def __init__(self, board):
        self.board = board
        self.id = TakuzuState.state_id
        TakuzuState.state_id += 1

    def __lt__(self, other):
        return self.id < other.id


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
        if row == 0:
            return self.board[row + 1][col], None
        elif row == lines-1:
            return None, self.board[row - 1][col]
        return self.board[row + 1][col], self.board[row - 1][col]

    def adjacent_horizontal_numbers(self, row: int, col: int) -> (int, int):
        """Devolve os valores imediatamente à esquerda e à direita,
        respectivamente."""
        cols = self.len
        if col == 0:
            return None, self.board[row][col + 1]
        elif col == cols-1:
            return self.board[row][col - 1], None
        return self.board[row][col - 1], self.board[row][col + 1]
    
    def check_adjacent_v2(self):
        board = self.board
        print(board)
        len = self.len
        for row in range(len):
            for val in range(len):
                ver = self.adjacent_vertical_numbers(row, val)
                hor = self.adjacent_horizontal_numbers(row, val)
                if all(x==val for x in ver) or all(x==val for x in hor):
                    return False
        return True

    def __contains__(self, number: int):
        return len([x for x in self.board if number in x]) > 0

    @staticmethod
    def parse_instance_from_stdin():
        """Lê o test do standard input (stdin) que é passado como argumento
        e retorna uma instância da classe Board.

        Por exemplo:
            $ python3 takuzu.py < input_T01

            > from sys import stdin
            > stdin.readline()
        """

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

    #TODO as linhas não podem conter 2   (em teoria)  
    def check_lines(self):
        board_w = []
        for row in self.board:
            if 2 not in row:
                board_w += [row]
        u, c = numpy.unique(board_w, axis=0, return_counts=True)
        return (c==1).all()
    
    #TODO as linhas não podem conter 2 (em teoria)    
    def check_cols(self):
        board_w = []
        board_t = numpy.transpose(self.board)
        for col in board_t:
            if 2 not in col:
                board_w += [col]
        u, c = numpy.unique(board_w, axis=0, return_counts=True)
        return (c==1).all()
    
    #TODO ERRADO
    def check_row_and_col(self):
        matrix = numpy.matrix(self.board)
        for i in range(self.len):  # generate pairs
            for j in range(i + 1, self.len): 
                if numpy.array_equal(matrix[i], matrix[j]):  # compare rows
                    if numpy.array_equal(matrix[:,i], matrix[:,j]):  # compare columns
                        return False
        return True

    def check_adjacent(self):
        for i in range(self.len):
            for j in range(self.len-2):
                if self.board[i][j] != 2 and self.board[i][j] == self.board[i][j+1] == self.board[i][j+2]:
                    return False
        for j in range(self.len):
            for i in range(self.len-2):
                if self.board[i][j] != 2 and self.board[i][j] == self.board[i+1][j] == self.board[i+2][j]:
                    return False
        return True


    def check_over_half(self):
        for line in self.board:
            count = {0: 0, 1: 0}
            for el in line:
                if el in (0,1):
                    count[el] += 1
            if (self.len % 2 != 0):
                if (count[1] > self.len//2 + 1 or count[0] > self.len//2 + 1):
                    return False
            else:
                if (count[1] > self.len//2 or count[0] > self.len//2):
                    return False

        for col in list(zip(*self.board)):
            count = {0: 0, 1: 0}
            for el in col:
                if el in (0,1):
                    count[el] += 1
            if (self.len % 2 != 0):
                if (count[1] > self.len//2 + 1 or count[0] > self.len//2 + 1):
                    return False
            else:
                if (count[1] > self.len//2 or count[0] > self.len//2):
                    return False
        
        return True


    def check_zero_one(self):
        for line in self.board:
            count = {0: 0, 1: 0}
            for el in line:
                if (el == 2):
                    raise ValueError("non full board being zero-one-checked")
                if el in (0,1):
                    count[el] += 1
            if self.len % 2 == 0:
                if (abs(count[0]-count[1]) > 0):
                    return False
            elif (abs(count[0]-count[1]) > 1):
                return False
        
        for col in zip(*self.board):
            count = {0: 0, 1: 0}
            for el in col:
                if (el == 2):
                    raise ValueError("non full board being zero-one-checked")
                if el in (0,1):
                    count[el] += 1
            if self.len % 2 == 0:
                if (abs(count[0]-count[1]) > 0):
                    return False
            elif (abs(count[0]-count[1]) > 1):
                return False
        
        return True
    
    def check_zero_one_v2(self):
        board_t = numpy.transpose(self.board)
        for row in self.board:
            if 2 not in row:
                ones, zeros = numpy.count_nonzero(row == 1), numpy.count_nonzero(row == 0)
                if (self.len % 2 == 0 and ones != zeros):
                    return False
                if (self.len % 2 != 0 and abs(ones-zeros) != 1):
                    return False
        for col in board_t:
            if 2 not in col:
                ones, zeros = numpy.count_nonzero(col == 1), numpy.count_nonzero(col == 0)
                if (self.len % 2 == 0 and ones != zeros):
                    return False
                if (self.len % 2 != 0 and abs(ones-zeros) != 1):
                    return False
        return True

    def generate_possibilities(self):
        result = numpy.argwhere(numpy.array(self.board) == 2)
        actions = [(x[0], x[1], y) for y in (0,1) for x in result]
        return actions
    
    def full_board(self):
        for row in self.board:
            if 2 in row:
                return False
        return True

class Takuzu(Problem):
    def __init__(self, board: Board):
        """O construtor especifica o estado inicial."""
        self.initial = TakuzuState(board)

    def actions(self, state: TakuzuState):
        """Retorna uma lista de ações que podem ser executadas a
        partir do estado passado como argumento."""
        actions = state.board.generate_possibilities()
        actions = self.patch_illegal(state, actions)
        return actions

    def result(self, state: TakuzuState, action):
        """Retorna o estado resultante de executar a 'action' sobre
        'state' passado como argumento. A ação a executar deve ser uma
        das presentes na lista obtida pela execução de
        self.actions(state)."""
        row, col, val = action[0], action[1], action[2]
        result_board = numpy.copy(state.board.board)
        result_board[row][col] = val
        return TakuzuState(Board(result_board))

    def goal_test(self, state: TakuzuState):
        """Retorna True se e só se o estado passado como argumento é
        um estado objetivo. Deve verificar se todas as posições do tabuleiro
        estão preenchidas com uma sequência de números adjacentes."""
        board = state.board
        if not board.full_board():
            print("rejeito pq 2 in board")
            return False
        # if (not board.check_zero_one()):
        #     print("nao passou goal pq check zero one")
        #     return False
        # if (not board.check_adjacent_v2()):
        #     # print("nao passou goal pq check adj")
        #     return False
        # if (not board.check_over_half()):
        #     # print("nao passou goal pq check over half")
        #     return False
        # if not board.check_cols():
        #     # print("nao passou goal pq check cols")
        #     return False
        # if (not board.check_lines()):
        #     # print("nao passou goal pq check lines")
        #     return False
        return True
        #return board.check_over_half() and board.check_lines() and board.check_cols() and board.check_zero_one() and board.check_adjacent()

    def h(self, node: Node):
        """Função heuristica utilizada para a procura A*."""
        # TODO
        pass
    
    def patch_illegal(self, state: TakuzuState, arr: list):
        """Given a list containing actions, it removes the illegal moves."""
        arr = list(arr)
        # print(f"patch illegal inicial: {arr}, len {len(arr)}")
        i=0
        temp = ()
        for action in arr:
            i+=1
            # print(f"act: {action}")
            res = self.result(state, action)
            board_res = res.board
            # if not (board_res.check_over_half()):
            #     temp += (action,)
                # print(f"removeu: {action} over half")
                # print(f"pq resultado: \n{res.board}")
            # if not board_res.check_lines() and action in arr:
            #     temp += (action,)
            #     print(f"removeu: {action} lines")
            #     print(f"pq resultado: \n{res.board}")

                
            # if not board_res.check_cols() and action in arr:
            #     temp += (action,)
            #     print(f"removeu: {action} row")
            #     print(f"pq resultado: \n{res.board}")

                
            # if not board_res.check_adjacent_v2() and action in arr:
            #     temp += (action,)
            #     print(f"removeu: {action} adjacent")
            #     print(f"pq resultado: \n{res.board}")
            
            # if not board_res.check_zero_one_v2() and action in arr:
            #     temp += (action,)
            #     print(f"removeu: {action} adjacent")
            #     print(f"pq resultado: \n{res.board}")
        
        res = []
        for item in arr:
            if item not in temp:
                res.append(item)
        return res
    
    def search(self):
        return depth_first_tree_search(self)
    # TODO: outros metodos da classe


if __name__ == "__main__":
    # TODO:
    # Ler o ficheiro de input de sys.argv[1],
    # Usar uma técnica de procura para resolver a instância,
    # Retirar a solução a partir do nó resultante,
    # Imprimir para o standard output no formato indicado.
    board = Board.parse_instance_from_stdin()
    takuzu = Takuzu(board)
    #print(type(takuzu.initial))
    state = TakuzuState(board)

    res = takuzu.search()
    if (res):
        print(res.state.board)
        # pass
    else:
        print("None")
        # pass
    #testb = Board([[2,2,1,1],[1,0,2,1],[0,2,1,0],[1,2,1,2]])