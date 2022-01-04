import argparse
import dataclasses
import typing


def parse_args():
    parser = argparse.ArgumentParser()

    parser.add_argument('input')

    return parser.parse_args()


@dataclasses.dataclass
class Position:
    depth: int
    distance: int


@dataclasses.dataclass
class Movement:
    direction: str
    distance: int


class Sub:
    def move(self, movement: Movement):
        raise NotImplemented

    def current_position(self):
        raise NotImplemented


class SubNoAim(Sub):
    def __init__(self, current_position: Position):
        self._position = current_position

    def move(self, movement: Movement):
        if movement.direction == 'up':
            self._position.depth -= movement.distance
        elif movement.direction == 'down':
            self._position.depth += movement.distance
        elif movement.direction == 'forward':
            self._position.distance += movement.distance

    def current_position(self) -> Position:
        return self._position


class SubWithAim(Sub):
    def __init__(self, current_position: Position, current_aim: int):
        self._position = current_position
        self._aim = current_aim

    def move(self, movement: Movement):
        if movement.direction == 'up':
            self._aim -= movement.distance
        elif movement.direction == 'down':
            self._aim += movement.distance
        elif movement.direction == 'forward':
            self._position.distance += movement.distance
            self._position.depth += self._aim * movement.distance

    def current_position(self) -> Position:
        return self._position


def read_input(input_file: str) -> typing.List[Movement]:
    def read_movement(raw_datum: str) -> Movement:
        direction, distance = raw_datum.split(' ')

        return Movement(
            direction=direction,
            distance=int(distance)
        )

    with open(input_file) as input_data:
        data = input_data.readlines()

    return [read_movement(d) for d in data]


def move_sub(sub: Sub, instructions: typing.List[Movement]) -> Position:
    for instruction in instructions:
        sub.move(instruction)

    return sub.current_position()


def run(input_file):
    instructions = read_input(input_file)

    sub_no_aim = SubNoAim(
        current_position=Position(depth=0, distance=0)
    )

    final_position = move_sub(sub_no_aim, instructions)
    print('No aim position:', final_position.distance * final_position.depth)

    sub_with_aim = SubWithAim(
        current_position=Position(depth=0, distance=0),
        current_aim=0,
    )
    final_position = move_sub(sub_with_aim, instructions)
    print('With aim position:', final_position.distance * final_position.depth)


if __name__ == '__main__':
    args = parse_args()
    run(args.input)
