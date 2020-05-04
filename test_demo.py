from hypothesis import settings, note
from hypothesis.stateful import RuleBasedStateMachine, rule, invariant, precondition
from hypothesis.strategies import integers

N = 4  # this is the "N" in the N-queens problem


class Queen(object):
    def __init__(self, i):
        self.i = i
        self.coordinates = tuple()

    def __repr__(self):
        return f"Queen {self.i} on (column={self.coordinates[0]}, row={self.coordinates[1]})"


def all_queens_placed_on_board(self):
    all_on_board = all(map(lambda x: len(x.coordinates), self.queens))  # are they placed on board yet?
    if not all_on_board:
        return False
    on_distinct_positions = len(set(map(lambda x: x.coordinates, self.queens))) == N
    if not on_distinct_positions:
        return False
    return True


def descending_diagonal_index(param: Queen):
    """2 queens are on same descending diagonal if both of their `i` are equal, where `i = (row + column)`"""
    index = param.coordinates[0] + param.coordinates[1]
    return index


def ascending_diagonal_index(param: Queen):
    """2 queens are on same ascending diagonal if both of their `i` are equal, where `i = (row - column)`"""
    index = param.coordinates[0] - param.coordinates[1]
    return index


def ints():
    """ generates only integers that are valid for this problem """
    return integers(min_value=0, max_value=N - 1)


class NQueensProblem(RuleBasedStateMachine):
    def __init__(self):
        super().__init__()
        self.queens = [Queen(i) for i in range(N)]

    @rule(queen_index=ints(), column=ints(), row=ints())
    def set_new_queen_position(self, queen_index, column, row):
        # print(f"moving queen {queen_index} to {row, column}")
        queen = self.queens[queen_index]
        queen.coordinates = (column, row)

    @invariant()
    @precondition(all_queens_placed_on_board)
    def unsolved_yet(self):
        queens_on_distinct_columns = len(set(map(lambda x: x.coordinates[0], self.queens))) == N
        if not queens_on_distinct_columns:
            return

        queens_on_distinct_rows = len(set(map(lambda x: x.coordinates[1], self.queens))) == N
        if not queens_on_distinct_rows:
            return

        queens_on_distinct_ascending_diagonals = len(set(map(ascending_diagonal_index, self.queens))) == N
        if not queens_on_distinct_ascending_diagonals:
            return

        queens_on_distinct_descending_diagonals = len(set(map(descending_diagonal_index, self.queens))) == N
        if not queens_on_distinct_descending_diagonals:
            return
        note(f'Queens\' final positions: {self.queens}')
        assert False


NQueensProblem.TestCase.settings = settings(max_examples=10_000, deadline=None)

test_n_queens = NQueensProblem.TestCase
