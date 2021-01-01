"""
| gamepy module for the sudoku game
"""
import sudoku
from copy import deepcopy
import pygame
import pickle
from os import path, remove
import threading

global window, size_9, board, difficulty_pick, user_input_menu, user_input_menu_unsolvable, \
    exit_clicked, mark_incorrect, num_to_find, load_user_sudoku

global window_width, window_height, button_9_data, button_16_data, button_menu_1, button_menu_2, button_menu_3, \
    button_menu_4, button_menu_5, button_menu_exit, buttons_font_size, size_buttons_font_size, num_font, num_font_small

pygame.init()


class Puzzle:
    """
    | class for the sudoku grid
    """
    def __init__(self, grid, size, number_of_squares, solution=False):
        """
        | create the puzzle object
        :param grid: the grid of the board
        :param size: the size of the board
        :param number_of_squares: number of squares in the board
        :param solution: board's solution
        """
        self.base_grid = grid
        self.size = size
        self.number_of_squares = number_of_squares
        self.solution = solution
        self.board_width = window_width - int((window_width * 19.9) / 100)
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
        """
        | reset the board to have only the base numbers
        """
        for row in range(self.size):
            for col in range(self.size):
                self.cubes[row][col].reset_cube()
        global num_to_find
        num_to_find = self.num_to_find

    def draw_board(self):
        """
        | draw the grid lines of the board and then send to draw cube one by one
        """
        gap = int(self.board_width // self.size)
        board_max = gap * self.size
        for i in range(self.size + 1):
            if i in range(0, self.size + 1, self.number_of_squares):
                thick = 4
            else:
                thick = 1
            pos = i * gap
            pygame.draw.line(window, (0, 0, 0), (0, pos), (board_max, pos), thick)
            pygame.draw.line(window, (0, 0, 0), (pos, 0), (pos, board_max), thick)
            # add lower border at the bottom of the board
            if i == self.size:
                pygame.draw.line(window, (0, 0, 0), (0, pos - 4), (board_max, pos - 4), thick)

        for row in range(self.size):
            for col in range(self.size):
                self.cubes[row][col].draw_cube()

    def click(self, pos):
        """
        | find the [row,col] clicked in the board
        :param pos: [x,y] positions of the mouse click
        :return: [row. col] clicked in the board
        """
        if pos[0] < self.board_width and pos[1] < self.board_height:
            gap = int(self.board_width / self.size)
            x = pos[0] // gap
            y = pos[1] // gap
            return int(y), int(x)
        else:
            return None

    def delete_selected(self):
        """
        | delete the number of the selected cube
        """
        if self.selected is not None:
            row, col = self.selected
            self.cubes[row][col].set_val(0)

    def select(self, row, col):
        """
        | select the clicked cube and remove the previous selected one
        :param row: row of the cube to select
        :param col: col of the cube to select
        """
        if self.selected is not None:
            self.cubes[self.selected[0]][self.selected[1]].selected = False
        if row != -1:
            self.cubes[row][col].selected = True
            self.selected = (row, col)

    def enter_value(self, value):
        """
        | enter value to the selected cube
        :param value: int value to enter
        """
        row, col = self.selected
        self.cubes[row][col].set_val(value)

    def get_size(self):
        """
        | get the size of the board
        :return: size of the board
        """
        return self.size

    def get_number_of_squares(self):
        """
        | get the number of squares in the board
        :return: number of squares in the board
        """
        return self.number_of_squares

    def get_num_to_find(self):
        """
        | get the number of empty/incorrect cubes
        :return: number of empty/incorrect cubes
        """
        return self.num_to_find

    def get_board_width(self):
        """
        | get the width of the board
        :return: width of the board
        """
        return self.board_width

    def solve_board(self):
        """
        | reveal the solution of the board
        """
        for row in range(self.size):
            for col in range(self.size):
                self.cubes[row][col].solve_cube()
        global num_to_find
        num_to_find = 0

    def resize(self):
        """
        | resize the board size
        """
        self.board_width = window_width - int((window_width * 19.9) / 100)
        self.board_height = window_height
        for row in range(self.size):
            for col in range(self.size):
                self.cubes[row][col].update_size(self.board_width, self.size)


class Cube:
    """
    | sub-class for cubes in the Puzzle
    """
    def __init__(self, val, row, col, correct_val, board_width, size):
        """
        | create the cube object
        :param val: cubes value
        :param row: row the cube is in its parent grid
        :param col: col the cube is in its parent grid
        :param correct_val: correct value of the cube
        :param board_width: width of the cube parent grid
        :param size: size of the cube parent grid
        """
        self.val = val
        self.row = row
        self.col = col
        self.base = True if val != 0 else False
        self.correct_val = correct_val
        self.cube_width = int(board_width // size)
        self.size = size
        self.selected = False
        if self.val == 0:
            global num_to_find
            num_to_find += 1

    def reset_cube(self):
        """
        | set cube to 0 if its not a base number cube
        """
        if not self.base:
            self.val = 0

    def set_val(self, value):
        """
        | set the value of the cube
        :param value: value to set the cube to
        """
        global num_to_find
        if value == self.correct_val:
            num_to_find -= 1
        elif self.size == 16 and self.correct_val > 9 and self.val == 1:
            temp = self.correct_val - 10
            if value == temp:
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
        if num_to_find == 0:
            self.selected = False

    def get_val(self):
        """
        | get the value of the cube
        :return: cube's value
        """
        return self.val

    def draw_cube(self):
        """
        | draw the cube value and the selected mark when selected
        """
        font_size = num_font
        if self.size == 16:
            font_size = num_font_small
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
        """
        | set cube value to it's correct value
        """
        if not self.base:
            self.val = self.correct_val

    def update_cube(self):
        """
        | update visually the cube
        """
        self.draw_cube()
        x = self.col * self.cube_width
        y = self.row * self.cube_width
        update = pygame.Rect(x, y, x + self.cube_width, y + self.cube_width)
        pygame.display.update(update)

    def update_size(self, board_width, size):
        """
        | update cube size
        :param board_width: width of the board the cube is in
        :param size: the size of the board the cube is in
        """
        self.cube_width = board_width // size


def difficulties_to_attempts(size, difficulties):
    """
    | convert difficulties to attempts
    :param size: size of the board
    :param difficulties: 1-easy 2-medium 3-hard, what arbitrary difficulty the board will be.
    :return: attempts to use in the board creation
    """
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
    """
    | draw side buttons of board size control
    """
    button_9_fill = (113, 183, 253)
    button_16_fill = (140, 140, 140)
    global size_9
    if size_9 is False:
        button_9_fill = (140, 140, 140)
        button_16_fill = (113, 183, 253)
    button_9 = pygame.draw.rect(window, button_9_fill, button_9_data, border_radius=10)
    button_16 = pygame.draw.rect(window, button_16_fill, button_16_data, border_radius=10)
    font_color = (0, 0, 0)
    fnt = pygame.font.SysFont("comicsans", size_buttons_font_size)
    text = fnt.render('9x9', True, font_color)
    window.blit(text, (button_9.center[0] - text.get_width() / 2, button_9.center[1] - text.get_height() / 2))
    text = fnt.render('16x16', True, font_color)
    window.blit(text, (button_16.center[0] - text.get_width() / 2, button_16.center[1] - text.get_height() / 2))


def draw_menu_button(text, button_data, button_fill=(113, 183, 253), size=None, width=0):
    """
    | draw side button
    :param text: string to use for the button
    :param button_data: list of the button position width and height. (x,y,width,height)
    :param button_fill: color of the button. default (113, 183, 253)
    :param size: button font size. default to use buttons_font_size global
    :param width: width of the button fill. default 0
    """
    if size is None:
        size = buttons_font_size
    fnt = pygame.font.SysFont("comicsans", size)
    button_new = pygame.draw.rect(window, button_fill, button_data, border_radius=10, width=width)
    text = fnt.render(text, True, (0, 0, 0))
    window.blit(text, (button_new.center[0] - text.get_width() / 2, button_new.center[1] - text.get_height() / 2))


def draw_difficulty_menu():
    """
    | draw difficulty menu
    """
    draw_menu_button('Easy', button_menu_1)
    draw_menu_button('Medium', button_menu_2)
    draw_menu_button('Hard', button_menu_3)
    draw_menu_button('Cancel', button_menu_4)


def draw_user_input_menu():
    """
    | draw user input menu and unsolvable 'tag' when needed
    """
    if user_input_menu_unsolvable:
        draw_menu_button('unsolvable', (window_width - 165, 120, 130, 40), (255, 0, 0), width=5)
    draw_menu_button('Lock In', button_menu_1)
    draw_menu_button('Restart', button_menu_2)
    draw_menu_button('Cancel', button_menu_3)


def draw_main_menu():
    """
    | draw the main menu
    """
    draw_board_size_buttons()
    draw_menu_button('New Sudoku', button_menu_1, size=buttons_font_size)
    draw_menu_button('Input Sudoku', button_menu_2)
    draw_menu_button('Reset', button_menu_3)
    draw_menu_button('Solve', button_menu_4)
    if mark_incorrect:
        draw_menu_button('Showing mistakes', button_menu_5, (255, 0, 0), size=int((window_width * 2.5) / 100), width=5)
    else:
        draw_menu_button('Hiding mistakes', button_menu_5, (140, 140, 140))


def draw_board():
    """
    | draw the board and send to sub-function according to the needed size bar
    """
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
    """
    | check if the given button was clicked
    :param button: the button to check, list of the button position width and height. (x,y,width,height)
    :param pos: the position clicked [x,y]
    :return: True when button was clicked
    """
    if button[0] <= pos[0] <= button[0] + button[2] \
            and button[1] <= pos[1] <= button[1] + button[3]:
        return True
    return False


def new_board_clicked(difficulty):
    """
    | create new sudoku board
    :param difficulty: 1-easy 2-medium 3-hard, what arbitrary difficulty the board will be.
    """
    global board, num_to_find
    num_to_find = 0
    if size_9:
        board = new_board(9, 3, difficulty)
        board = Puzzle(board[0], 9, 3, board[1])
    else:
        board = new_board(16, 4, difficulty)
        board = Puzzle(board[0], 16, 4, board[1])


def menu_status_difficult(pos):
    """
    | action to take when a button was clicked in the difficult menu.
    | call new_board_clicked() with the selected difficulty or go back according to the clicked button.
    :param pos: position of the click [x,y]
    """
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
    """
    | duplicates check of user input grid and set flags for solving process
    :param grid: user inputted grid to check
    :param size: the size of the grid
    :param squares: number of squares in the grid
    """
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
    """
    | action to take when user click to lock in his sudoku grid.
    | collect the user input to a grid and set load_user_sudoku global flag with the needed data
    """
    global board, load_user_sudoku
    temp = []
    for row in range(board.get_size()):
        temp_row = []
        for col in range(board.get_size()):
            temp_row.append(board.cubes[row][col].get_val())
        temp.append(temp_row)
    size = board.get_size()
    squares = board.get_number_of_squares()
    load_user_sudoku = [temp, size, squares]


def menu_status_user_input(pos):
    """
    | action to take when a button was clicked in the user sudoku input menu
    :param pos: position of the click. [x,y]
    """
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
    """
    | create sudoku grid with 0 in every position
    :param size: size of the board to create. default 9
    :param squares: numbers of squares in the board. default 3
    """
    global board
    # start with empty 9x9 board
    board = sudoku.create_board(size)
    board = Puzzle(board, size, squares, board)


def main_menu(pos):
    """
    | find what button was clicked in the main menu and act accordingly
    :param pos: position of the click
    """
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
    """
    | check if clicked to exit and if not go to the relevant menu
    :param pos: position of the click
    """
    if check_button_clicked(button_menu_exit, pos):
        global exit_clicked
        exit_clicked = True
    elif difficulty_pick:
        menu_status_difficult(pos)
    elif user_input_menu:
        menu_status_user_input(pos)
    else:
        main_menu(pos)


def initialize_globals_sizes(width=900, height=720):
    """
    | initialize global sizes, setup to mid run and easy switch size.
    """
    global window_width, window_height, button_9_data, button_16_data, button_menu_1, button_menu_2, button_menu_3, \
        button_menu_4, button_menu_5, button_menu_exit, buttons_font_size, size_buttons_font_size, \
        num_font, num_font_small
    # ratio 1.25, width = 1.25 * height
    # width need to be in jumps of 100
    # window_width = 1200
    # window_height = 960
    window_width = width
    window_height = height

    general_pos = int((window_width * 18) / 100)
    general_button_width = int((window_width * 16) / 100)
    general_button_height = int((window_height * 6.25) / 100)
    general_button_top_y = int((window_height * 25) / 100)
    general_button_gap = int((window_height * 3.47) / 100)
    size_button_y = int((window_height * 12.5) / 100)
    size_button_width = int((window_width * 7) / 100)
    size_button_height = int((window_height * 5) / 100)

    button_9_data = (window_width - general_pos, size_button_y, size_button_width, size_button_height)
    button_16_data = (window_width - int((window_width * 9) / 100), size_button_y,
                      size_button_width, size_button_height)

    button_menu_1 = (window_width - general_pos, general_button_top_y, general_button_width, general_button_height)
    button_menu_2 = (window_width - general_pos, (general_button_top_y + (general_button_height + general_button_gap)),
                     general_button_width, general_button_height)
    button_menu_3 = (window_width - general_pos, (general_button_top_y +
                     (2 * (general_button_height + general_button_gap))), general_button_width, general_button_height)
    button_menu_4 = (window_width - general_pos, (general_button_top_y +
                     (3 * (general_button_height + general_button_gap))), general_button_width, general_button_height)
    button_menu_5 = (window_width - general_pos, (general_button_top_y +
                     (4 * (general_button_height + general_button_gap))), general_button_width, general_button_height)
    button_menu_exit = (window_width - general_pos, window_height - int(window_height / 10),
                        general_button_width, general_button_height)

    buttons_font_size = int((window_width * 3) / 100)
    size_buttons_font_size = int((window_width * 3.5) / 100)
    num_font = int((window_width * 7.5) / 100)
    num_font_small = int((window_width * 4.5) / 100)


def initialize_globals():
    """
    | initialize globals flags.
    """
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
    """
    | get what key was pressed.
    :param event: pygame.KEYDOWN event to get its key.
    :return: int if number was pressed or string of the action to take.
    """
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
    """
    | load saved game or create new one when there is no save.
    :return: [width, height] to use for the window
    """
    global board, num_to_find
    if path.isfile('save.s'):
        save = pickle.load(open("save.s", "rb"))
        board = save[0]
        num_to_find = save[1]
        windows_board_resize(save[2], save[3])
    else:
        # start with empty 9x9 board
        new_board_clicked(2)


def save_before_exit():
    """
    | save active game before closing if the sudoku is not finished.
    """
    if num_to_find != 0 and user_input_menu is False:
        save = (board, num_to_find, window_width, window_height)
        pickle.dump(save, open("save.s", "wb"))
    elif num_to_find == 0:
        if path.isfile('save.s'):
            remove('save.s')


def delete_button_2_and_3():
    """
    | delete buttons 2&3 from the side bar
    """
    whitespace_buttons_buttons = button_menu_2[0] + button_menu_2[3] - button_menu_3[0]
    delete_buttons_height = button_menu_2[3] + button_menu_3[3] + whitespace_buttons_buttons
    delete_buttons = pygame.Rect(button_menu_2[0], button_menu_2[1], button_menu_2[2], delete_buttons_height)
    pygame.draw.rect(window, (243, 243, 243), delete_buttons)
    pygame.display.update(delete_buttons)


def load_user_sudoku_handler():
    """
    | try to solve user input sudoku in a thread, while showing solving 'icon'.
    | take care of pygame.event to prevent pygame to be unresponsive.
    | allow only exit when solving process is active.
    :return: 'exit' as string when user want to exit.
    """
    t1 = threading.Thread(target=check_user_sudoku_input, args=(*load_user_sudoku,))
    t1.setDaemon(True)
    t1.start()

    delete_button_2_and_3()

    num = 0
    while load_user_sudoku:
        text = 'Solving' + ('.' * num)
        draw_menu_button(text, button_menu_1)
        num += 1
        solving_update = pygame.Rect(button_menu_1)
        pygame.display.update(solving_update)
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


def windows_board_resize(width, height):
    """
    | resize the window and the sudoku board
    :param width: width for the new window
    :param height: height for the window
    """
    global window
    initialize_globals_sizes(width, height)
    board.resize()
    window = pygame.display.set_mode([window_width, window_height], pygame.RESIZABLE)


def fix_resize_scale(width):
    """
    | find if the user want to make the window larger or smaller.
    | fix the size to the 3 presets
    :param width: width the user scaled to
    :return: width, height - new window scale
    """
    height = 0
    scales = [[900, 720], [1000, 800], [1100, 880], [1200, 960]]
    if width < scales[0][0]:
        width, height = scales[0]
    elif width > scales[-1][0]:
        width, height = scales[3]
    else:
        if window_width < width:
            increase = True
        else:
            increase = False
        i = 0
        while i < 3:
            scale_test = scales[i][0], scales[i + 1][0]
            if scale_test[0] <= width <= scale_test[1]:
                if increase:
                    width, height = scales[i + 1]
                else:
                    width, height = scales[i]
                break
            i += 1
    return width, height


def window_resize_event_handler(event):
    """
    | resize the window and the grid
    :param event: pygame.event object
    """
    width, height = event.w, event.h
    if height != window_height and width == window_width:
        width = int(height * 1.25)
    elif width != window_width and height == window_height:
        height = int(width/1.25)
    else:
        height = int(width/1.25)
    # width, height = fix_resize_scale(width)

    windows_board_resize(width, height)


def game_loop():
    """
    | main game loop.
    """
    global window, exit_clicked
    initialize_globals_sizes()
    initialize_globals()

    load_or_create_new()
    window = pygame.display.set_mode([window_width, window_height], pygame.RESIZABLE)
    pygame.display.set_caption("Sudoku Game")
    pygame.display.set_allow_screensaver(True)

    key_pressed = None
    run = True
    load_or_create_new()
    while run:
        global load_user_sudoku
        if type(load_user_sudoku) is list:
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
                if pos[0] < board.get_board_width() and num_to_find != 0:
                    clicked = board.click(pos)
                    if clicked:
                        board.select(clicked[0], clicked[1])
                        key_pressed = None
                else:
                    board.select(-1, -1)
                    click_buttons(pos)

            if event.type == pygame.VIDEORESIZE:
                window_resize_event_handler(event)

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
