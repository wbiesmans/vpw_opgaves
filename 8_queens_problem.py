class ChessBoard:
    def __init__(self, size):
        self.size = size

        # 0: empty, 1: queen, -1: attacked
        self.board = [[0 for _ in range(size)] for _ in range(size)]
        self.queen_positions = []

    def return_copy(self):
        new_board = ChessBoard(self.size)
        new_board.board = [row[:] for row in self.board]
        new_board.queen_positions = self.queen_positions.copy()
        return new_board

    def add_queen(self, row, col):
        if self.is_safe(row, col):
            self.board[row][col] = 1
            self.queen_positions.append((row, col))  # For tracking queen positions
            self.mark_attacks(row, col)
            return True
        return False

    def mark_attacks(self, queen_row, queen_col):
        # Mark column
        for row in range(self.size):
            self.board[row][queen_col] = -1

        # Mark row
        for col in range(self.size):
            self.board[queen_row][col] = -1

        for i in range(-self.size, self.size):
            # Mark left diagonal
            if 0 <= queen_row + i < self.size and 0 <= queen_col + i < self.size:
                self.board[queen_row + i][queen_col + i] = -1
            if 0 <= queen_row + i < self.size and 0 <= queen_col - i < self.size:
                self.board[queen_row + i][queen_col - i] = -1
            # Mark right diagonal
            if 0 <= queen_row + i < self.size and 0 <= queen_col + i < self.size:
                self.board[queen_row + i][queen_col + i] = -1
            if 0 <= queen_row + i < self.size and 0 <= queen_col - i < self.size:
                self.board[queen_row + i][queen_col - i] = -1

        # Reset the queen's position to 1 (since it was marked as -1 in the above loops)
        self.board[queen_row][queen_col] = 1

    def is_safe(self, row, col):
        return self.board[row][col] == 0


def solve_n_queens(size):
    # For memoization to determine which solutions are unique
    current_solutions_i = [set() for _ in range(size)]

    def backtrack(row, board):
        if row == size:
            return

        current_solution = board.queen_positions
        for col in range(size):
            potential_new_solution = tuple(sorted(current_solution + [(row, col)]))
            if potential_new_solution in current_solutions_i[row]:
                continue
            if board.is_safe(row, col):
                new_board = board.return_copy()
                new_board.add_queen(row, col)
                current_solutions_i[row].add(potential_new_solution)
                backtrack(row + 1, new_board)

    initial_board = ChessBoard(size)
    backtrack(0, initial_board)
    return [list(solution) for solution in current_solutions_i[-1]]


if __name__ == "__main__":
    n = 8
    solutions = solve_n_queens(n)
    print(f"Number of solutions for {n}-Queens: {len(solutions)}")
    for solution in solutions:
        print(solution)
