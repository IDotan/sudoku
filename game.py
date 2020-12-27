import sudoku
from copy import deepcopy
import pygame


class Puzzle:
    def __init__(self, grid, size, number_of_squares, solution=False, empty=False):
        self.base_grid = grid
        self.size = size
        self.number_of_squares = number_of_squares
        self.solution = False
        if empty is False:
            self.solution = solution if solution is not False else \
                sudoku.modular_solve(deepcopy(grid), size, number_of_squares)
        if self.solution is not False:
            self.Cubes = [[Cube(self.base_grid[row][col], row, col, self.solution[row][col]) for col in range(size)]
                          for row in range(size)]
        else:
            self.Cubes = [[Cube(self.base_grid[row][col], row, col, None) for col in range(size)]
                          for row in range(size)]

    def reset_board(self):
        for row in range(self.size):
            for col in range(self.size):
                self.Cubes[row][col].reset_cube()

    def draw_board(self, window):
        cubes = 9
        board_width = window_width - 199
        board_height = window_height
        if self.size == 16:
            cubes = 16
        gap = board_width // cubes
        for i in range(self.size + 1):
            if i in range(0, self.size + 1, self.number_of_squares):
                thick = 4
            else:
                thick = 1
            pygame.draw.line(window, (0, 0, 0), (0, i * gap), (board_width, i * gap), thick)
            pygame.draw.line(window, (0, 0, 0), (i * gap, 0), (i * gap, board_height), thick)

        # Draw Cubes
        # for i in range(self.rows):
        #     for j in range(self.cols):
        #         self.cubes[i][j].draw(win)


class Cube:
    def __init__(self, val, row, col, correct_val):
        self.val = val
        self.row = row
        self.col = col
        self.base = True if val != 0 else False
        self.correct_val = correct_val

    def reset_cube(self):
        if not self.base:
            self.val = 0

    def set_val(self, value):
        if not self.base:
            self.val = value

    def get_val(self):
        return self.val


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


def draw_board(window, board, size_9, size_16):
    window.fill((255, 255, 255))

    board.draw_board(window)


def get_key(event):
    key = None
    if event.unicode == "1":
        key = 1
    elif event.unicode == "2":
        key = 2
    elif event.unicode == "3":
        key = 3
    elif event.unicode == "4":
        key = 4
    elif event.unicode == "5":
        key = 5
    elif event.unicode == "6":
        key = 6
    elif event.unicode == "7":
        key = 7
    elif event.unicode == "8":
        key = 8
    elif event.unicode == "9":
        key = 9
    elif event.key == 13:
        # enter
        key = '\r'
    elif event.key == 8:
        # delete
        key = '\x08'
    return key


def game_loop():
    window = pygame.display.set_mode([window_width, window_height])
    pygame.display.set_caption("Sudoku Game")
    board = sudoku.create_board(9)
    board = Puzzle(board, 9, 3, empty=True)
    key_pressed = None
    size_9 = True
    size_16 = False
    run = True
    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.KEYDOWN:
                key_pressed = get_key(event)

        draw_board(window, board, size_9, size_16)
        pygame.display.update()

    pygame.quit()


window_width = 1000
window_height = 800
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
    game_loop()
