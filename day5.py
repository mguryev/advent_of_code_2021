import argparse
import collections
import dataclasses
import re
import typing


@dataclasses.dataclass
class Vent:
    x: int
    y: int


VentLine = typing.List[Vent]


def parse_args():
    parser = argparse.ArgumentParser()

    parser.add_argument('input')

    return parser.parse_args()


def abs_range(start, end):
    if start > end:
        return range(start, end-1, -1)
    else:
        return range(start, end + 1)


def _read_data(input_file) -> typing.Iterator[VentLine]:
    def parse_vent(point_raw: str) -> Vent:
        coords = re.fullmatch(
            r'(\d+),(\d+)',
            point_raw,
        )

        if coords is None:
            raise ValueError

        x, y = coords.groups()
        return Vent(int(x), int(y))

    def parse_vent_line(start: Vent, end: Vent) -> VentLine:
        # Vertical line
        if start.x == end.x:
            return [
                Vent(start.x, y)
                for y in abs_range(start.y, end.y)
            ]

        # Horizontal line
        if start.y == end.y:
            return [
                Vent(x, start.y)
                for x in abs_range(start.x, end.x)
            ]

        # Diagonal line
        if abs(start.x - end.x) == abs(start.y - end.y):
            return [
                Vent(x, y)
                for x, y in zip(
                    abs_range(start.x, end.x),
                    abs_range(start.y, end.y),
                )
            ]

        # Some other line
        return []

    with open(input_file) as _input:
        lines = _input.read().splitlines()

    for line in lines:
        line_from, line_to = line.split(' -> ')

        yield parse_vent_line(
            parse_vent(line_from),
            parse_vent(line_to),
        )


def find_thermal_vents(input_file: str) -> None:
    vent_lines = _read_data(input_file)

    vent_locations = collections.defaultdict(lambda: 0)

    for vent_line in vent_lines:
        for vent in vent_line:
            vent_locations[f'{vent.x}, {vent.y}'] += 1

    vent_line_overlaps = [
        coords
        for coords, vents_count in vent_locations.items()
        if vents_count > 1
    ]

    print(len(vent_line_overlaps))


if __name__ == '__main__':
    args = parse_args()

    find_thermal_vents(args.input)
