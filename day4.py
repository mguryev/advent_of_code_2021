import argparse
import dataclasses
import itertools

import typing


def parse_args():
    parser = argparse.ArgumentParser()

    parser.add_argument('input')

    return parser.parse_args()


@dataclasses.dataclass
class BingoCell:
    number: int
    marked: bool


def _read_data(input_file):
    with open(input_file) as _input:
        lines = _input.read().splitlines()

    game_numbers = lines.pop(0)
    game_numbers = (int(number) for number in game_numbers.split(','))

    boards = []

    while len(lines) > 0:
        board_lines = []

        for line in lines[1:6]:
            numbers = [int(number) for number in line.split(' ') if number != '']
            board_line = [BingoCell(number, False) for number in numbers]
            board_lines.append(board_line)

        new_board = BingoBoard(board_lines)
        boards.append(new_board)

        lines = lines[6:]

    return game_numbers, boards


class BingoBoard:
    def __init__(self, board: typing.List[typing.List[BingoCell]]):
        self.board = board

    def print(self):
        for row in self.board:
            print([cell.number for cell in row])

    def mark_a_number(self, number: int):
        cells = (cell for row in self.board for cell in row)

        for cell in cells:
            if cell.number == number:
                cell.marked = True
                return

    @staticmethod
    def _board_is_won(cells: typing.List[BingoCell]) -> bool:
        return all(cell.marked for cell in cells)

    def is_won(self) -> bool:
        board_size = len(self.board)
        rows = range(board_size)
        columns = range(board_size)

        row_cells = (
            [self.board[row][column] for column in columns]
            for row in rows
        )

        column_cells = (
            [self.board[row][column] for row in rows]
            for column in columns
        )

        return any(
            self._board_is_won(cells)
            for cells in itertools.chain(row_cells, column_cells)
        )

    def get_marked_numbers(self) -> typing.List[int]:
        cells = (cell for row in self.board for cell in row)
        return [cell.number for cell in cells if cell.marked]

    def get_unmarked_numbers(self) -> typing.List[int]:
        cells = (cell for row in self.board for cell in row)
        return [cell.number for cell in cells if not cell.marked]


def play_bingo(input_file):
    numbers, boards = _read_data(input_file)

    winning_boards = []
    last_number = 0

    for number in numbers:
        last_number = number
        for board in boards:
            board.mark_a_number(number)

            if not board.is_won():
                continue

            winning_boards.append(board)

        if winning_boards:
            break

    winning_board = winning_boards[0]
    winning_board.print()

    return (
        sum(winning_board.get_unmarked_numbers())
        *
        last_number
    )


def play_bingo_to_lose(input_file):
    numbers, boards = _read_data(input_file)

    last_board = None
    last_number = 0

    for number in numbers:
        last_number = number
        boards_to_play = []

        for board in boards:
            board.mark_a_number(number)

            if not board.is_won():
                boards_to_play.append(board)
                continue

            last_board = board

        if not boards_to_play:
            break

        boards = boards_to_play

    losing_board = last_board
    losing_board.print()

    return (
        sum(losing_board.get_unmarked_numbers())
        *
        last_number
    )


if __name__ == '__main__':
    args = parse_args()

    print('looking for winning board')
    bingo_score = play_bingo(args.input)
    print(bingo_score)

    print('looking for losing board')
    bingo_score = play_bingo_to_lose(args.input)
    print(bingo_score)
