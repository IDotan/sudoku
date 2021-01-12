"""
| sudoku module to create and solve 9x9 sudoku puzzle.
"""
from random import randint, shuffle

# global used in modular_solve_after_remove() and remove_numbers() to check there is only 1 solution
global counter


def create_board(size):
    """
    | initialise empty sudoku grid.
    :var size: size of the grid to make.
    :return: grid filled with 0 in every position.
    """
    grid = []
    for i in range(size):
        row = []
        for j in range(size):
            row.append(0)
        grid.append(row)
    return grid


def find_square(grid, row, col, number_of_squares):
    """
    | Identify which of the 9 squares the program is in and the num in it.
    :param grid: the grid to check.
    :param row: the row to find which square it's in.
    :param col: the column to find which square it's in.
    :param number_of_squares: the number of square a row/column of the bord is split to (3/4...).
    :return: list of num in the square.
    """
    # divide to go to the start of the square
    # square_row = row//number_of_squares
    # square_col = col//number_of_squares
    square_list = []
    for i in range(number_of_squares):
        for j in range(number_of_squares):
            # go over each col for every row and add the num to the list
            square_list.append(grid[row + i][col + j])
    return square_list


def find_column(grid, col):
    """
    | get the num that are already in the given column.
    :param grid: the grid to use.
    :param col: the column to get it's num.
    :return: list of num in the column.
    """
    num_in_col = []
    for i in range(9):
        num_in_col.append(grid[i][col])
    return num_in_col


def find_duplicate(lst):
    """
    | check for duplicates in a list.
    :param lst: list to check.
    :return: True when there is duplicates in the list.
    """
    if len(lst) == 0:
        return False
    temp_lst = []
    for i in lst:
        if i != 0:
            temp_lst.append(i)
    if len(temp_lst) != len(set(temp_lst)):
        return True
    return False


def check_no_duplicates(grid, number_of_squares):
    """
    | check if the sudoku grid have duplicates in it.
    :param grid: grid to check in.
    :param number_of_squares: the number of square a row/column of the bord is split to (3/4...).
    :return: True when no duplicates are found.
    """
    size = len(grid)
    for row in range(size):
        if find_duplicate(grid[row]):
            return False
    for col in range(size):
        if find_duplicate(find_column(grid, col)):
            return False
    for square_row in range(0, size, number_of_squares):
        for square_col in range(0, size, number_of_squares):
            if find_duplicate(find_square(grid, square_row, square_col, number_of_squares)):
                return False
    return True


def modular_solve_after_remove(grid, size, number_of_squares):
    """
    | fill given sudoku board.
    :param grid: grid to try to solve.
    :param size: the sudoku row and column length (9/16...).
    :param number_of_squares: the number of square a row/column of the bord is split to (3/4...).
    """
    global counter
    for row in range(size):
        for col in range(size):
            if grid[row][col] == 0:
                for value in range(1, size + 1):
                    if modular_is_possible(grid, row, col, value, size, number_of_squares):
                        grid[row][col] = value
                        if modular_solve_after_remove(grid, size, number_of_squares):
                            counter += 1
                            grid[row][col] = 0
                            break
                        grid[row][col] = 0
                return False
    return True


def remove_numbers(grid, size, number_of_squares, attempts=5):
    """
    | remove numbers from a sudoku board one by one to create a new sudoku puzzle with only one solution.
    :param grid: sudoku board to remove numbers from.
    :param size: the sudoku row and column length (9/16...).
    :param number_of_squares: the number of square a row/column of the bord is split to (3/4...).
    :param attempts: number of attempts to remove numbers. default 5.
    :return: sudoku grid.
    """
    global counter
    max_range = size - 1
    while attempts > 0:
        # Select a random cell that is not already empty
        row = randint(0, max_range)
        col = randint(0, max_range)
        while grid[row][col] == 0:
            row = randint(0, max_range)
            col = randint(0, max_range)

        backup = grid[row][col]
        grid[row][col] = 0

        # Count the number of solutions
        counter = 0
        modular_solve_after_remove(grid, size, number_of_squares)
        # solve_grid(grid)
        # If there is more then 1 solution revert back the change to the board
        if counter != 1:
            grid[row][col] = backup
            attempts -= 1
    return grid


def modular_is_possible(grid, row, col, value, size, number_of_squares):
    """
    | check if a given value is possible in the given sudoku grid.
    :param grid: grid to check.
    :param row: row position.
    :param col: column position.
    :param value: value to check if possible.
    :param size: the sudoku row and column length (9/16...).
    :param number_of_squares: the number of square a row/column of the bord is split to (3/4...).
    :return: True when possible value.
    """
    for i in range(size):
        # check the value is not in the row
        if grid[row][i] == value:
            return False
        # check the value is not in the column
        if grid[i][col] == value:
            return False
    # floor division to find the square out of the given (number_of_squares)
    # multiply by (number_of_squares) to get the starting position for the square in the grid
    square_row = (row // number_of_squares) * number_of_squares
    square_col = (col // number_of_squares) * number_of_squares
    for i in range(number_of_squares):
        for j in range(number_of_squares):
            if grid[square_row + i][square_col + j] == value:
                return False
    return True


def random_num_list(size):
    """
    | create random list of numbers to use.
    :param size: the max number to be in the list.
    :return: random list of numbers from 1 to (size).
    """
    num_list = []
    for num in range(1, size + 1):
        num_list.append(num)
    shuffle(num_list)
    return num_list


def modular_solve(grid, size, number_of_squares, num_list=None, board=None):
    """
    | solve given sudoku board.
    :param grid: grid to try to solve.
    :param size: the sudoku row and column length (9/16...).
    :param number_of_squares: the number of square a row/column of the bord is split to (3/4...).
    :param num_list: possible numbers on the board. default None.
    :param board: Puzzle object from game.py to update the display
    :return: grid when solved, False when there is no solution.
    """
    def update(val):
        board.cubes[row][col].set_val(val)
        board.cubes[row][col].draw_cube()
        board.cubes[row][col].update_cube()

    if num_list is None:
        num_list = random_num_list(size)

    for row in range(size):
        for col in range(size):
            if grid[row][col] == 0:
                for value in num_list:
                    if modular_is_possible(grid, row, col, value, size, number_of_squares):
                        grid[row][col] = value
                        if board is not None:
                            update(value)
                        if modular_solve(grid, size, number_of_squares, num_list, board=board):
                            return grid
                        grid[row][col] = 0
                        if board is not None:
                            update(0)
                return False
    return True


def new_board():
    """
    | create random full sudoku grid.
    :return: sudoku grid.
    """
    grid = create_board(9)
    full_grid = modular_solve(grid, 9, 3)
    return full_grid


def print_board_console(grid):
    """
    | print sudoku grid to the console.
    :param grid: the sudoku grid to print.
    """
    for i in range(9):
        temp_line = str(grid[i])[1:-1]
        temp_line = temp_line.replace(',', '')
        print_line = f"{temp_line[0:6]}|{temp_line[6:12]}|{temp_line[12:18]}"
        print(print_line)
        if i in (2, 5):
            line_break = f'{"-" * 6}|{"-" * 6}|{"-" * 6}'
            print(line_break)


def unsolvable_try(grid=None):
    if grid is None:
        grid = []
        for i in range(9):
            grid.append([1, 0, 0, 0, 0, 0, 0, 0, 0])
    dup = check_no_duplicates(grid, 3)
    if dup is True:
        solve = modular_solve(grid, 9, 3)
        if solve:
            print('solved')
        else:
            print('unsolvable')
    else:
        print('unsolvable-duplicates')


def startup():
    full_grid = new_board()
    print_board_console(full_grid)

    print("Sudoku Grid Ready")

    # remove num from board
    grid_to_solve = remove_numbers(full_grid, 9, 3)
    print_board_console(grid_to_solve)


if __name__ == "__main__":
    unsolvable_try()
    print()
    startup()
    print()
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
    # unsolvable_try(temp)
    temp = modular_solve(temp, 9, 3)
    if temp is False:
        print('unsolvable')
    else:
        print_board_console(temp)
    # temp = [
    #     [2, 0, 0, 0, 0, 6, 0, 0, 0, 15, 0, 0, 0, 13, 0, 14],
    #     [0, 0, 15, 0, 0, 0, 0, 0, 4, 0, 0, 14, 5, 0, 0, 0],
    #     [8, 0, 0, 5, 1, 0, 0, 12, 0, 13, 0, 0, 4, 0, 7, 0],
    #     [0, 12, 6, 4, 3, 9, 7, 0, 0, 8, 0, 5, 15, 11, 0, 0],
    #     [0, 13, 0, 15, 0, 8, 5, 7, 6, 0, 9, 0, 10, 12, 0, 0],
    #     [0, 0, 0, 0, 6, 0, 0, 1, 0, 14, 0, 7, 16, 0, 0, 4],
    #     [5, 0, 7, 14, 0, 12, 9, 0, 0, 11, 0, 8, 3, 0, 0, 0],
    #     [0, 11, 0, 0, 15, 0, 0, 10, 3, 0, 12, 1, 0, 9, 0, 0],
    #     [0, 0, 9, 0, 4, 5, 0, 8, 13, 0, 0, 10, 0, 0, 16, 0],
    #     [0, 0, 0, 8, 13, 0, 1, 0, 0, 12, 16, 0, 14, 10, 0, 15],
    #     [10, 0, 0, 2, 12, 0, 15, 0, 9, 0, 0, 3, 0, 0, 0, 0],
    #     [0, 0, 13, 7, 0, 2, 0, 3, 1, 4, 15, 0, 8, 0, 9, 0],
    #     [0, 0, 4, 9, 7, 0, 6, 0, 0, 10, 5, 11, 12, 3, 1, 0],
    #     [0, 10, 0, 3, 0, 0, 14, 0, 2, 0, 0, 15, 13, 0, 0, 9],
    #     [0, 0, 0, 13, 10, 0, 0, 2, 0, 0, 0, 0, 0, 15, 0, 0],
    #     [7, 0, 11, 0, 0, 0, 4, 0, 0, 0, 6, 0, 0, 0, 0, 10]
    # ]
    # modular_solve(temp, 16, 4)
    # for this in temp:
    #     print(this)
    # temp = create_board(16)
    # modular_solve(temp, 16, 4)
    # for this in temp:
    #     print(this)
    # print("empty:")
    # remove_numbers(temp, 16, 4, 10)
    # for this in temp:
    #     print(this)
