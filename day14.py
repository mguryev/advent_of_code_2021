import argparse
import collections
import datetime
import re
import typing


def parse_args():
    parser = argparse.ArgumentParser()

    parser.add_argument('input')

    return parser.parse_args()


def _read_data(input_file):
    """
    Return incidence map
    """

    with open(input_file) as _input:
        input_lines = _input.read().splitlines()

    polymer = input_lines[0]

    rules = {}

    for line in input_lines[2:]:
        pattern = re.compile(r'(.*) -> (.*)')
        chain, product = pattern.match(line).groups()

        rules[chain] = product

    return polymer, rules


def extend_polymer(polymer: typing.Dict[str, int], rules: typing.Dict[str, str]) -> typing.Dict[str, int]:
    processed_polymer = collections.defaultdict(int)

    for pair, pair_count in polymer.items():
        if pair not in rules:
            processed_polymer[pair] += pair_count

        else:
            addition = rules[pair]
            pair_a = pair[0] + addition
            pair_b = addition + pair[1]

            processed_polymer[pair_a] += pair_count
            processed_polymer[pair_b] += pair_count

    return processed_polymer


def run(input_file: str) -> None:
    _polymer, rules = _read_data(input_file)

    polymer = collections.defaultdict(int)

    for pair in zip(_polymer[:-1], _polymer[1:]):
        pair = ''.join(pair)
        polymer[pair] += 1

    for iteration in range(40):
        print('running polymer extension iteration:', iteration)
        iteration_start = datetime.datetime.now()
        polymer = extend_polymer(polymer, rules)
        print(polymer)
        print('elapsed time:', datetime.datetime.now() - iteration_start)

    elements_count = collections.defaultdict(int)
    elements_count[_polymer[-1]] += 1

    for pair, pair_count in polymer.items():
        elements_count[pair[0]] += pair_count

    print(elements_count)

    elements_count = sorted(elements_count.values())

    print(elements_count[-1] - elements_count[0])


if __name__ == '__main__':
    args = parse_args()

    run(args.input)
