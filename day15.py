import argparse
import collections
import itertools
import heapq
import re
import typing


def parse_args():
    parser = argparse.ArgumentParser()

    parser.add_argument('input')

    return parser.parse_args()


def _read_data(input_file):
    with open(input_file) as _input:
        lines = _input.read().splitlines()

    cavern = []

    for line in lines:
        cavern += [[
            int(p) for p in line
        ]]

    return cavern


Position = typing.Tuple[int, int]
Map = typing.List[typing.List[int]]


class Fringe:
    __DELETED = (-1, -1)  # type: Position

    def __init__(self):
        self.__fringe = []
        self.__fringe_nodes = {}

    def add(self, pos: Position, cost: int):
        if Position in self.__fringe_nodes:
            self.delete(pos)

        record = [cost, pos]
        heapq.heappush(self.__fringe, record)
        self.__fringe_nodes[pos] = record

    def delete(self, pos: Position):
        record = self.__fringe_nodes.pop(pos)
        record[1] = self.__DELETED

    def pop(self):
        while self.__fringe:
            cost, pos = heapq.heappop(self.__fringe)

            if pos == self.__DELETED:
                continue

            self.__fringe_nodes.pop(pos, None)
            return pos, cost

    def contains(self, pos: Position):
        return pos in self.__fringe_nodes


def neighbours(current_pos: Position, cavern_size: int) -> typing.List[Position]:
    x, y = current_pos
    candidates = [
        (x, y - 1),
        (x, y + 1),
        (x - 1, y),
        (x + 1, y),
    ]

    return [
        (x, y)
        for x, y in candidates
        if (
            -1 < x < cavern_size
            and
            -1 < y < cavern_size
        )
    ]


def cost_to_end(current: Position, end: Position) -> int:
    distance = (
        abs(current[0] - end[0])
        + abs(current[1] - end[1])
    )

    return distance


def reconstruct_path(came_from: typing.Dict[Position, Position], end: Position):
    current_position = end
    path = []

    while current_position is not None:
        path.append(current_position)
        current_position = came_from.get(current_position)

    return list(reversed(path))


def find_path(cavern: Map, start: Position, end: Position) -> typing.List[Position]:
    map_size = len(cavern)

    came_from = {}
    g_score = collections.defaultdict(lambda: map_size ** 2 * 10)
    g_score[start] = 0

    fringe = Fringe()
    fringe.add(start, 0)

    while fringe:
        current_pos, cost = fringe.pop()

        if current_pos == end:
            # TODO: reconstruct path
            break

        for neighbour in neighbours(current_pos, map_size):
            x, y = neighbour
            cost = g_score[current_pos] + cavern[y][x]

            if cost >= g_score[neighbour]:
                continue

            came_from[neighbour] = current_pos
            g_score[neighbour] = cost
            fringe.add(neighbour, cost + cost_to_end(neighbour, end))

    else:
        raise RuntimeError('no path found')

    return reconstruct_path(came_from, end)


def run(input_file: str) -> None:
    cavern = _read_data(input_file)
    cavern_size = len(cavern)

    bigger_cavern = []

    for y in range(cavern_size * 5):
        row = []
        for x in range(cavern_size * 5):
            danger_offset = (x // cavern_size) + (y // cavern_size)

            raw_danger_level = cavern[y % cavern_size][x % cavern_size] + danger_offset
            row.append(raw_danger_level % 9 or 9)

        bigger_cavern.append(row)

    cavern_size = len(bigger_cavern)
    path = find_path(bigger_cavern, (0, 0), (cavern_size - 1, cavern_size - 1))

    path_cost = 0

    for pos in path:
        x, y = pos
        path_cost += bigger_cavern[y][x]
    path_cost -= bigger_cavern[0][0]

    for line in bigger_cavern:
        line = [str(i) for i in line]
        print(''.join(line))

    print(path)
    print(path_cost)


if __name__ == '__main__':
    args = parse_args()

    run(args.input)
