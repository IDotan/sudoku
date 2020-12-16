"""
| sudoku module to create and solve 9x9 sudoku puzzle
"""
import turtle
from random import randint, shuffle
from time import sleep

global counter


def create_board():
    """
    | initialise empty 9 by 9 grid
    :return: 9x9 grid filled with 0 in every position
    """
    grid = []
    for i in range(9):
        grid.append([0, 0, 0, 0, 0, 0, 0, 0, 0])
    return grid


def check_grid(grid):
    """
    | A function to check if the grid is full
    :param grid: the grid to check
    :return: True when the grid is full with num which are not 0
    """
    for row in range(0, 9):
        for col in range(0, 9):
            if grid[row][col] == 0:
                return False
    return True


def find_square(grid, row, col):
    """
    | Identify which of the 9 squares the program is in and the num in it
    :param grid: the grid to check
    :param row: the row to find which square it's in
    :param col: the column to find which square it's in
    :return: list of num in the square
    """
    if row < 3:
        if col < 3:
            square = [grid[i][0:3] for i in range(0, 3)]
        elif col < 6:
            square = [grid[i][3:6] for i in range(0, 3)]
        else:
            square = [grid[i][6:9] for i in range(0, 3)]
    elif row < 6:
        if col < 3:
            square = [grid[i][0:3] for i in range(3, 6)]
        elif col < 6:
            square = [grid[i][3:6] for i in range(3, 6)]
        else:
            square = [grid[i][6:9] for i in range(3, 6)]
    else:
        if col < 3:
            square = [grid[i][0:3] for i in range(6, 9)]
        elif col < 6:
            square = [grid[i][3:6] for i in range(6, 9)]
        else:
            square = [grid[i][6:9] for i in range(6, 9)]
    square_list = square[0] + square[1] + square[2]
    return square_list


def find_column(grid, col):
    """
    | get the num that are already in the given column
    :param grid: the grid to use
    :param col: the column to get it's num
    :return: list of num in the column
    """
    num_in_col = []
    for i in range(9):
        num_in_col.append(grid[i][col])
    return num_in_col


# A backtracking/recursive function to check all possible combinations of numbers until a solution is found
def solve_grid(grid):
    global counter
    # Find next empty cell
    row, col = 0, 0
    for i in range(0, 81):
        row = i // 9
        col = i % 9
        if grid[row][col] == 0:
            for value in range(1, 10):
                # Check that this value has not already been used on this row
                if not (value in grid[row]):
                    # Check that this value has not already be used on this column
                    num_in_column = find_column(grid, col)
                    if value not in num_in_column:
                        square = find_square(grid, row, col)
                        # Check that this value has not already be used on this 3x3 square
                        if value not in square:
                            grid[row][col] = value
                            if check_grid(grid):
                                counter += 1
                                break
                            else:
                                if solve_grid(grid):
                                    return True
            break
    # reset the position to 0 when cant complete the board
    grid[row][col] = 0


def find_duplicate(lst):
    """
    | check for duplicates in a list
    :param lst: list to check
    :return: True when there is duplicates in the list
    """
    temp_lst = []
    for i in lst:
        if i != 0:
            temp_lst.append(i)
    if len(temp_lst) != len(set(temp_lst)):
        return True
    return False


def check_no_duplicates(grid):
    """
    | check if the sudoku grid have duplicates in it
    :param grid: grid to check in
    :return: True when no duplicates are found
    """
    for row in range(9):
        if find_duplicate(grid[row]):
            return False
    for col in range(9):
        if find_duplicate(find_column(grid, col)):
            return False
    for square_row in [0, 3, 6]:
        for square_col in [0, 3, 6]:
            if find_duplicate(find_square(grid, square_row, square_col)):
                return False
    return True


# A backtracking/recursive function to check all possible combinations of numbers until a solution is found
def fill_grid(grid):
    number_list = [1, 2, 3, 4, 5, 6, 7, 8, 9]
    row, col = 0, 0
    # Find next empty cell
    for i in range(0, 81):
        row = i // 9
        col = i % 9
        if grid[row][col] == 0:
            shuffle(number_list)
            for value in number_list:
                # Check that this value has not already been used on this row
                if not (value in grid[row]):
                    # Check that this value has not already be used on this column
                    num_in_column = find_column(grid, col)
                    if value not in num_in_column:
                        square = find_square(grid, row, col)
                        # Check that this value has not already be used on this 3x3 square
                        if value not in square:
                            grid[row][col] = value
                            if check_grid(grid):
                                return True
                            else:
                                if fill_grid(grid):
                                    return True, grid
            break
    # reset the position to 0 when cant complete the board
    grid[row][col] = 0


def remove_numbers(grid):
    attempts = 5
    global counter
    while attempts > 0:
        # Select a random cell that is not already empty
        row = randint(0, 8)
        col = randint(0, 8)
        while grid[row][col] == 0:
            row = randint(0, 8)
            col = randint(0, 8)

        backup = grid[row][col]
        grid[row][col] = 0

        # Count the number of solutions
        counter = 0
        solve_grid(grid)
        # If there is more then 1 solution revert back the change to the board
        if counter != 1:
            grid[row][col] = backup
            attempts -= 1
    return grid


def new_board(grid):
    full_grid = fill_grid(grid)[1]
    sleep(1)
    return full_grid


def print_board_console(grid):
    for i in range(9):
        temp_line = str(grid[i])[1:-1]
        temp_line = temp_line.replace(',', '')
        print_line = f"{temp_line[0:6]}|{temp_line[6:12]}|{temp_line[12:18]}"
        print(print_line)
        if i in (2, 5, 8):
            line_break = f'{"-" * 6}|{"-" * 6}|{"-" * 6}'
            print(line_break)


def startup():
    grid = create_board()
    full_grid = new_board(grid)
    print_board_console(full_grid)

    print("Sudoku Grid Ready")

    # remove num from board
    grid_to_solve = remove_numbers(full_grid)
    print_board_console(grid_to_solve)


def unsolvable_try(grid=None):
    if grid is None:
        grid = []
        for i in range(9):
            grid.append([1, 0, 0, 0, 0, 0, 0, 0, 0])
    dup = check_no_duplicates(grid)
    if dup is True:
        solve = fill_grid(grid)
        if solve:
            print('solved')
        else:
            print('unsolvable')
    else:
        print('unsolvable-duplicates')


if __name__ == "__main__":
    unsolvable_try()
    startup()

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
    unsolvable_try(temp)
