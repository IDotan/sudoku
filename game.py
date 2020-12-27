import sudoku
from copy import deepcopy
import pygame


class Puzzle:
    def __init__(self, grid, size, number_of_squares, solution=False):
        self.base_grid = grid
        self.size = size
        self.number_of_squares = number_of_squares
        self.solution = solution
        self.board_width = window_width - 199
        self.board_height = window_height
        self.selected = None
        self.solution = solution if solution is not False else \
            sudoku.modular_solve(deepcopy(grid), size, number_of_squares)
        if self.solution is not False:
            self.cubes = [[Cube(self.base_grid[row][col], row, col, self.solution[row][col], self.board_width,
                                self.size) for col in range(size)] for row in range(size)]
        else:
            self.cubes = [[Cube(self.base_grid[row][col], row, col, None, self.board_width, self.size)
                           for col in range(size)] for row in range(size)]

    def reset_board(self):
        for row in range(self.size):
            for col in range(self.size):
                self.cubes[row][col].reset_cube()

    def draw_board(self, window):
        gap = self.board_width // self.size
        for i in range(self.size + 1):
            if i in range(0, self.size + 1, self.number_of_squares):
                thick = 4
            else:
                thick = 1
            pos = i * gap
            pygame.draw.line(window, (0, 0, 0), (0, pos), (self.board_width, pos), thick)
            pygame.draw.line(window, (0, 0, 0), (pos, 0), (pos, self.board_height), thick)
            # add lower border at the bottom of the board
            if i == self.size:
                pygame.draw.line(window, (0, 0, 0), (0, pos - 4), (self.board_width, pos - 4), thick)

        for row in range(self.size):
            for col in range(self.size):
                self.cubes[row][col].draw_cube(window)

    def click(self, pos):
        if pos[0] < self.board_width and pos[1] < self.board_height:
            gap = self.board_width / self.size
            x = pos[0] // gap
            y = pos[1] // gap
            return int(y), int(x)
        else:
            return None

    def delete_selected(self):
        if self.selected is not None:
            row, col = self.selected
            self.cubes[row][col].set_val(0)

    def select(self, row, col):
        # Reset all other
        for i in range(self.size):
            for j in range(self.size):
                self.cubes[i][j].selected = False

        self.cubes[row][col].selected = True
        self.selected = (row, col)

    def enter_value(self, value):
        row, col = self.selected
        self.cubes[row][col].set_val(value)

class Cube:
    def __init__(self, val, row, col, correct_val, board_width, size):
        self.val = val
        self.row = row
        self.col = col
        self.base = True if val != 0 else False
        self.correct_val = correct_val
        self.cube_width = board_width // size
        self.size = size
        self.selected = False

    def reset_cube(self):
        if not self.base:
            self.val = 0

    def set_val(self, value):
        if not self.base:
            self.val = value

    def get_val(self):
        return self.val

    def draw_cube(self, window):
        font_size = 75
        if self.size == 16:
            font_size = 45
        fnt = pygame.font.SysFont("comicsans", font_size)
        x = self.col * self.cube_width
        y = self.row * self.cube_width

        if not (self.val == 0):
            font_color = (113, 183, 253)
            # black for base number
            if self.base is True:
                font_color = (0, 0, 0)
            # red font when incorrect number
            elif self.val != self.correct_val:
                font_color = (255, 0, 0)
            text = fnt.render(str(self.val), True, font_color)
            window.blit(text, (x + (self.cube_width / 2 - text.get_width() / 2),
                               y + (self.cube_width / 2 - text.get_height() / 2)))
        if self.selected:
            pygame.draw.rect(window, (71, 170, 255), (x, y, self.cube_width, self.cube_width), 3)


def difficulties_to_attempts(size, difficulties):
    attempts = 0
    if difficulties == 1:
        attempts = 3
    elif difficulties == 2:
        attempts = 5
    elif difficulties == 3:
        attempts = 7
    if size == 16:
        attempts = attempts * 2
    return attempts


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
    attempts = difficulties_to_attempts(size, difficulties)
    grid = sudoku.remove_numbers(grid, size, number_of_squares, attempts)
    return grid, full


def draw_board(window, board):
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
        key = 'enter'
    elif event.key == 8:
        key = 'delete'
    return key


def game_loop():
    window = pygame.display.set_mode([window_width, window_height])
    pygame.display.set_caption("Sudoku Game")
    # start with empty 9x9 board
    board = sudoku.create_board(9)
    board = Puzzle(board, 9, 3, board)

    # board and a solution
    board = new_board(9, 3, 2)
    board = Puzzle(board[0], 9, 3, board[1])

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
            if key_pressed == 'delete':
                board.delete_selected()
                key_pressed = None

            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                clicked = board.click(pos)
                if clicked:
                    board.select(clicked[0], clicked[1])
                    key_pressed = None

        if board.selected and key_pressed is not None:
            board.enter_value(key_pressed)
        draw_board(window, board)
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
    pygame.font.init()
    game_loop()
