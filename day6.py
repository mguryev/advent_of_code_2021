import argparse
import copy
import typing


FISH_SPAWN_RATE = 6
FIRST_GENERATION_SPAWN_RATE = 8


def parse_args():
    parser = argparse.ArgumentParser()

    parser.add_argument('input')

    return parser.parse_args()


def _read_data(input_file) -> typing.List[int]:
    with open(input_file) as _input:
        lines = _input.read().splitlines()

    fish_ages = [0] * (FIRST_GENERATION_SPAWN_RATE + 1)

    for line in lines:
        for fish_age in line.split(','):
            fish_age = int(fish_age)
            fish_ages[fish_age] += 1

    return fish_ages


def emulate_generation(fish_ages: typing.List[int]) -> typing.List[int]:
    next_generation_ages = copy.deepcopy(fish_ages)

    # progress the generation age
    next_generation_ages += [0]
    spawning_generation = next_generation_ages.pop(0)

    next_generation_ages[FIRST_GENERATION_SPAWN_RATE] += spawning_generation
    next_generation_ages[FISH_SPAWN_RATE] += spawning_generation

    return next_generation_ages


def run(input_file: str) -> None:
    fish_ages = _read_data(input_file)

    generations = 18

    for generation in range(generations):
        print(f'generation - {generation}, fish population - {fish_ages}')
        fish_ages = emulate_generation(fish_ages)

    print(f'final fish count - {sum(fish_ages)}')


if __name__ == '__main__':
    args = parse_args()

    run(args.input)
