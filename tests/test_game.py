import game

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
game.initialize_globals()


def test_puzzle_reset():
    test = game.Puzzle(grid, 9, 3, solution)
    test.cubes[0][0].set_val(3)
    test.cubes[1][0].set_val(5)
    # assert the change happened
    assert test.cubes[0][0].get_val() == 3
    assert test.cubes[1][0].get_val() == 5
    test.reset_board()
    assert test.cubes[0][0].get_val() == 0
    assert test.cubes[0][0].get_val() == 0
    # make sure base value didn't reset to zero
    assert test.cubes[0][3].get_val() == 4


def test_change_base_value():
    test = game.Puzzle(grid, 9, 3, solution)
    test.cubes[0][3].set_val(7)
    assert test.cubes[0][3].get_val() == 4
