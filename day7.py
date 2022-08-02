import argparse
import functools
import json
import math
import statistics
import typing


def parse_args():
    parser = argparse.ArgumentParser()

    parser.add_argument('input')

    return parser.parse_args()


def _read_data(input_file) -> typing.Dict[int, int]:
    with open(input_file) as _input:
        lines = _input.read().splitlines()

    pos_count = {}

    for line in lines:
        for pos in line.split(','):
            pos = int(pos)
            pos_count[pos] = pos_count.get(pos, 0) + 1

    return pos_count


def calculate_optimal_position(sub_positions: typing.Dict[int, int], cost_fn) -> int:
    leftmost_pos = min(sub_positions.keys())
    rightmost_pos = max(sub_positions.keys())

    optimal_fuel_cost = math.inf
    optimal_pos = -1 * math.inf

    for pos in range(leftmost_pos, rightmost_pos):
        fuel_cost = cost_fn(sub_positions, pos)
        # Next position is strictly larger
        if optimal_fuel_cost < fuel_cost:
            break

        optimal_fuel_cost = fuel_cost
        optimal_pos = pos

    return optimal_pos


def calculate_fuel_cost_linear(sub_positions: typing.Dict[int, int], optimal_position: int) -> int:
    fuel_cost = 0

    for sub_pos, sub_count in sub_positions.items():
        fuel_cost += abs(optimal_position - sub_pos) * sub_count

    return fuel_cost


def calculate_fuel_cost_arithmetic(sub_positions: typing.Dict[int, int], optimal_position: int) -> int:
    fuel_cost = 0

    for sub_pos, sub_count in sub_positions.items():
        pos_distance = abs(optimal_position - sub_pos)
        pos_cost = (pos_distance + 1) / 2 * pos_distance
        fuel_cost += pos_cost * sub_count

    return fuel_cost


def run(input_file: str) -> None:
    sub_positions = _read_data(input_file)

    pos_mean = calculate_optimal_position(sub_positions, calculate_fuel_cost_linear)
    print(f"optimal position - {pos_mean}")

    fuel_expense = calculate_fuel_cost_linear(sub_positions, pos_mean)
    print(f"total fuel expense - {fuel_expense}")

    pos_mean = calculate_optimal_position(sub_positions, calculate_fuel_cost_arithmetic)
    print(f"optimal position - {pos_mean}")

    fuel_expense = calculate_fuel_cost_arithmetic(sub_positions, pos_mean)
    print(f"total fuel expense - {fuel_expense}")


if __name__ == '__main__':
    args = parse_args()

    run(args.input)
