"""
Generates two matrices for a code-name duet game.
The two matrices generated follow these rules:
1. Each player sees its own "green" and "black" tiles, and all other tiles are presented as neutral.
2. Each player's green and black tiles will be seen as neutral by the other player.

This script allows players to use the normal code-name cards even when only two players are participating (basically
turning the regular code-name game into code-name "duet" for free.
"""
import random
import enum


class Tile(enum.Enum):
    NEUTRAL = 0
    BLACK = 1
    GREEN = 2


GREEN_AMOUNT_PER_PLAYER = 4
BLACK_AMOUNT_PER_PLAYER = 1
MAT_SIZE = 25


def randomly_choose_indexes(available_indexes: list[int], amount: int) -> set[int]:
    """
    Chooses <amount> of indexes randomly from the given set of available indexes, removes them from the available list
    and return the chosen elements.
    """
    chosen_indexes = set(random.sample(available_indexes, amount))
    for i in chosen_indexes:
        available_indexes.remove(i)  # object is mutable, let's change it
    return chosen_indexes


def generate_mat(black_indexes: set[int], green_indexes: set[int], mat_size: int) -> list[Tile]:
    """
    Generates a single player's matrix given the black and green indexes.
    """
    mat = []
    for i in range(mat_size):
        if i in black_indexes:
            mat.append(Tile.BLACK)
        elif i in green_indexes:
            mat.append(Tile.GREEN)
        else:
            mat.append(Tile.NEUTRAL)
    return mat


def get_player_matrices(mat_size: int) -> tuple[list[Tile], list[Tile]]:
    """
    Generates two matrices with the given size, one for each player.
    """
    available_indexes = [i for i in range(mat_size)]
    chosen_green_indexes_player_one = randomly_choose_indexes(available_indexes, GREEN_AMOUNT_PER_PLAYER)
    chosen_black_indexes_player_one = randomly_choose_indexes(available_indexes, BLACK_AMOUNT_PER_PLAYER)
    chosen_green_indexes_player_two = randomly_choose_indexes(available_indexes, GREEN_AMOUNT_PER_PLAYER)
    chosen_black_indexes_player_two = randomly_choose_indexes(available_indexes, BLACK_AMOUNT_PER_PLAYER)
    mat_one = generate_mat(chosen_black_indexes_player_one, chosen_green_indexes_player_one, mat_size)
    mat_two = generate_mat(chosen_black_indexes_player_two, chosen_green_indexes_player_two, mat_size)
    return mat_one, mat_two


def test_matrices(matrix_1: list[Tile], matrix_2: list[Tile]):
    """
    Make sure the matrices follow the rules of the game, meant as a test case only.
    """
    assert len(matrix_1) == len(matrix_2)
    for i in range(len(matrix_1)):
        if matrix_1[i] in (Tile.GREEN, Tile.BLACK):
            assert matrix_2[i] == Tile.NEUTRAL
        if matrix_2[i] in (Tile.GREEN, Tile.BLACK):
            assert matrix_1[i] == Tile.NEUTRAL


def write_matrix_to_csv(matrix: list[Tile], output_path: str):
    """
    Writes the matrix into a CSV file.
    """
    sqrt_len = pow(len(matrix), 0.5)
    assert sqrt_len == int(sqrt_len), "matrix size {} is impossible".format(len(matrix))
    row_size = int(sqrt_len)
    with open(output_path, 'w') as f:
        for row in range(row_size):
            for col in range(row_size):
                f.write(matrix[row * row_size + col].name + ",")
            f.write("\r\n")


def main():
    matrix_1, matrix_2 = get_player_matrices(MAT_SIZE)
    write_matrix_to_csv(matrix_1, r'C:\temp\matrix_1.csv')
    write_matrix_to_csv(matrix_2, r'C:\temp\matrix_2.csv')


if __name__ == '__main__':
    main()
