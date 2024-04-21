class Estimate:
    def __init__(self):
        self.array_score = [0, 1, 4, 16, 64, 256]
        self.board_size = 9

    def estimate(self, cells):
        score = 0
        i = 0
        for row in range(self.board_size):
            for col in range(self.board_size):
                if cells[row][col] != 0:
                    i += 1
                for a in range(-1, 2):
                    for b in range(-1, 2):
                        if not (a == 0 and b == 0):
                            score += self.array_score[self.score_(row, col, a, b, 1)] - self.array_score[self.score_(row, col, a, b, -1)]
        return score

    def score_(self, x, y, a, b, symbol, cells):
        score = 0
        for i in range(5):
            flag = self.border(x + a * i, y + b * i)
            if flag == -1 or (cells[x + a * i][y + b * i] != symbol and cells[x + a * i][y + b * i] != 0):
                return 0
            else:
                if cells[x + a * i][y + b * i] == symbol:
                    score += 1
        return score

    def border(self, x, y):
        if x >= 0 and x < self.board_size and y >= 0 and y < self.board_size:
            return True
        return -1
