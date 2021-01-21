"""
| pygame module for the sudoku game
"""
import sudoku
from copy import deepcopy
import pygame
import pickle
from os import path, remove
import threading

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
        self.__base_grid = grid
        self.__size = size
        self.__number_of_squares = number_of_squares
        self.__solution = solution
        self.__board_width = game_window.window_width - int((game_window.window_width * 19.9) / 100)
        self.__board_height = game_window.window_height
        self.selected = None
        self.__solution = solution if solution is not False else \
            sudoku.modular_solve(deepcopy(grid), size, number_of_squares)
        if self.__solution is not False:
            self.cubes = [[Cube(self.__base_grid[row][col], row, col, self.__solution[row][col], self.__board_width,
                                self.__size) for col in range(size)] for row in range(size)]
        else:
            self.cubes = [[Cube(self.__base_grid[row][col], row, col, None, self.__board_width, self.__size)
                           for col in range(size)] for row in range(size)]
        self.__num_to_find = game_window.num_to_find

    def reset_board(self):
        """
        | reset the board to have only the base numbers
        """
        for row in range(self.__size):
            for col in range(self.__size):
                self.cubes[row][col].reset_cube()
        game_window.num_to_find = self.__num_to_find

    def draw_board(self):
        """
        | draw the grid lines of the board and then send to draw cube one by one
        """
        gap = int(self.__board_width // self.__size)
        board_max = gap * self.__size
        for i in range(self.__size + 1):
            if i in range(0, self.__size + 1, self.__number_of_squares):
                thick = 4
            else:
                thick = 1
            pos = i * gap
            pygame.draw.line(game_window.window, (0, 0, 0), (0, pos), (board_max, pos), thick)
            pygame.draw.line(game_window.window, (0, 0, 0), (pos, 0), (pos, board_max), thick)
            # add lower border at the bottom of the board
            if i == self.__size:
                pygame.draw.line(game_window.window, (0, 0, 0), (0, pos - 2), (board_max, pos - 2), thick)

        for row in range(self.__size):
            for col in range(self.__size):
                self.cubes[row][col].draw_cube()

    def click(self, pos):
        """
        | find the [row,col] clicked in the board
        :param pos: [x,y] positions of the mouse click
        :return: [row. col] clicked in the board
        """
        if pos[0] < self.__board_width and pos[1] < self.__board_height:
            gap = int(self.__board_width / self.__size)
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
            self.cubes[self.selected[0]][self.selected[1]].set_selected(False)
        if row != -1:
            self.cubes[row][col].set_selected(True)
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
        return self.__size

    def get_number_of_squares(self):
        """
        | get the number of squares in the board
        :return: number of squares in the board
        """
        return self.__number_of_squares

    def get_num_to_find(self):
        """
        | get the number of empty/incorrect cubes
        :return: number of empty/incorrect cubes
        """
        return self.__num_to_find

    def get_board_width(self):
        """
        | get the width of the board
        :return: width of the board
        """
        return self.__board_width

    def solve_board(self):
        """
        | reveal the solution of the board
        """
        for row in range(self.__size):
            for col in range(self.__size):
                self.cubes[row][col].solve_cube()
        game_window.num_to_find = 0

    def resize(self):
        """
        | resize the board size
        """
        self.__board_width = game_window.window_width - int((game_window.window_width * 19.9) / 100)
        self.__board_height = game_window.window_height
        for row in range(self.__size):
            for col in range(self.__size):
                self.cubes[row][col].update_size(self.__board_width, self.__size)


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
        self.__val = val
        self.__row = row
        self.__col = col
        self.__base = True if val != 0 else False
        self.__correct_val = correct_val
        self.__cube_width = int(board_width // size)
        self.__size = size
        self.__selected = False
        if self.__val == 0:
            game_window.num_to_find += 1

    def reset_cube(self):
        """
        | set cube to 0 if its not a base number cube
        """
        if not self.__base:
            self.__val = 0

    def set_val(self, value):
        """
        | set the value of the cube
        :param value: value to set the cube to
        """
        if value == self.__correct_val:
            game_window.num_to_find -= 1
        elif self.__size == 16 and self.__correct_val > 9 and self.__val == 1:
            temp = self.__correct_val - 10
            if value == temp:
                game_window.num_to_find -= 1
        elif value != self.__correct_val and self.__val == self.__correct_val:
            game_window.num_to_find += 1

        if not self.__base:
            if self.__size == 9:
                self.__val = value
            else:
                # fix to enter numbers in 16x16
                if self.__val == 1 and value < 7:
                    temp_val = str(self.__val) + str(value)
                    self.__val = int(temp_val)
                else:
                    self.__val = value
        if game_window.num_to_find == 0:
            self.__selected = False

    def set_selected(self, flag):
        """
        | set the cube to be selected or not
        :param flag: bool, True when selected
        """
        self.__selected = flag

    def get_val(self):
        """
        | get the value of the cube
        :return: cube's value
        """
        return self.__val

    def draw_cube(self):
        """
        | draw the cube value and the selected mark when selected
        """
        font_size = game_window.num_font
        if self.__size == 16:
            font_size = game_window.num_font_small
        fnt = pygame.font.SysFont("comicsans", font_size)
        x = self.__col * self.__cube_width
        y = self.__row * self.__cube_width

        if not (self.__val == 0):
            font_color = (113, 183, 253)
            # black for base number
            if self.__base is True:
                font_color = (0, 0, 0)
            # red font when incorrect number
            elif self.__val != self.__correct_val and self.__correct_val != 0 and game_window.mark_incorrect:
                font_color = (255, 0, 0)
            # set to black when the board is complete
            if game_window.num_to_find == 0:
                font_color = (0, 0, 0)
            text = fnt.render(str(self.__val), True, font_color)
            game_window.window.blit(text, (x + (self.__cube_width / 2 - text.get_width() / 2),
                                           y + (self.__cube_width / 2 - text.get_height() / 2)))
        if self.__selected:
            pygame.draw.rect(game_window.window, (71, 170, 255), (x, y, self.__cube_width, self.__cube_width), 3)

    def solve_cube(self):
        """
        | set cube value to it's correct value
        """
        if not self.__base:
            self.__val = self.__correct_val

    def update_cube(self):
        """
        | update the cube visually
        """
        x = self.__col * self.__cube_width
        y = self.__row * self.__cube_width

        clear_size = [(game_window.window_height * 0.5 / 100), (game_window.window_height * 1 / 100)]
        game_window.window.fill((243, 243, 243),
                                pygame.Rect(x + clear_size[0], y + clear_size[0], self.__cube_width - clear_size[1],
                                            self.__cube_width - clear_size[1]))
        self.draw_cube()
        update = pygame.Rect(x, y, x + self.__cube_width, y + self.__cube_width)
        pygame.display.update(update)

    def update_size(self, board_width, size):
        """
        | update cube size
        :param board_width: width of the board the cube is in
        :param size: the size of the board the cube is in
        """
        self.__cube_width = board_width // size


class GameGlobals:
    """
    | class to store 'globals' in
    """
    def __init__(self):
        """
        | create global object
        """
        self.size_9 = True
        self.difficulty_pick = False
        self.user_input_menu = False
        self.user_input_menu_unsolvable = False
        self.exit_clicked = False
        self.mark_incorrect = False
        self.num_to_find = 0
        self.load_user_sudoku = None
        self.scale_toggle = True
        self.num_solving = False

        self.window_width = 0
        self.window_height = 0

        self.button_9_data = (0, 0, 0, 0)
        self.button_16_data = (0, 0, 0, 0)
        self.button_menu_1 = (0, 0, 0, 0)
        self.button_menu_2 = (0, 0, 0, 0)
        self.button_menu_3 = (0, 0, 0, 0)
        self.button_menu_4 = (0, 0, 0, 0)
        self.button_menu_5 = (0, 0, 0, 0)
        self.button_menu_exit = (0, 0, 0, 0)
        self.button_scales_toggle = (0, 0, 0, 0)
        self.buttons_font_size = 0
        self.size_buttons_font_size = 0
        self.num_font = 0
        self.num_font_small = 0

        self.set_sizes()

        self.board = None
        self.window = None

    def set_sizes(self, width=900, height=720):
        """
        | set/change the scales
        :param width: window width to use. default 900
        :param height: window height to use. default 720
        """
        self.window_width = width
        self.window_height = height

        general_pos = self.window_width - int((self.window_width * 18) / 100)
        general_button_width = int((self.window_width * 16) / 100)
        general_button_height = int((self.window_height * 6.25) / 100)
        general_button_top_y = int((self.window_height * 25) / 100)
        general_button_gap = int((self.window_height * 3.47) / 100)
        size_button_y = int((self.window_height * 12.5) / 100)
        size_button_width = int((self.window_width * 7) / 100)
        size_button_height = int((self.window_height * 5) / 100)

        self.button_9_data = (general_pos, size_button_y, size_button_width, size_button_height)
        self.button_16_data = (self.window_width - int((self.window_width * 9) / 100), size_button_y,
                               size_button_width, size_button_height)
        self.button_menu_1 = (general_pos, general_button_top_y, general_button_width, general_button_height)
        self.button_menu_2 = (general_pos, (general_button_top_y + (general_button_height + general_button_gap)),
                              general_button_width, general_button_height)
        self.button_menu_3 = (general_pos, (general_button_top_y +
                                            (2 * (general_button_height + general_button_gap))), general_button_width,
                              general_button_height)
        self.button_menu_4 = (general_pos, (general_button_top_y +
                                            (3 * (general_button_height + general_button_gap))), general_button_width,
                              general_button_height)
        self.button_menu_5 = (general_pos, (general_button_top_y +
                                            (4 * (general_button_height + general_button_gap))), general_button_width,
                              general_button_height)
        self.button_menu_exit = (general_pos, self.window_height - int(self.window_height / 10),
                                 general_button_width, general_button_height)
        self.button_scales_toggle = (general_pos, (self.button_menu_exit[1] - int(general_button_gap / 3) -
                                                   general_button_height), general_button_width, general_button_height)

        self.buttons_font_size = int((self.window_width * 3) / 100)
        self.size_buttons_font_size = int((self.window_width * 3.5) / 100)
        self.num_font = int((self.window_width * 7.5) / 100)
        self.num_font_small = int((self.window_width * 4.5) / 100)


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
    if game_window.size_9 is False:
        button_9_fill = (140, 140, 140)
        button_16_fill = (113, 183, 253)
    button_9 = pygame.draw.rect(game_window.window, button_9_fill, game_window.button_9_data, border_radius=10)
    button_16 = pygame.draw.rect(game_window.window, button_16_fill, game_window.button_16_data, border_radius=10)
    font_color = (0, 0, 0)
    fnt = pygame.font.SysFont("comicsans", game_window.size_buttons_font_size)
    text = fnt.render('9x9', True, font_color)
    game_window.window.blit(text,
                            (button_9.center[0] - text.get_width() / 2, button_9.center[1] - text.get_height() / 2))
    text = fnt.render('16x16', True, font_color)
    game_window.window.blit(text,
                            (button_16.center[0] - text.get_width() / 2, button_16.center[1] - text.get_height() / 2))


def draw_menu_button(text, button_data, button_fill=(113, 183, 253), size=None, width=0):
    """
    | draw side button
    :param text: string to use for the button
    :param button_data: list of the button position width and height. (x,y,width,height)
    :param button_fill: color of the button. default (113, 183, 253)
    :param size: button font size. default to use game_window.buttons_font_size
    :param width: width of the button fill. default 0
    """
    if size is None:
        size = game_window.buttons_font_size
    fnt = pygame.font.SysFont("comicsans", size)
    button_new = pygame.draw.rect(game_window.window, button_fill, button_data, border_radius=10, width=width)
    text = fnt.render(text, True, (0, 0, 0))
    game_window.window.blit(text,
                            (button_new.center[0] - text.get_width() / 2, button_new.center[1] - text.get_height() / 2))


def draw_difficulty_menu():
    """
    | draw difficulty menu
    """
    draw_menu_button('Easy', game_window.button_menu_1)
    draw_menu_button('Medium', game_window.button_menu_2)
    draw_menu_button('Hard', game_window.button_menu_3)
    draw_menu_button('Cancel', game_window.button_menu_4)


def draw_user_input_menu():
    """
    | draw user input menu and unsolvable 'tag' when needed
    """
    if game_window.user_input_menu_unsolvable:
        draw_menu_button('unsolvable', (int(game_window.window_width - (game_window.window_width * 17) / 100),
                                        int((game_window.window_height * 16) / 100),
                                        int((game_window.window_width * 14) / 100),
                                        int((game_window.window_height * 5) / 100)), (255, 0, 0), width=5)
    draw_menu_button('Lock In', game_window.button_menu_1)
    draw_menu_button('Restart', game_window.button_menu_2)
    if game_window.num_solving:
        draw_menu_button('Showing work', game_window.button_menu_3)
    else:
        draw_menu_button('Hiding work', game_window.button_menu_3)
    draw_menu_button('Cancel', game_window.button_menu_4)


def draw_main_menu():
    """
    | draw the main menu
    """
    draw_board_size_buttons()
    draw_menu_button('New Sudoku', game_window.button_menu_1, size=game_window.buttons_font_size)
    draw_menu_button('Input Sudoku', game_window.button_menu_2)
    draw_menu_button('Reset', game_window.button_menu_3)
    draw_menu_button('Solve', game_window.button_menu_4)
    if game_window.mark_incorrect:
        draw_menu_button('Showing mistakes', game_window.button_menu_5, (255, 0, 0),
                         size=int((game_window.window_width * 2.5) / 100), width=5)
    else:
        draw_menu_button('Hiding mistakes', game_window.button_menu_5, (140, 140, 140))


def draw_board():
    """
    | draw the board and send to sub-function according to the needed size bar
    """
    game_window.window.fill((243, 243, 243))

    if game_window.difficulty_pick:
        draw_difficulty_menu()
    elif game_window.user_input_menu:
        draw_user_input_menu()
    else:
        draw_main_menu()

    if game_window.scale_toggle:
        draw_menu_button('Preset scales', game_window.button_scales_toggle, (140, 140, 140))
    else:
        draw_menu_button('Free scaling', game_window.button_scales_toggle, (0, 210, 14), width=5)
    draw_menu_button('Exit', game_window.button_menu_exit, (140, 140, 140))
    game_window.board.draw_board()


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
    game_window.num_to_find = 0
    if game_window.size_9:
        board = new_board(9, 3, difficulty)
        game_window.board = Puzzle(board[0], 9, 3, board[1])
    else:
        board = new_board(16, 4, difficulty)
        game_window.board = Puzzle(board[0], 16, 4, board[1])


def menu_status_difficult(pos):
    """
    | action to take when a button was clicked in the difficult menu.
    | call new_board_clicked() with the selected difficulty or go back according to the clicked button.
    :param pos: position of the click [x,y]
    """
    if check_button_clicked(game_window.button_menu_1, pos):
        new_board_clicked(1)
        game_window.difficulty_pick = False
    elif check_button_clicked(game_window.button_menu_2, pos):
        new_board_clicked(2)
        game_window.difficulty_pick = False
    elif check_button_clicked(game_window.button_menu_3, pos):
        new_board_clicked(3)
        game_window.difficulty_pick = False
    elif check_button_clicked(game_window.button_menu_4, pos):
        game_window.difficulty_pick = False


def check_user_sudoku_input(grid, size, squares):
    """
    | duplicates check of user input grid and set flags for solving process
    :param grid: user inputted grid to check
    :param size: the size of the grid
    :param squares: number of squares in the grid
    """
    solution = False
    game_window.load_user_sudoku = True
    if sudoku.check_no_duplicates(grid, squares):
        if game_window.num_solving:
            solution = sudoku.modular_solve(deepcopy(grid), size, squares, board=game_window.board)
        else:
            solution = sudoku.modular_solve(deepcopy(grid), size, squares)
    if solution is not False:
        game_window.num_to_find = 0
        game_window.board = Puzzle(grid, size, squares, solution)
        game_window.user_input_menu = False
        game_window.user_input_menu_unsolvable = False
    else:
        game_window.user_input_menu_unsolvable = True
    game_window.load_user_sudoku = None


def menu_status_user_input_lock_clicked():
    """
    | action to take when user click to lock in his sudoku grid.
    | collect the user input to a grid and set game_window.load_user_sudoku flag with the needed data
    """
    temp = []
    for row in range(game_window.board.get_size()):
        temp_row = []
        for col in range(game_window.board.get_size()):
            temp_row.append(game_window.board.cubes[row][col].get_val())
        temp.append(temp_row)
    size = game_window.board.get_size()
    squares = game_window.board.get_number_of_squares()
    game_window.load_user_sudoku = [temp, size, squares]


def menu_status_user_input(pos):
    """
    | action to take when a button was clicked in the user sudoku input menu
    :param pos: position of the click. [x,y]
    """
    if check_button_clicked(game_window.button_menu_1, pos):
        menu_status_user_input_lock_clicked()
    elif check_button_clicked(game_window.button_menu_2, pos):
        game_window.board.reset_board()
        game_window.user_input_menu_unsolvable = False
        return
    elif check_button_clicked(game_window.button_menu_3, pos):
        if game_window.num_solving is True:
            game_window.num_solving = False
        else:
            game_window.num_solving = True
    elif check_button_clicked(game_window.button_menu_4, pos):
        game_window.user_input_menu = False
        game_window.user_input_menu_unsolvable = False


def create_empty_board(size=9, squares=3):
    """
    | create sudoku grid with 0 in every position
    :param size: size of the board to create. default 9
    :param squares: numbers of squares in the board. default 3
    """
    # start with empty 9x9 board
    game_window.board = sudoku.create_board(size)
    game_window.board = Puzzle(game_window.board, size, squares, game_window.board)


def main_menu(pos):
    """
    | find what button was clicked in the main menu and act accordingly
    :param pos: position of the click
    """
    if check_button_clicked(game_window.button_9_data, pos):
        game_window.size_9 = True
    elif check_button_clicked(game_window.button_16_data, pos):
        game_window.size_9 = False
    elif check_button_clicked(game_window.button_menu_1, pos):
        game_window.difficulty_pick = True
    elif check_button_clicked(game_window.button_menu_2, pos):
        if game_window.size_9:
            create_empty_board()
        else:
            create_empty_board(16, 4)
        game_window.user_input_menu = True
    elif check_button_clicked(game_window.button_menu_3, pos):
        game_window.board.reset_board()
    elif check_button_clicked(game_window.button_menu_4, pos):
        game_window.board.solve_board()
    elif check_button_clicked(game_window.button_menu_5, pos):
        if game_window.mark_incorrect:
            game_window.mark_incorrect = False
        else:
            game_window.mark_incorrect = True


def click_buttons(pos):
    """
    | check if clicked to exit and if not go to the relevant menu
    :param pos: position of the click
    """
    if check_button_clicked(game_window.button_menu_exit, pos):
        game_window.exit_clicked = True
    elif check_button_clicked(game_window.button_scales_toggle, pos):
        if game_window.scale_toggle:
            game_window.scale_toggle = False
        else:
            game_window.scale_toggle = True
            window_resize_event_handler(game_window.window_width, game_window.window_height)
    elif game_window.difficulty_pick:
        menu_status_difficult(pos)
    elif game_window.user_input_menu:
        menu_status_user_input(pos)
    else:
        main_menu(pos)


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
    if path.isfile('save.s'):
        save = pickle.load(open("save.s", "rb"))
        game_window.board = save[0]
        game_window.num_to_find = save[1]
        game_window.set_sizes(save[2], save[3])
    else:
        # start with empty 9x9 board
        new_board_clicked(2)


def save_before_exit():
    """
    | save active game before closing if the sudoku is not finished.
    """
    if game_window.num_to_find != 0 and game_window.user_input_menu is False:
        save = (game_window.board, game_window.num_to_find, game_window.window_width, game_window.window_height)
        pickle.dump(save, open("save.s", "wb"))
    elif game_window.num_to_find == 0:
        if path.isfile('save.s'):
            remove('save.s')


def delete_button_when_solving():
    """
    | delete buttons 2&3 from the side bar
    """
    delete_buttons_height = game_window.button_menu_exit[1] - game_window.button_menu_2[1]
    delete_buttons = pygame.Rect(game_window.button_menu_2[0], game_window.button_menu_2[1],
                                 game_window.button_menu_2[2], delete_buttons_height)
    pygame.draw.rect(game_window.window, (243, 243, 243), delete_buttons)
    pygame.display.update(delete_buttons)


def load_user_sudoku_handler():
    """
    | try to solve user input sudoku in a thread, while showing solving 'icon'.
    | take care of pygame.event to prevent pygame to be unresponsive.
    | allow only exit when solving process is active.
    :return: 'exit' as string when user want to exit.
    """
    t1 = threading.Thread(target=check_user_sudoku_input, args=(*game_window.load_user_sudoku,))
    t1.setDaemon(True)
    t1.start()

    delete_button_when_solving()

    num = 0
    while game_window.load_user_sudoku:
        text = 'Solving' + ('.' * num)
        draw_menu_button(text, game_window.button_menu_1)
        num += 1
        solving_update = pygame.Rect(game_window.button_menu_1)
        pygame.display.update(solving_update)
        pygame.time.wait(2000)
        if num == 4:
            num = 0
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return 'exit'
            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                if check_button_clicked(game_window.button_menu_exit, pos):
                    return 'exit'


def windows_board_resize(width, height):
    """
    | resize the window and the sudoku board
    :param width: width for the new window
    :param height: height for the window
    """
    game_window.set_sizes(width, height)
    game_window.board.resize()
    game_window.window = pygame.display.set_mode([game_window.window_width, game_window.window_height],
                                                 pygame.RESIZABLE)


def fix_resize_scale(width):
    """
    | find if the user want to make the window larger or smaller.
    | fix the size to the 4 presets
    :param width: width the user scaled to
    :return: width, height - new window scale
    """
    height = 0
    scales = [[900, 720], [1000, 800], [1100, 880], [1200, 960]]
    if width < scales[0][0]:
        width, height = scales[0]
    elif width > scales[-1][0]:
        width, height = scales[-1]
    else:
        if game_window.window_width < width:
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


def window_resize_event_handler(width, height):
    """
    | resize the window and the grid
    :param width: new window width
    :param height: new window height
    """
    if height != game_window.window_height and width == game_window.window_width:
        width = int(height * 1.25)
    elif width != game_window.window_width and height == game_window.window_height:
        height = int(width / 1.25)
    else:
        height = int(width / 1.25)
    if game_window.scale_toggle:
        width, height = fix_resize_scale(width)

    windows_board_resize(width, height)


def game_loop():
    """
    | main game loop.
    """
    load_or_create_new()
    game_window.window = pygame.display.set_mode([game_window.window_width, game_window.window_height],
                                                 pygame.RESIZABLE)
    pygame.display.set_caption("Sudoku Game")
    pygame.display.set_allow_screensaver(True)

    key_pressed = None
    run = True
    load_or_create_new()
    while run:
        if type(game_window.load_user_sudoku) is list:
            task = load_user_sudoku_handler()
            if task == 'exit':
                break
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.KEYDOWN:
                key_pressed = get_key(event)
            if key_pressed == 'delete':
                game_window.board.delete_selected()
                key_pressed = None

            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                if pos[0] < game_window.board.get_board_width() and game_window.num_to_find != 0:
                    clicked = game_window.board.click(pos)
                    if clicked:
                        game_window.board.select(clicked[0], clicked[1])
                        key_pressed = None
                else:
                    game_window.board.select(-1, -1)
                    click_buttons(pos)

            if event.type == pygame.VIDEORESIZE:
                window_resize_event_handler(event.w, event.h)

        if game_window.exit_clicked:
            break
        if game_window.board.selected and key_pressed is not None:
            game_window.board.enter_value(key_pressed)
            key_pressed = None

        draw_board()
        pygame.display.update()

    save_before_exit()
    pygame.quit()


game_window = GameGlobals()

if __name__ == "__main__":
    game_loop()
