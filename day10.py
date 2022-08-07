import argparse
import typing


BRACKETS = [
    ('(', ')'),
    ('[', ']'),
    ('{', '}'),
    ('<', '>'),
]

ERROR_COSTS = {
    ')': 3,
    ']': 57,
    '}': 1197,
    '>': 25137,
}

COMPLETION_COSTS = {
    '(': 1,
    '[': 2,
    '{': 3,
    '<': 4,
}


def parse_args():
    parser = argparse.ArgumentParser()

    parser.add_argument('input')

    return parser.parse_args()


def _read_data(input_file) -> typing.List[str]:
    with open(input_file) as _input:
        lines = _input.read().splitlines()

    return lines


def line_parse(line: str) -> (str, str, str):
    syntax_stack = []

    brackets_closing = {
        closing: opening
        for
        opening, closing in BRACKETS
    }

    valid_line = ''

    for symbol in line:
        if symbol not in brackets_closing:
            syntax_stack += [symbol]
            valid_line += symbol
            continue

        open_bracket = syntax_stack.pop(-1)

        if open_bracket == brackets_closing[symbol]:
            valid_line += symbol
            continue

        else:
            return valid_line, '', symbol

    # no error to return
    return valid_line, ''.join(syntax_stack), ''


def run(input_file: str) -> None:
    data = _read_data(input_file)

    complete = []
    incomplete = []
    errors = []

    for line in data:
        line, missing_symbols, error = line_parse(line)

        if error:
            errors.append(error)
            continue

        if missing_symbols:
            incomplete.append(missing_symbols)
            continue

        complete.append(line)

    print(f'complete - {complete}')

    print(f'incomplete - {incomplete}')
    completion_costs = []

    for line in incomplete:
        cost = 0
        for symbol in reversed(line):
            cost = (cost * 5) + COMPLETION_COSTS[symbol]
        completion_costs.append(cost)

    completion_costs = sorted(completion_costs)
    print(f'completion cost - {completion_costs}')
    middle_cost = completion_costs[len(completion_costs) // 2]
    print(f'middle completion cost - {middle_cost}')

    print(f'errors - {errors}')
    error_cost = sum([
        ERROR_COSTS[error]
        for error in errors
    ])
    print(f'error cost - {error_cost}')




if __name__ == '__main__':
    args = parse_args()

    run(args.input)
