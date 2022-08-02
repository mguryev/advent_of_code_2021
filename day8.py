import argparse
import dataclasses
import functools
import typing


@dataclasses.dataclass
class InputLine:
    digits: typing.List[str]
    display: typing.List[str]


def parse_args():
    parser = argparse.ArgumentParser()

    parser.add_argument('input')

    return parser.parse_args()


def _read_data(input_file) -> typing.Iterator[InputLine]:
    with open(input_file) as _input:
        lines = _input.read().splitlines()

    for line in lines:
        digits, display = line.split(' | ')

        digits = [
            ''.join(sorted(d))
            for d in digits.split(' ')
        ]

        display = [
            ''.join(sorted(d))
            for d in display.split(' ')
        ]

        yield InputLine(
            digits,
            display,
        )


def build_digit_map(digits: typing.List[str]) -> typing.Dict[str, int]:
    digit_map = {}

    for d in digits * 2:
        if len(d) == 2:
            digit_map[1] = d

        elif len(d) == 4:
            digit_map[4] = d

        elif len(d) == 3:
            digit_map[7] = d

        elif len(d) == 7:
            digit_map[8] = d

        elif len(d) == 5:
            if len(
                set(digit_map.get(4, ''))
                .intersection(set(d))
            ) == 2:
                digit_map[2] = d
            elif len(
                set(digit_map.get(1, ''))
                .intersection(set(d))
            ) == 2:
                digit_map[3] = d
            else:
                digit_map[5] = d

        elif len(d) == 6:
            if len(
                set(digit_map.get(4, ''))
                .intersection(set(d))
            ) == 4:
                digit_map[9] = d
            elif len(
                set(digit_map.get(1, ''))
                .intersection(set(d))
            ) == 2:
                digit_map[0] = d
            else:
                digit_map[6] = d
        else:
            continue

    digit_map = {
        symbols: digit
        for digit, symbols in digit_map.items()
    }

    return digit_map


def translate_display(
    digit_map: typing.Dict[str, int],
    display: typing.List[str],
) -> typing.List[int]:
    display = [
        digit_map.get(digit)
        for digit in display
    ]
    display = [
        d
        for d in display
        if d is not None
    ]

    return display


def run(input_file: str) -> None:
    data = _read_data(input_file)

    outputs = []

    for line in data:
        digit_map = build_digit_map(line.digits)
        display = translate_display(digit_map, line.display)

        outputs.append(display)

    print('digit counts: ')
    print(len([
        d
        for display in outputs
        for d in display
    ]))

    display_value = 0

    for display in outputs:
        display_value += functools.reduce(
            lambda x, y: x * 10 + y,
            display
        )

    print(f'displays sum - {display_value}')


if __name__ == '__main__':
    args = parse_args()

    run(args.input)
