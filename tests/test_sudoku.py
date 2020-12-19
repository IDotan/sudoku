import sudoku


def test_create_board():
    grid = sudoku.create_board(9)
    for i in range(9):
        assert grid[i] == [0, 0, 0, 0, 0, 0, 0, 0, 0]


def test_find_square():
    grid = []
    for i in range(9):
        if 0 <= i <= 2:
            grid.append([1, 1, 1, 2, 2, 2, 3, 3, 3])
        elif 3 <= i <= 5:
            grid.append([4, 4, 4, 5, 5, 5, 6, 6, 6])
        elif 6 <= i <= 8:
            grid.append([7, 7, 7, 8, 8, 8, 9, 9, 9])

    squares = [[0, 0], [0, 3], [0, 6], [3, 0], [3, 3], [3, 6], [6, 0], [6, 3], [6, 6]]
    for i in range(9):
        temp = []
        for j in range(9):
            temp.append(i + 1)
        assert sudoku.find_square(grid, squares[i][0], squares[i][1]) == temp


def test_find_column():
    grid = []
    for i in range(9):
        temp = []
        for j in range(9):
            temp.append(j + 1)
        grid.append(temp)

    for col in range(9):
        test_col = []
        for i in range(9):
            test_col.append(col + 1)
        assert sudoku.find_column(grid, col) == test_col


def test_find_duplicate():
    lst = []
    assert sudoku.find_duplicate(lst) is False

    lst = [1, 1]
    assert sudoku.find_duplicate(lst) is True

    lst = [0, 1]
    assert sudoku.find_duplicate(lst) is False

    lst = [1, 0, 0]
    assert sudoku.find_duplicate(lst) is False

    lst = [1, 2, 3]
    assert sudoku.find_duplicate(lst) is False

    lst = [1, 2, 2]
    assert sudoku.find_duplicate(lst) is True


def test_check_no_duplicates_no_dup():
    grid = [
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
    assert sudoku.check_no_duplicates(grid) is True


def test_check_no_duplicates_dup_row():
    grid = [
        [0, 0, 4, 4, 9, 7, 6, 0, 5],
        [0, 0, 6, 3, 0, 8, 0, 0, 0],
        [0, 7, 0, 0, 0, 0, 0, 1, 0],
        [0, 3, 0, 9, 0, 0, 8, 4, 0],
        [6, 0, 0, 0, 3, 0, 0, 0, 0],
        [0, 4, 2, 0, 0, 0, 9, 3, 1],
        [0, 5, 0, 0, 8, 0, 7, 9, 2],
        [0, 8, 0, 7, 5, 3, 1, 6, 0],
        [0, 0, 0, 0, 0, 0, 0, 8, 3]
    ]
    assert sudoku.check_no_duplicates(grid) is False


def test_check_no_duplicates_dup_col():
    grid = [
        [0, 0, 0, 4, 9, 7, 6, 0, 5],
        [0, 0, 6, 3, 0, 8, 0, 0, 0],
        [0, 7, 0, 0, 0, 0, 0, 1, 0],
        [0, 3, 0, 9, 0, 0, 8, 4, 0],
        [6, 0, 0, 0, 3, 0, 0, 0, 0],
        [0, 4, 2, 0, 0, 0, 9, 3, 1],
        [0, 5, 0, 0, 8, 0, 7, 9, 2],
        [0, 8, 0, 7, 5, 3, 1, 6, 0],
        [0, 7, 0, 0, 0, 0, 0, 8, 3]
    ]
    assert sudoku.check_no_duplicates(grid) is False


def test_check_no_duplicates_dup_square():
    grid = [
        [0, 0, 0, 4, 9, 7, 6, 0, 5],
        [0, 6, 6, 3, 0, 8, 0, 0, 0],
        [0, 7, 0, 0, 0, 0, 0, 1, 0],
        [0, 3, 0, 9, 0, 0, 8, 4, 0],
        [6, 0, 0, 0, 3, 0, 0, 0, 0],
        [0, 4, 2, 0, 0, 0, 9, 3, 1],
        [0, 5, 0, 0, 8, 0, 7, 9, 2],
        [0, 8, 0, 7, 5, 3, 1, 6, 0],
        [0, 0, 0, 0, 0, 0, 0, 8, 3]
    ]
    assert sudoku.check_no_duplicates(grid) is False


def test_fill_grid():
    grid = [
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
    solution = [
        [3, 1, 8, 4, 9, 7, 6, 2, 5],
        [5, 2, 6, 3, 1, 8, 4, 7, 9],
        [9, 7, 4, 5, 6, 2, 3, 1, 8],
        [7, 3, 5, 9, 2, 1, 8, 4, 6],
        [6, 9, 1, 8, 3, 4, 2, 5, 7],
        [8, 4, 2, 6, 7, 5, 9, 3, 1],
        [4, 5, 3, 1, 8, 6, 7, 9, 2],
        [2, 8, 9, 7, 5, 3, 1, 6, 4],
        [1, 6, 7, 2, 4, 9, 5, 8, 3]
    ]
    assert sudoku.modular_solve(grid, 9, 3) == solution


def test_fill_grid_no_solution():
    grid = [
        [0, 0, 0, 4, 9, 7, 6, 0, 5],
        [4, 0, 6, 3, 0, 8, 0, 0, 0],
        [0, 7, 0, 0, 0, 0, 0, 1, 0],
        [0, 3, 0, 9, 0, 0, 8, 4, 0],
        [6, 0, 0, 0, 3, 0, 0, 0, 0],
        [0, 4, 2, 0, 0, 0, 9, 3, 1],
        [0, 5, 0, 0, 8, 0, 7, 9, 2],
        [0, 8, 0, 7, 5, 3, 1, 6, 0],
        [0, 0, 0, 0, 0, 0, 0, 8, 3]
    ]
    assert sudoku.modular_solve(grid, 9, 3) is False


def test_fill_grid_duplicates():
    grid = [
        [0, 0, 0, 4, 9, 7, 6, 0, 5],
        [0, 0, 6, 3, 0, 8, 0, 0, 0],
        [6, 7, 0, 0, 0, 0, 0, 1, 0],
        [0, 3, 0, 9, 0, 0, 8, 4, 0],
        [6, 0, 0, 0, 3, 0, 0, 0, 0],
        [0, 4, 2, 0, 0, 0, 9, 3, 1],
        [0, 5, 0, 0, 8, 0, 7, 9, 2],
        [0, 8, 0, 7, 5, 3, 1, 6, 0],
        [0, 0, 0, 0, 0, 0, 0, 8, 3]
    ]
    assert sudoku.modular_solve(grid, 9, 3) is False


def test_remove_numbers():
    grid = [
        [3, 1, 8, 4, 9, 7, 6, 2, 5],
        [5, 2, 6, 3, 1, 8, 4, 7, 9],
        [9, 7, 4, 5, 6, 2, 3, 1, 8],
        [7, 3, 5, 9, 2, 1, 8, 4, 6],
        [6, 9, 1, 8, 3, 4, 2, 5, 7],
        [8, 4, 2, 6, 7, 5, 9, 3, 1],
        [4, 5, 3, 1, 8, 6, 7, 9, 2],
        [2, 8, 9, 7, 5, 3, 1, 6, 4],
        [1, 6, 7, 2, 4, 9, 5, 8, 3]
    ]
    check = [
        [3, 1, 8, 4, 9, 7, 6, 2, 5],
        [5, 2, 6, 3, 1, 8, 4, 7, 9],
        [9, 7, 4, 5, 6, 2, 3, 1, 8],
        [7, 3, 5, 9, 2, 1, 8, 4, 6],
        [6, 9, 1, 8, 3, 4, 2, 5, 7],
        [8, 4, 2, 6, 7, 5, 9, 3, 1],
        [4, 5, 3, 1, 8, 6, 7, 9, 2],
        [2, 8, 9, 7, 5, 3, 1, 6, 4],
        [1, 6, 7, 2, 4, 9, 5, 8, 3]
    ]
    check = sudoku.remove_numbers(check)
    assert check != grid
