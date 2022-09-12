import argparse
import itertools
import re


def parse_args():
    parser = argparse.ArgumentParser()

    parser.add_argument('input')

    return parser.parse_args()


def _parse_goal_coordinates(coords):
    return sorted(int(d) for d in coords.split('..'))


def _read_data(input_file):
    with open(input_file) as _input:
        lines = _input.read().splitlines()

    instruction = lines[0]
    pattern = re.compile(r'target area: x=(.*), y=(.*)')
    x, y = pattern.match(instruction).groups()

    x = _parse_goal_coordinates(x)
    y = _parse_goal_coordinates(y)

    return x, y


def calculate_firing_solution(goal_x, goal_y):
    # best_height = -math.inf
    solutions = []

    search_range_x = range(max(goal_x) + 1)
    search_range_y = range(min(goal_y), -1 * (min(goal_y) - 1))

    for shot_x, shot_y in itertools.product(search_range_x, search_range_y):
        x, y = 0, 0
        reached_height = 0
        solution = (shot_x, shot_y)

        while min(goal_y) <= y and x <= max(goal_x):
            x += shot_x
            y += shot_y

            if reached_height < y:
                reached_height = y

            if (
                goal_x[0] <= x <= goal_x[1]
                and
                goal_y[0] <= y <= goal_y[1]
            ):
                solutions.append(solution)
                break

            shot_x = max([shot_x - 1, 0])
            shot_y -= 1

    return solutions


def run(input_file: str) -> None:
    goal_x, goal_y = _read_data(input_file)

    solutions = calculate_firing_solution(goal_x, goal_y)

    best_solution = sorted(solutions, key=lambda solution: solution[1])[0]
    shot_x, shot_y = best_solution
    best_height = int((shot_y + 1) * (shot_y / 2))

    print('height:', best_height)
    print('N solution:', len(solutions))


if __name__ == '__main__':
    args = parse_args()

    run(args.input)
