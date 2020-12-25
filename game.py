import sudoku
from copy import deepcopy


class Puzzle:
    def __init__(self, grid, size, number_of_squares, solution=False):
        self.base_grid = grid
        self.size = size
        self.number_of_squares = number_of_squares
        self.solution = solution if solution is not False else \
            sudoku.modular_solve(deepcopy(grid), size, number_of_squares)
        if self.solution is not False:
            self.Cubes = [[Cube(self.base_grid[row][col], row, col, self.solution[row][col]) for col in range(size)]
                          for row in range(size)]


class Cube:
    def __init__(self, val, row, col, correct_val):
        self.val = val
        self.row = row
        self.col = col
        if val != 0:
            self.base = True
        else:
            self.base = False
        self.correct_val = correct_val


def new_board(size, number_of_squares, difficulties):
    """
    | create new sudoku puzzle and its solution.
    :param size: the size of the sudoku(9/16...).
    :param number_of_squares: the number of square a row/column of the bord is split to (3/4...).
    :param difficulties: 1-easy 2-medium 3-hard, what arbitrary difficulty the board will be.
    :return: grid - board to fill by the user, full - the solution of the board.
    """
    full = sudoku.create_board(size)
    full = sudoku.modular_solve(full, size, number_of_squares)
    grid = deepcopy(full)
    grid = sudoku.remove_numbers(grid, size, number_of_squares, difficulties)
    return grid, full


if __name__ == "__main__":
    temp = [
        [0, 0, 0, 4, 9, 7, 6, 0, 5],
        [0, 0, 6, 3, 0, 8, 0, 0, 0],
        [0, 7, 0, 0, 0, 0, 0, 1, 0],
        [0, 3, 0, 9, 0, 0, 8, 4, 0],
        [6, 0, 0, 0, 3, 0, 0, 0, 0],
        [0, 4, 2, 0, 0, 0, 9, 3, 1],
        [0, 5, 0, 0, 8, 0, 7, 9, 2],
        [0, 8, 0, 7, 5, 3, 1, 6, 0],
        [0, 0, 0, 0, 0, 0, 0, 8, 3]
    ]
    game = Puzzle(temp, 9, 3)
    game2 = new_board(9, 3, 5)
    game2 = Puzzle(game2[0], 9, 3, game2[1])
    print('done')
