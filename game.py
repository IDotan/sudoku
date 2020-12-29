import sudoku
from copy import deepcopy
import pygame
import pickle
from os import path, remove
import threading

global window, size_9, board, difficulty_pick, user_input_menu, user_input_menu_unsolvable, \
    exit_clicked, mark_incorrect, num_to_find, load_user_sudoku

window_width = 1000
window_height = 800
# static buttons positions and size
button_9_data = (window_width - 180, 100, 70, 40)
button_16_data = (window_width - 90, 100, 70, 40)
button_menu_1 = (window_width - 180, 180, 160, 50)
button_menu_2 = (window_width - 180, 250, 160, 50)
button_menu_3 = (window_width - 180, 320, 160, 50)
button_menu_4 = (window_width - 180, 390, 160, 50)
button_menu_5 = (window_width - 180, 460, 160, 50)
button_menu_exit = (window_width - 180, window_height - 80, 160, 50)


pygame.font.init()


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
        self.num_to_find = num_to_find

    def reset_board(self):
        for row in range(self.size):
            for col in range(self.size):
                self.cubes[row][col].reset_cube()
        global num_to_find
        num_to_find = self.num_to_find

    def draw_board(self):
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
                self.cubes[row][col].draw_cube()

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
        if row != -1:
            self.cubes[row][col].selected = True
            self.selected = (row, col)

    def enter_value(self, value):
        row, col = self.selected
        self.cubes[row][col].set_val(value)

    def get_size(self):
        return self.size

    def get_number_of_squares(self):
        return self.number_of_squares

    def get_num_to_find(self):
        return self.num_to_find

    def solve_board(self):
        for row in range(self.size):
            for col in range(self.size):
                self.cubes[row][col].solve_cube()
        global num_to_find
        num_to_find = 0


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
        if self.val == 0:
            global num_to_find
            num_to_find += 1

    def reset_cube(self):
        if not self.base:
            self.val = 0

    def set_val(self, value):
        global num_to_find
        if value == self.correct_val:
            num_to_find -= 1
        elif value != self.correct_val and self.val == self.correct_val:
            num_to_find += 1

        if not self.base:
            if self.size == 9:
                self.val = value
            else:
                # fix to enter numbers in 16x16
                if self.val == 1 and value < 7:
                    temp_val = str(self.val) + str(value)
                    self.val = int(temp_val)
                else:
                    self.val = value

    def get_val(self):
        return self.val

    def draw_cube(self):
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
            elif self.val != self.correct_val and self.correct_val != 0 and mark_incorrect:
                font_color = (255, 0, 0)
            # set to black when the board is complete
            if num_to_find == 0:
                font_color = (0, 0, 0)
            text = fnt.render(str(self.val), True, font_color)
            window.blit(text, (x + (self.cube_width / 2 - text.get_width() / 2),
                               y + (self.cube_width / 2 - text.get_height() / 2)))
        if self.selected:
            pygame.draw.rect(window, (71, 170, 255), (x, y, self.cube_width, self.cube_width), 3)

    def solve_cube(self):
        if not self.base:
            self.val = self.correct_val


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


def draw_board_size_buttons():
    button_9_fill = (113, 183, 253)
    button_16_fill = (140, 140, 140)
    global size_9
    if size_9 is False:
        button_9_fill = (140, 140, 140)
        button_16_fill = (113, 183, 253)
    button_9 = pygame.draw.rect(window, button_9_fill, button_9_data, border_radius=10)
    button_16 = pygame.draw.rect(window, button_16_fill, button_16_data, border_radius=10)
    font_color = (0, 0, 0)
    font_size = 35
    fnt = pygame.font.SysFont("comicsans", font_size)
    text = fnt.render('9x9', True, font_color)
    window.blit(text, (button_9.center[0] - text.get_width() / 2, button_9.center[1] - text.get_height() / 2))
    text = fnt.render('16x16', True, font_color)
    window.blit(text, (button_16.center[0] - text.get_width() / 2, button_16.center[1] - text.get_height() / 2))


def draw_menu_button(text, button_data, button_fill=(113, 183, 253), size=30, width=0):
    fnt = pygame.font.SysFont("comicsans", size)
    button_new = pygame.draw.rect(window, button_fill, button_data, border_radius=10, width=width)
    text = fnt.render(text, True, (0, 0, 0))
    window.blit(text, (button_new.center[0] - text.get_width() / 2, button_new.center[1] - text.get_height() / 2))


def draw_difficulty_menu():
    draw_menu_button('Easy', button_menu_1)
    draw_menu_button('Medium', button_menu_2)
    draw_menu_button('Hard', button_menu_3)
    draw_menu_button('Cancel', button_menu_4)


def draw_user_input_menu():
    if user_input_menu_unsolvable:
        draw_menu_button('unsolvable', (window_width - 165, 120, 130, 40), (255, 0, 0), width=5)
    draw_menu_button('Lock In', button_menu_1)
    draw_menu_button('Restart', button_menu_2)
    draw_menu_button('Cancel', button_menu_3)


def draw_main_menu():
    draw_board_size_buttons()
    draw_menu_button('New Sudoku', button_menu_1)
    draw_menu_button('Input Sudoku', button_menu_2)
    draw_menu_button('Reset', button_menu_3)
    draw_menu_button('Solve', button_menu_4)
    if mark_incorrect:
        draw_menu_button('Showing mistakes', button_menu_5, (255, 0, 0), size=25, width=5)
    else:
        draw_menu_button('Hiding incorrect', button_menu_5, (140, 140, 140))


def draw_board():
    window.fill((243, 243, 243))

    if difficulty_pick:
        draw_difficulty_menu()
    elif user_input_menu:
        draw_user_input_menu()
    else:
        draw_main_menu()

    draw_menu_button('Exit', button_menu_exit, (140, 140, 140))
    board.draw_board()


def check_button_clicked(button, pos):
    if button[0] <= pos[0] <= button[0] + button[2] \
            and button[1] <= pos[1] <= button[1] + button[3]:
        return True
    return False


def new_board_clicked(difficulty):
    global board, num_to_find
    num_to_find = 0
    if size_9:
        board = new_board(9, 3, difficulty)
        board = Puzzle(board[0], 9, 3, board[1])
    else:
        board = new_board(16, 4, difficulty)
        board = Puzzle(board[0], 16, 4, board[1])


def menu_status_difficult(pos):
    global difficulty_pick
    if check_button_clicked(button_menu_1, pos):
        new_board_clicked(1)
        difficulty_pick = False
    elif check_button_clicked(button_menu_2, pos):
        new_board_clicked(2)
        difficulty_pick = False
    elif check_button_clicked(button_menu_3, pos):
        new_board_clicked(3)
        difficulty_pick = False
    elif check_button_clicked(button_menu_4, pos):
        difficulty_pick = False


def check_user_sudoku_input(grid, size, squares):
    global user_input_menu, board, user_input_menu_unsolvable, num_to_find, load_user_sudoku
    solution = False
    load_user_sudoku = True
    if sudoku.check_no_duplicates(grid, squares):
        solution = sudoku.modular_solve(deepcopy(grid), size, squares)
    if solution is not False:
        num_to_find = 0
        board = Puzzle(grid, size, squares, solution)
        user_input_menu = False
        user_input_menu_unsolvable = False
    else:
        user_input_menu_unsolvable = True
    load_user_sudoku = None


def menu_status_user_input_lock_clicked():
    global board, load_user_sudoku
    temp = []
    for row in range(board.get_size()):
        temp_row = []
        for col in range(board.get_size()):
            temp_row.append(board.cubes[row][col].get_val())
        temp.append(temp_row)
    size = board.get_size()
    squares = board.get_number_of_squares()
    load_user_sudoku = (temp, size, squares)


def menu_status_user_input(pos):
    global user_input_menu, board, user_input_menu_unsolvable
    if check_button_clicked(button_menu_1, pos):
        menu_status_user_input_lock_clicked()
    elif check_button_clicked(button_menu_2, pos):
        board.reset_board()
        user_input_menu_unsolvable = False
        return
    elif check_button_clicked(button_menu_3, pos):
        user_input_menu = False
        user_input_menu_unsolvable = False


def create_empty_board(size=9, squares=3):
    global board
    # start with empty 9x9 board
    board = sudoku.create_board(size)
    board = Puzzle(board, size, squares, board)


def main_menu(pos):
    global size_9, board, difficulty_pick, user_input_menu, mark_incorrect
    if check_button_clicked(button_9_data, pos):
        size_9 = True
    elif check_button_clicked(button_16_data, pos):
        size_9 = False
    elif check_button_clicked(button_menu_1, pos):
        difficulty_pick = True
    elif check_button_clicked(button_menu_2, pos):
        if size_9:
            create_empty_board()
        else:
            create_empty_board(16, 4)
        user_input_menu = True
    elif check_button_clicked(button_menu_3, pos):
        global board
        board.reset_board()
    elif check_button_clicked(button_menu_4, pos):
        board.solve_board()
    elif check_button_clicked(button_menu_5, pos):
        if mark_incorrect:
            mark_incorrect = False
        else:
            mark_incorrect = True


def click_buttons(pos):
    if check_button_clicked(button_menu_exit, pos):
        global exit_clicked
        exit_clicked = True
    elif difficulty_pick:
        menu_status_difficult(pos)
    elif user_input_menu:
        menu_status_user_input(pos)
    else:
        main_menu(pos)


def initialize_globals():
    global size_9, difficulty_pick, user_input_menu, user_input_menu_unsolvable, \
        exit_clicked, mark_incorrect, num_to_find, load_user_sudoku
    size_9 = True
    difficulty_pick = False
    user_input_menu = False
    user_input_menu_unsolvable = False
    exit_clicked = False
    mark_incorrect = False
    num_to_find = 0
    load_user_sudoku = None


def get_key(event):
    key = None
    try:
        key = int(event.unicode)
    except ValueError:
        # if event.key == 13:
        #     key = 'enter'
        if event.key == 8:
            key = 'delete'
    return key


def load_or_create_new():
    global board, num_to_find
    if path.isfile('save.s'):
        save = pickle.load(open("save.s", "rb"))
        board = save[0]
        num_to_find = save[1]
    else:
        # start with empty 9x9 board
        new_board_clicked(2)


def save_before_exit():
    if num_to_find != 0 and user_input_menu is False:
        save = (board, num_to_find)
        pickle.dump(save, open("save.s", "wb"))
    elif num_to_find == 0:
        if path.isfile('save.s'):
            remove('save.s')


def load_user_sudoku_handler():
    grid, size, squares = load_user_sudoku[0], load_user_sudoku[1], load_user_sudoku[2]
    t1 = threading.Thread(target=check_user_sudoku_input, args=(grid, size, squares))
    t1.setDaemon(True)
    t1.start()
    num = 0
    draw_menu_button('', button_menu_2, (243, 243, 243))
    draw_menu_button('', button_menu_3, (243, 243, 243))
    while load_user_sudoku:
        # pygame.event.pump()
        text = 'Solving' + ('.' * num)
        draw_menu_button(text, button_menu_1)
        num += 1
        pygame.display.update()
        pygame.time.wait(2000)
        if num == 4:
            num = 0
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return 'exit'
            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                if check_button_clicked(button_menu_exit, pos):
                    return 'exit'


def game_loop():
    global window, exit_clicked
    window = pygame.display.set_mode([window_width, window_height])
    pygame.display.set_caption("Sudoku Game")

    initialize_globals()

    key_pressed = None
    run = True
    load_or_create_new()
    while run:
        global load_user_sudoku
        if type(load_user_sudoku) is tuple:
            task = load_user_sudoku_handler()
            if task == 'exit':
                break
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
                if pos[0] < 800 and num_to_find != 0:
                    clicked = board.click(pos)
                    if clicked:
                        board.select(clicked[0], clicked[1])
                        key_pressed = None
                else:
                    board.select(-1, -1)
                    click_buttons(pos)

        if exit_clicked:
            break
        if board.selected and key_pressed is not None:
            board.enter_value(key_pressed)
            key_pressed = None

        draw_board()
        pygame.display.update()

    save_before_exit()
    pygame.quit()


if __name__ == "__main__":
    game_loop()
