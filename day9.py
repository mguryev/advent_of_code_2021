import argparse
import copy
import itertools
import math
import typing


def parse_args():
    parser = argparse.ArgumentParser()

    parser.add_argument('input')

    return parser.parse_args()


class Field:
    _data: typing.List[typing.List[float]]

    def __init__(self, data: typing.List[typing.List[float]]):
        self._data = data

    def get(self, column: int, row: int, default: float = math.inf) -> float:
        if not 0 <= row <= (len(self._data) - 1):
            return default

        line = self._data[row]

        if not 0 <= column <= (len(line) - 1):
            return default

        return line[column]

    def rows(self) -> int:
        return len(self._data)

    def columns(self) -> int:
        return len(self._data[0])

    def print(self) -> typing.NoReturn:
        for line in self._data:
            print(line)


def _read_data(input_file) -> Field:
    with open(input_file) as _input:
        lines = _input.read().splitlines()

    pillars = []

    for line in lines:
        pillars += [[
            int(p) for p in line
        ]]

    return Field(pillars)


def run(input_file: str) -> None:
    data = _read_data(input_file)

    basins = []

    locs = [
        (x, y)
        for x, y in itertools.product(
            range(data.columns()),
            range(data.rows()),
        )
    ]
    search_frontier = set(
        copy.deepcopy(locs)
    )

    for x, y in locs:
        if (x, y) not in search_frontier:
            continue

        search_frontier.remove((x, y))
        basin_frontier = [(x, y)]
        basin = []

        while len(basin_frontier) > 0:
            x, y = basin_frontier.pop()
            print(f'loc - {x, y}')

            if data.get(x, y) == 9:
                continue

            basin.append((x, y))
            neighbours = [
                (x - 1, y),
                (x + 1, y),
                (x, y - 1),
                (x, y + 1),
            ]
            print(f'neighbours - {neighbours}')
            neighbours = {
                (x, y)
                for x, y in neighbours
                if data.get(x, y) < 9
            }

            neighbours = neighbours.intersection(
                search_frontier
            )
            print(f'searchable neighbours - {neighbours}')

            basin_frontier += list(neighbours)
            print(f'basin frontier - {basin_frontier}')
            search_frontier = search_frontier.difference(neighbours)
            print(f'search frontier - {basin_frontier}')

        if basin:
            basins.append(basin)

    basins = list(sorted(
        basins,
        key=lambda b: len(b),
        reverse=True
    ))

    top_3_basins = basins[0:3]

    result = 1

    for basin in top_3_basins:
        print(basin, len(basin))
        result *= len(basin)

    print(result)


if __name__ == '__main__':
    args = parse_args()

    run(args.input)
