# takuzu.py: Template para implementação do projeto de Inteligência Artificial 2021/2022.
# Devem alterar as classes e funções neste ficheiro de acordo com as instruções do enunciado.
# Além das funções e classes já definidas, podem acrescentar outras que considerem pertinentes.

# Grupo 35:
# 99095 João Furtado
# 99078 Guilherme Carabalone

import sys
from search import (
    Problem,
    InstrumentedProblem,
    Node,
    compare_searchers,
    astar_search,
    breadth_first_tree_search,
    depth_first_tree_search,
    depth_limited_search,
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


class Board:
    """Representação interna de um tabuleiro de Takuzu."""
    def __init__(self, board: tuple):
        self.board = board
        self.len = len(board)
    
    def get_number(self, row: int, col: int) -> int:
        """Devolve o valor na respetiva posição do tabuleiro."""
        return self.board[row][col]
    
    def adjacent_vertical_numbers(self, row: int, col: int):
        """Devolve os valores imediatamente abaixo e acima,
        respectivamente."""
        lines = self.len
        if row == 0:
            return self.board[row + 1][col], None
        elif row == lines-1:
            return None, self.board[row - 1][col]
        return self.board[row + 1][col], self.board[row - 1][col]

    def adjacent_horizontal_numbers(self, row: int, col: int):
        """Devolve os valores imediatamente à esquerda e à direita,
        respectivamente."""
        cols = self.len
        if col == 0:
            return None, self.board[row][col + 1]
        elif col == cols-1:
            return self.board[row][col - 1], None
        return self.board[row][col - 1], self.board[row][col + 1]

    def __contains__(self, number: int):
        for i in self.board:
            if number in i:
                return True
        return False
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
            for index, element in enumerate(row):
                if index == self.len-1:
                    string += str(element) + '\n'
                else:
                    string += str(element) + '\t'
        return string[:-1]


    #TODO as linhas não podem conter 2   (em teoria)  
    def check_lines(self):
        b = []
        for row in self.board:
            if row in b:
                return False
            else:    
                b += [row]
        return len(b) == self.len
    
    #TODO as linhas não podem conter 2 (em teoria)    
    def check_cols(self):
        b = []
        for row in zip(*self.board):
            if row in b:
                return False 
            else: 
                b += [row]
        return len(b) == self.len
    
    def check_adjacent(self):
        for i in range(self.len):
            for j in range(self.len-2):
                if (self.board[i][j] != 2 and self.board[i][j] == self.board[i][j+1] == self.board[i][j+2] or
                    self.board[j][i] != 2 and self.board[j][i] == self.board[j+1][i] == self.board[j+2][i]):
                    return False
                
        return True
    def check_over_half(self):
        gtp = self.len//2
        gto = self.len//2 + 1
        for i in range(self.len):
            countr = {0: 0, 1: 0}
            for j in range(self.len):
                elr = self.board[i][j]
                if elr in (0,1):
                    countr[elr] += 1
            if (self.len % 2 != 0):
                if (countr[1] > gto or countr[0] > gto):
                    return False
            else:
                if (countr[1] > gtp or countr[0] > gtp):
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
    
    def generate_possibilities(self):
        for row in self.board:
            for el in row:
                if el == 2:
                    result = (self.board.index(row), row.index(el))
                    break

        actions = [(result[0], result[1], 0), (result[0], result[1], 1)]
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
        result_board = [[x for x in row] for row in state.board.board] 
        result_board[row][col] = val
        return TakuzuState(Board(result_board))

    def goal_test(self, state: TakuzuState):
        """Retorna True se e só se o estado passado como argumento é
        um estado objetivo. Deve verificar se todas as posições do tabuleiro
        estão preenchidas com uma sequência de números adjacentes."""
        return 2 not in state.board 
    def h(self, node: Node):
        return heuristic(node.state)
    
    def patch_illegal(self, state: TakuzuState, arr: list):
        """Given a list containing actions, it removes the illegal moves."""
        temp = ()
        for action in arr:
            res = self.result(state, action)
            board_res = res.board
            if not (board_res.check_over_half()):
                temp += (action,)
            # if not (board_res.check_zero_one()):
                # temp += (action,)
                # print(f"removeu: {action} zero_one")
                # print(f"pq resultado: \n{res.board}")

            elif not board_res.check_adjacent() and action in arr:
                temp += (action,)
            elif 2 not in board_res:
                if not board_res.check_lines() and action in arr:
                    temp += (action,)
                elif not board_res.check_cols() and action in arr:
                    temp += (action,)
                
        
        res = []
        for item in arr:
            if item not in temp:
                res.append(item)
        return res
    
    
def heuristic(state: TakuzuState):
    board = state.board.board
    h = {}
    for i, e in enumerate(board):
        count = board[i].count(2)
        h[i] = count
    
    vals = h.values()
    minimum = state.board.len
    for val in vals:
        if (val < minimum and val > 0):
            minimum = val
    return 1/minimum

if __name__ == "__main__":
    board = Board.parse_instance_from_stdin()
    takuzu = Takuzu(board)
    def depth_limited_search_wrapper():
        limit = board.len**2
        return depth_limited_search()
    # TODO:

    goal_node = depth_limited_search(takuzu, limit=board.len**2)
    print(board.len)
    compare_searchers([takuzu], "fodase", searchers=[depth_first_tree_search,
                                                        breadth_first_tree_search,
                                                        depth_limited_search,
                                                        astar_search,
                                                        greedy_search])
