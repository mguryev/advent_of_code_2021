import argparse


def parse_args():
    parser = argparse.ArgumentParser()

    parser.add_argument('input')

    return parser.parse_args()


def compare_numbers(input_file):
    with open(input_file) as input:
        data = [int(d) for d in input.readlines()]

    increases = (
        previous < current
        for previous, current
        in zip(data[:-1], data[1:])
    )

    return sum(increases)


def compare_triplets(input_file):
    with open(input_file) as input:
        data = [int(d) for d in input.readlines()]

    window_width = 3

    data_windowed = [
        sum(data[i: i+window_width])
        for i in range(len(data) + 1 - window_width)
    ]

    increases = (
        previous < current
        for previous, current
        in zip(data_windowed[:-1], data_windowed[1:])
    )

    return sum(increases)


if __name__ == '__main__':
    args = parse_args()
    result = compare_numbers(args.input)
    print('Number of record increases', result)

    result = compare_triplets(args.input)
    print('Number of triplet increases', result)
