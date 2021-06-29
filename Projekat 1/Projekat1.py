import time
import hashmap_1
import tree_1


class Colors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'


class State(object):
    __slots__ = ['board', 'white_tokens', 'black_tokens', 'white', 'black', 'move']

    def __init__(self):
        self.board = []
        for i in range(8):
            self.board.append(8 * ['-'])
        self.white_tokens = 0
        self.black_tokens = 0
        self.white = 0b0
        self.black = 0b0
        self.move = ()

    def initialize_board(self):
        self.board[3][3] = 'w'
        self.board[4][4] = 'w'
        self.board[4][3] = 'b'
        self.board[3][4] = 'b'
        self.calculate_board()

    def __getitem__(self, coordinates):
        x, y = coordinates
        return self.board[x][y]

    def __setitem__(self, coordinates, value):
        x, y = coordinates
        self.board[x][y] = value

    def __delitem__(self, coordinates):
        x, y = coordinates
        self.board[x][y] = '-'

    def calculate_board(self):
        # Kreira binarnu reprezentaciju table i računa broj belih i crnih tokena
        self.white_tokens = 0
        self.black_tokens = 0
        self.white = 0b0
        self.black = 0b0
        for i in range(8):
            for j in range(8):
                self.white = self.white << 1
                self.black = self.black << 1
                if self.board[i][j] == 'w':
                    self.white_tokens += 1
                    self.white += 1
                elif self.board[i][j] == 'b':
                    self.black_tokens += 1
                    self.black += 1

    def tokens(self):
        return self.white_tokens + self.black_tokens

    def key(self):
        # Na osnovu stanja table kreira jedinstven 128 bitni ključ
        return self.white * (2 ** 64) + self.black

    def __eq__(self, other):
        if self.white == other.white and self.black == other.black:
            return True

    def __str__(self):
        board = Colors.BOLD + '   0 1 2 3 4 5 6 7 \n' + Colors.ENDC
        for i in range(8):
            board += Colors.BOLD + str(i) + " " + Colors.ENDC
            for j in range(8):
                board += '|' + self.board[i][j].upper()
            board += '|\n'
        return board


class Game(object):
    __slots__ = ['current_state', 'map']

    def __init__(self):
        self.current_state = None
        self.map = hashmap_1.ChainedHashMap()
        self.initialize_game()

    def initialize_game(self):
        self.current_state = State()
        self.current_state.initialize_board()
        self.next_turn()

    def next_turn(self):
        while True:
            if self.play_white():
                if self.current_state.white_tokens > self.current_state.black_tokens:
                    self.end('w')
                else:
                    self.end('b')
            if self.play_black():
                if self.current_state.white_tokens < self.current_state.black_tokens:
                    self.end('b')
                else:
                    self.end('w')
            if self.current_state.tokens() == 64:
                if self.current_state.white_tokens > self.current_state.black_tokens:
                    self.end('w')
                elif self.current_state.white_tokens < self.current_state.black_tokens:
                    self.end('b')
                else:
                    print(Colors.OKCYAN + "Kraj Igre. Rezultat je izjednačen." + Colors.ENDC)
                    exit()

    def end(self, who):
        if who == 'w':
            print(Colors.OKGREEN + "Kraj Igre. Pobedio je WHITE igrač!" + Colors.ENDC)
            print("White:{} vs Black:{}".format(self.current_state.white_tokens, self.current_state.black_tokens))
            exit()
        elif who == 'b':
            print(Colors.OKGREEN + "Kraj Igre. Pobedio je BLACK igrač!" + Colors.ENDC)
            print("White:{} vs Black:{}".format(self.current_state.white_tokens, self.current_state.black_tokens))
            exit()
        else:
            print(Colors.OKCYAN + "Kraj Igre. Rezultat je izjednačen." + Colors.ENDC)
            exit()

    def best_move(self, board, map):
        root = tree_1.Node(board)

        # Varijabilna dubina
        if board.tokens() < 16:
            n = 5
        elif 16 <= board.tokens() < 48:
            n = 3
        else:
            n = 1

        # Minimax sa alfa-beta rezovima
        _, best_move = self.search(root, n, -10000, 10000, True, map)

        return best_move

    def create_moves(self, who, node):
        all_moves = self.proposal(who, node.value)
        for move in all_moves:
            new_child = node.deepcopy()
            new_child.value.move = move
            self.play(who, move[0], move[1], new_child.value)
            node.add_child(new_child)

    def search(self, position, depth, alfa, beta, player, map):
        if depth == 0:
            heuristic = self.heuristic(position.value)
            map[position.value.key()] = (heuristic, position.value.move)
            return heuristic, position.value.move

        if player:
            try:
                return map[position.value.key()]
            except Exception:
                max_eval = -10000
                max_move = position.value.move
                self.create_moves('b', position)
                for child in position:
                    score, move = self.search(child, depth - 1, alfa, beta, False, map)
                    if score > max_eval:
                        max_eval = score
                        max_move = child.value.move
                    alfa = max(alfa, score)
                    if beta <= alfa:
                        break
                map[position.value.key()] = (max_eval, max_move)
                return max_eval, max_move

        else:
            try:
                return map[position.value.key()]
            except Exception:
                min_eval = 10000
                min_move = position.value.move
                self.create_moves('w', position)
                for child in position:
                    score, move = self.search(child, depth - 1, alfa, beta, True, map)
                    if score < min_eval:
                        min_eval = score
                        min_move = child.value.move
                    beta = min(beta, score)
                    if beta <= alfa:
                        break
                map[position.value.key()] = (min_eval, min_move)
                return min_eval, min_move

    def heuristic(self, board):
        heuristic = 0

        heuristic += self.token_parity(board)
        heuristic += self.mobility(board)
        heuristic += self.walls_captured(board)
        heuristic += self.bad_positions_captured(board)
        heuristic += self.corners_captured(board)
        heuristic += self.good_positions_captured(board)

        return heuristic

    def token_parity(self, board):
        if board.tokens() > 48:
            return 400 * (board.black_tokens - board.white_tokens) / (board.tokens())
        elif board.tokens() > 32:
            return 200 * (board.black_tokens - board.white_tokens) / (board.tokens())
        else:
            return 100 * (board.black_tokens - board.white_tokens) / (board.tokens())

    def mobility(self, board):
        black_moves = len(self.proposal('b', board))
        white_moves = len(self.proposal('w', board))
        if black_moves != 0 or white_moves != 0:
            if board.tokens() > 48:
                return 50 * (black_moves - white_moves) / (black_moves + white_moves)
            elif board.tokens() > 32:
                return 100 * (black_moves - white_moves) / (black_moves + white_moves)
            else:
                return 200 * (black_moves - white_moves) / (black_moves + white_moves)
        else:
            return 0

    def corners_captured(self, board):
        white_corners = 0
        black_corners = 0
        if board[0, 0] == 'w':
            white_corners += 1
        elif board[0, 0] == 'b':
            black_corners += 1
        if board[0, 7] == 'w':
            white_corners += 1
        elif board[0, 7] == 'b':
            black_corners += 1
        if board[7, 0] == 'w':
            white_corners += 1
        elif board[7, 0] == 'b':
            black_corners += 1
        if board[7, 7] == 'w':
            white_corners += 1
        elif board[7, 7] == 'b':
            black_corners += 1

        if white_corners != 0 or black_corners != 0:
            return 500 * (black_corners - white_corners) / (black_corners + white_corners)
        else:
            return 0

    def walls_captured(self, board):
        white_walls = 0
        black_walls = 0
        for i in range(2, 6):
            if board[0, i] == 'w':
                white_walls += 1
            elif board[0, i] == 'b':
                black_walls += 1
        for i in range(2, 6):
            if board[7, i] == 'w':
                white_walls += 1
            elif board[7, i] == 'b':
                black_walls += 1
        for i in range(2, 6):
            if board[i, 0] == 'w':
                white_walls += 1
            elif board[i, 0] == 'b':
                black_walls += 1
        for i in range(2, 6):
            if board[i, 7] == 'w':
                white_walls += 1
            elif board[i, 7] == 'b':
                black_walls += 1

        if white_walls != 0 or black_walls != 0:
            return 100 * (black_walls - white_walls) / (black_walls + white_walls)
        else:
            return 0

    def bad_positions_captured(self, board):
        white_bad = 0
        black_bad = 0

        if board[0, 1] == 'w':
            white_bad += 1
        elif board[0, 1] == 'b':
            black_bad += 1
        if board[1, 0] == 'w':
            white_bad += 1
        elif board[1, 0] == 'b':
            black_bad += 1
        if board[1, 1] == 'w':
            white_bad += 1
        elif board[1, 1] == 'b':
            black_bad += 1

        if board[0, 6] == 'w':
            white_bad += 1
        elif board[0, 6] == 'b':
            black_bad += 1
        if board[1, 6] == 'w':
            white_bad += 1
        elif board[1, 6] == 'b':
            black_bad += 1
        if board[1, 7] == 'w':
            white_bad += 1
        elif board[1, 7] == 'b':
            black_bad += 1

        if board[6, 1] == 'w':
            white_bad += 1
        elif board[6, 1] == 'b':
            black_bad += 1
        if board[6, 0] == 'w':
            white_bad += 1
        elif board[6, 0] == 'b':
            black_bad += 1
        if board[7, 1] == 'w':
            white_bad += 1
        elif board[7, 1] == 'b':
            black_bad += 1

        if board[6, 7] == 'w':
            white_bad += 1
        elif board[6, 7] == 'b':
            black_bad += 1
        if board[6, 6] == 'w':
            white_bad += 1
        elif board[6, 6] == 'b':
            black_bad += 1
        if board[7, 6] == 'w':
            white_bad += 1
        elif board[7, 6] == 'b':
            black_bad += 1

        if white_bad != 0 or black_bad != 0:
            return -(black_bad - white_bad) / (black_bad + white_bad)
        else:
            return 0

    def good_positions_captured(self, board):
        white_good = 0
        black_good = 0
        for i in range(2, 6):
            for j in range(2, 6):
                if board[i, j] == 'w':
                    white_good += 1
                elif board[i, j] == 'b':
                    black_good += 1
        if board.tokens() > 32:
            return (black_good - white_good) / (black_good + white_good)
        else:
            return 200 * (black_good - white_good) / (black_good + white_good)

    def is_valid(self, who, x, y, board):
        # Proverava validnost poteza
        if board[x, y] == '-':
            for vertical in (1, 0, -1):
                for horizontal in (1, 0, -1):
                    if vertical != 0 or horizontal != 0:
                        if self.valid_move(who, x, y, vertical, horizontal, board):
                            return True
        return False

    def other(self, who):
        if who == 'w':
            return 'b'
        else:
            return 'w'

    def check_direction(self, who, row, column, vertical, horizontal, board):
        if board[row, column] == '-':
            return False
        if board[row, column] == who:
            return True
        if row + horizontal < 0 or row + horizontal > 7:
            return False
        if column + vertical < 0 or column + vertical > 7:
            return False
        return self.check_direction(who, row + horizontal, column + vertical, vertical, horizontal, board)

    def valid_move(self, who, row, column, horizontal, vertical, board):
        other = self.other(who)
        if row + horizontal < 0 or row + horizontal > 7:
            return False
        if column + vertical < 0 or column + vertical > 7:
            return False
        if board[row + horizontal, column + vertical] != other:
            return False
        if row + horizontal * 2 < 0 or row + horizontal * 2 > 7:
            return False
        if column + vertical * 2 < 0 or column + vertical * 2 > 7:
            return False
        return self.check_direction(who, row + horizontal * 2, column + vertical * 2, vertical, horizontal, board)

    def proposal(self, who, board):
        # Kreira niz predloga svih mogućih poteza koje igrač može da odigra u određenom stanju
        possible_moves = []
        for row in range(8):
            for column in range(8):
                if board[row, column] == '-':
                    nn = self.valid_move(who, row, column, -1, 0, board)
                    if nn:
                        possible_moves.append((row, column))
                        continue
                    ne = self.valid_move(who, row, column, -1, 1, board)
                    if ne:
                        possible_moves.append((row, column))
                        continue
                    nw = self.valid_move(who, row, column, -1, -1, board)
                    if nw:
                        possible_moves.append((row, column))
                        continue

                    ee = self.valid_move(who, row, column, 0, 1, board)
                    if ee:
                        possible_moves.append((row, column))
                        continue
                    ww = self.valid_move(who, row, column, 0, -1, board)
                    if ww:
                        possible_moves.append((row, column))
                        continue

                    ss = self.valid_move(who, row, column, 1, 0, board)
                    if ss:
                        possible_moves.append((row, column))
                        continue
                    se = self.valid_move(who, row, column, 1, 1, board)
                    if se:
                        possible_moves.append((row, column))
                        continue
                    sw = self.valid_move(who, row, column, 1, -1, board)
                    if sw:
                        possible_moves.append((row, column))
        return possible_moves

    def flip_line(self, who, row, column, horizontal, vertical, board):
        if row + horizontal < 0 or row + horizontal > 7:
            return False
        if column + vertical < 0 or column + vertical > 7:
            return False
        if board[row + horizontal, column + vertical] == '-':
            return False
        if board[row + horizontal, column + vertical] == who:
            return True
        else:
            if self.flip_line(who, row + horizontal, column + vertical, horizontal, vertical, board):
                board[row + horizontal, column + vertical] = who
                return True
            else:
                return False

    def flip(self, who, x, y, board):
        self.flip_line(who, x, y, -1, 0, board)
        self.flip_line(who, x, y, -1, 1, board)
        self.flip_line(who, x, y, -1, -1, board)

        self.flip_line(who, x, y, 0, 1, board)
        self.flip_line(who, x, y, 0, -1, board)

        self.flip_line(who, x, y, 1, 0, board)
        self.flip_line(who, x, y, 1, 1, board)
        self.flip_line(who, x, y, 1, -1, board)

    def play(self, who, x, y, board):
        # Realizacija samog poteza
        board[x, y] = who
        self.flip(who, x, y, board)
        board.calculate_board()

    def play_white(self):
        print("\nNa potezu je WHITE igrač\n")
        print(self.current_state)

        while True:
            proposals = self.proposal('w', self.current_state)
            if len(proposals) == 0:
                return True
            print(Colors.OKBLUE + "Moguć potez: X = {}, Y = {}".format(proposals[0][0], proposals[0][1]) + Colors.ENDC)
            for i in range(1, len(proposals)):
                print("Moguć potez: X = {}, Y = {}".format(proposals[i][0], proposals[i][1]))
            try:
                x = int(input("Unesite X kordinatu: "))
                y = int(input("Unesite Y kordinatu: "))
                if self.is_valid('w', x, y, self.current_state):
                    self.play('w', x, y, self.current_state)
                    return False
            except Exception:
                pass
            print(Colors.BOLD + "\n! Odigrani potez nije validan! Pokušajte ponovo. !\n" + Colors.ENDC)

    def play_black(self):
        print("\nNa potezu je BLACK igrač\n")
        print(self.current_state)
        start = time.time()
        proposals = self.proposal('b', self.current_state)
        if len(proposals) == 0:
            return True
        played = False
        for force in [(0, 0), (0, 7), (7, 0), (7, 7)]:
            if force in proposals:
                self.play('b', force[0], force[1], self.current_state)
                played = True
                break
        best_move = self.best_move(self.current_state, self.map)
        if not played:
            self.play('b', best_move[0], best_move[1], self.current_state)
        end = time.time()
        print("T: ", end - start)
        return False


def main():
    new_game = Game()


if __name__ == '__main__':
    main()
