import sudoku


def test_create_board():
    grid = sudoku.create_board()
    for i in range(9):
        assert grid[i] == [0, 0, 0, 0, 0, 0, 0, 0, 0]


def test_check_grid_full():
    grid = sudoku.create_board()
    assert sudoku.check_grid(grid) is False

    grid = []
    for i in range(9):
        grid.append([1, 1, 1, 1, 1, 1, 1, 1, 1])
    assert sudoku.check_grid(grid) is True

    grid = []
    for i in range(9):
        grid.append([1, 1, 1, 1, 1, 0, 1, 1, 1])
    assert sudoku.check_grid(grid) is False


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
            temp.append(i+1)
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
