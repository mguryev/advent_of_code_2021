import argparse
import copy
import itertools
import json
import typing


def parse_args():
    parser = argparse.ArgumentParser()

    parser.add_argument('input')

    return parser.parse_args()


class Field:
    _data: typing.List[typing.List[int]]

    _SIZE = 10

    def __init__(self, data: typing.List[typing.List[int]]):
        self._data = data

    @staticmethod
    def __increase_energy_levels(data):
        return [
            [
                level + 1
                for level in row
            ]
            for row in data
        ]

    @staticmethod
    def __flash(data, x, y):
        # flash self
        data[y][x] = 0

        neighbours = itertools.product(
            [-1, 0, 1],
            repeat=2
        )
        neighbours = [
            (x + x_delta, y + y_delta)
            for x_delta, y_delta in neighbours
        ]

        next_flashes = []

        for x, y in neighbours:
            # neighbours outside the field
            if not (-1 < x < 10) or not (-1 < y < 10):
                continue

            neighbour_level = data[y][x]

            # has already flashed
            if neighbour_level == 0:
                continue

            # increase neighbour level
            data[y][x] = min(10, neighbour_level + 1)

            if data[y][x] > 9:
                next_flashes.append((x, y))

        return data, next_flashes

    def run_step(self):
        self._data = self.__increase_energy_levels(self._data)

        check_for_flashes = [
            (x, y)
            for x, y in itertools.product(
                range(self._SIZE), repeat=2
            )
        ]

        flashes = 0

        while len(check_for_flashes) > 0:
            x, y = check_for_flashes.pop(0)

            if self._data[y][x] <= 9:
                continue

            flashes += 1

            self._data, new_flashes = self.__flash(
                self._data, x, y
            )

            check_for_flashes += new_flashes

        return flashes

    def print(self):
        for row in self._data:
            print(row)
        print('---')


def _read_data(input_file) -> Field:
    with open(input_file) as _input:
        lines = _input.read().splitlines()

    octopi = []

    for line in lines:

        octopi.append([
            int(p) for p in line
        ])

    return Field(octopi)


def run(input_file: str) -> None:
    field = _read_data(input_file)

    field.print()

    result = []

    for step in range(1000):
        print(f'running step {step}')
        flashes = field.run_step()
        field.print()

        print(f'flashes - {flashes}')
        result.append(flashes)
        if flashes == 100:
            print(f'first step to sync-up! - {step}')
            break

    print(f'result - {result}')
    print(f'total flashes - {sum(result)}')


if __name__ == '__main__':
    args = parse_args()

    run(args.input)
