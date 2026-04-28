import copy

BOARD_SIZE = 9
EMPTY = "."
BLACK = "X"   # Người chơi
WHITE = "O"   # AI


class GoGame:
    def __init__(self):
        self.board = [[EMPTY for _ in range(BOARD_SIZE)] for _ in range(BOARD_SIZE)]

    def in_board(self, x, y):
        return 0 <= x < BOARD_SIZE and 0 <= y < BOARD_SIZE

    def neighbors(self, x, y):
        directions = [(1, 0), (-1, 0), (0, 1), (0, -1)]
        result = []

        for dx, dy in directions:
            nx = x + dx
            ny = y + dy

            if self.in_board(nx, ny):
                result.append((nx, ny))

        return result

    def get_group(self, board, x, y, visited=None):
        if visited is None:
            visited = set()

        color = board[x][y]
        group = set()
        stack = [(x, y)]

        while stack:
            cx, cy = stack.pop()

            if (cx, cy) in visited:
                continue

            visited.add((cx, cy))
            group.add((cx, cy))

            for nx, ny in self.neighbors(cx, cy):
                if board[nx][ny] == color and (nx, ny) not in visited:
                    stack.append((nx, ny))

        return group

    def count_liberties(self, board, group):
        liberties = set()

        for x, y in group:
            for nx, ny in self.neighbors(x, y):
                if board[nx][ny] == EMPTY:
                    liberties.add((nx, ny))

        return len(liberties)

    def remove_captured_stones(self, board, opponent):
        visited = set()

        for i in range(BOARD_SIZE):
            for j in range(BOARD_SIZE):
                if board[i][j] == opponent and (i, j) not in visited:
                    group = self.get_group(board, i, j, visited)
                    liberties = self.count_liberties(board, group)

                    if liberties == 0:
                        for x, y in group:
                            board[x][y] = EMPTY

    def is_valid_move(self, board, x, y, player):
        if not self.in_board(x, y):
            return False

        if board[x][y] != EMPTY:
            return False

        temp_board = copy.deepcopy(board)
        temp_board[x][y] = player

        opponent = BLACK if player == WHITE else WHITE
        self.remove_captured_stones(temp_board, opponent)

        group = self.get_group(temp_board, x, y)
        liberties = self.count_liberties(temp_board, group)

        return liberties > 0

    def make_move(self, board, x, y, player):
        new_board = copy.deepcopy(board)
        new_board[x][y] = player

        opponent = BLACK if player == WHITE else WHITE
        self.remove_captured_stones(new_board, opponent)

        return new_board

    def get_valid_moves(self, board, player):
        moves = []

        for i in range(BOARD_SIZE):
            for j in range(BOARD_SIZE):
                if board[i][j] != EMPTY:
                    continue

                if self.is_valid_move(board, i, j, player):
                    moves.append((i, j))

        return moves

    def evaluate_board(self, board):
        ai_score = 0
        human_score = 0
        visited = set()

        center = BOARD_SIZE // 2

        for i in range(BOARD_SIZE):
            for j in range(BOARD_SIZE):
                if board[i][j] != EMPTY and (i, j) not in visited:
                    group = self.get_group(board, i, j, visited)
                    liberties = self.count_liberties(board, group)
                    group_size = len(group)

                    center_bonus = 0
                    for x, y in group:
                        dist = abs(x - center) + abs(y - center)
                        center_bonus += max(0, 4 - dist)

                    danger_penalty = 0
                    if liberties <= 1:
                        danger_penalty = -15

                    score = (
                        group_size * 12
                        + liberties * 5
                        + center_bonus * 2
                        + danger_penalty
                    )

                    if board[i][j] == WHITE:
                        ai_score += score
                    else:
                        human_score += score

        return ai_score - human_score

    def calculate_score(self, board):
        black_score = 0
        white_score = 0
        visited = set()

        for i in range(BOARD_SIZE):
            for j in range(BOARD_SIZE):
                if board[i][j] != EMPTY and (i, j) not in visited:
                    group = self.get_group(board, i, j, visited)
                    liberties = self.count_liberties(board, group)

                    score = len(group) + liberties

                    if board[i][j] == BLACK:
                        black_score += score
                    elif board[i][j] == WHITE:
                        white_score += score

        return black_score, white_score

    def is_board_full(self, board):
        for row in board:
            if EMPTY in row:
                return False
        return True

    def is_game_over(self, board):
        if self.is_board_full(board):
            return True

        black_moves = self.get_valid_moves(board, BLACK)
        white_moves = self.get_valid_moves(board, WHITE)

        return len(black_moves) == 0 and len(white_moves) == 0

    def get_winner(self, board):
        black_score, white_score = self.calculate_score(board)

        if black_score > white_score:
            return BLACK, black_score, white_score
        elif white_score > black_score:
            return WHITE, black_score, white_score
        else:
            return "DRAW", black_score, white_score
