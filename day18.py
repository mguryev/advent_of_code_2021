import argparse
import copy
import math
import itertools
import typing

from dataclasses import dataclass


def parse_args():
    parser = argparse.ArgumentParser()

    parser.add_argument('input')

    return parser.parse_args()


def _parse_number(number_str) -> typing.Tuple['Number', str]:
    if number_str[0] == '[':
        value, rest = _read_number(number_str)
    else:
        value = NumberValue(
            value=int(number_str[0])
        )
        rest = number_str[1:]

    return value, rest


def _read_number(number_str) -> typing.Tuple['Number', str]:
    if number_str[0] != '[':
        raise ValueError

    number_str = number_str[1:]

    left_child, number_str = _parse_number(number_str)
    number_str = number_str[number_str.index(',') + 1:]

    right_child, number_str = _parse_number(number_str)
    number_str = number_str[number_str.index(']') + 1:]

    return (
        Number(left_child, right_child),
        number_str
    )


def _read_data(input_file):
    with open(input_file) as _input:
        lines = _input.read().splitlines()

    numbers = []

    for line in lines:
        number, _ = _read_number(line)
        numbers.append(number)

    return numbers


@dataclass
class NumberValue:
    value: int


@dataclass
class Number:
    left: typing.Union['Number', 'NumberValue']
    right: typing.Union['Number', 'NumberValue']


@dataclass
class NumberNode:
    number: typing.Union['Number', 'NumberValue']
    parent: 'NumberNode'
    depth: int


class Arithmetics:
    @staticmethod
    def add(a: Number, b: Number):
        return Number(left=a, right=b)

    @classmethod
    def print(cls, root: typing.Union[Number, NumberValue]):
        if type(root) is NumberValue:
            print(root.value, end='')
            return

        print('[', end='')
        cls.print(root.left)
        print(',', end='')
        cls.print(root.right)
        print(']', end='')

    @classmethod
    def walk_left(
            cls,
            a: Number,
            parent: typing.Optional[NumberNode] = None,
            depth: int = 0,
    ) -> typing.List[NumberNode]:
        if type(a) == NumberValue:
            return [NumberNode(a, parent, depth)]

        else:
            current_node = NumberNode(
                a,
                parent,
                depth
            )
            return (
                cls.walk_left(a.left, current_node, depth + 1)
                +
                [current_node]
                +
                cls.walk_left(a.right, current_node, depth + 1)
            )

    @staticmethod
    def _find_regular_number(nodes: typing.List[NumberNode]) -> typing.Optional[NumberNode]:
        for node in nodes:
            if type(node.number) is not NumberValue:
                continue

            return node
        else:
            return None

    @classmethod
    def explode(cls, root: Number):
        nodes = list(cls.walk_left(root))

        for idx, node in enumerate(nodes):
            if node.depth < 4 or type(node.number) is not Number:
                continue

            if (
                type(node.number.left) is not NumberValue
                or
                type(node.number.right) is not NumberValue
            ):
                continue

            node_to_explode = node
            node_idx = idx
            break
        else:
            raise ValueError('No more nodes to explode')

        number_to_left = cls._find_regular_number(
            list(reversed(nodes[:node_idx - 1]))
        )

        if number_to_left:
            number_to_left.number.value += node_to_explode.number.left.value

        number_to_right = cls._find_regular_number(
            nodes[node_idx + 2:]
        )

        if number_to_right:
            number_to_right.number.value += node_to_explode.number.right.value

        if node_to_explode.parent.number.left is node_to_explode.number:
            node_to_explode.parent.number.left = NumberValue(
                value=0
            )
        if node_to_explode.parent.number.right is node_to_explode.number:
            node_to_explode.parent.number.right = NumberValue(
                value=0
            )

    @classmethod
    def split(cls, root: Number):
        nodes = list(cls.walk_left(root))

        for node in nodes:
            if type(node.number) is not NumberValue:
                continue

            if node.number.value < 10:
                continue

            node_to_split = node
            break

        else:
            raise ValueError

        parent = node_to_split.parent.number
        node_to_split = node_to_split.number

        replacement = Number(
            left=NumberValue(
                math.floor(node.number.value / 2)
            ),
            right=NumberValue(
                math.ceil(node.number.value / 2)
            ),
        )

        if parent.left is node_to_split:
            parent.left = replacement

        if parent.right is node_to_split:
            parent.right = replacement


def sum_numbers(a: Number, b: Number) -> Number:
    result = Arithmetics.add(a, b)
    reduceable = True

    while reduceable:
        try:
            Arithmetics.explode(result)
            continue

        except ValueError:
            pass

        try:
            Arithmetics.split(result)
            continue

        except ValueError:
            pass

        reduceable = False

    return result


def calculate_magnitude(node: typing.Union[Number, NumberValue]) -> int:
    if type(node) is NumberValue:
        return node.value

    return (
        3 * calculate_magnitude(node.left)
        +
        2 * calculate_magnitude(node.right)
    )


def run(input_file: str) -> None:
    numbers = _read_data(input_file)
    result = numbers.pop(0)

    while numbers:
        next_number = numbers.pop(0)

        result = sum_numbers(result, next_number)

    Arithmetics.print(result)
    print('')

    print('total magnitude:', calculate_magnitude(result))

    numbers = _read_data(input_file)
    best_magnitude = 0
    best_solution = None

    for a, b in itertools.permutations(numbers, 2):
        a = copy.deepcopy(a)
        b = copy.deepcopy(b)
        _sum = sum_numbers(a, b)
        magnitude = calculate_magnitude(_sum)

        print(magnitude)

        if magnitude <= best_magnitude:
            continue

        best_magnitude = magnitude
        best_solution = (a, b)

    print('best magnitude:', best_magnitude)
    print('best solution:')
    Arithmetics.print(best_solution[0])
    print('')
    Arithmetics.print(best_solution[1])
    print('')


if __name__ == '__main__':
    args = parse_args()

    run(args.input)
