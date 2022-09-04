import argparse
import re


class Image:
    def __init__(self):
        self.__dots = {}

        self.__height = 0
        self.__width = 0

    def add_dot(self, x, y, value):
        if value is None:
            return

        self.__dots[y] = {
            **self.__dots.get(y, {}),
            **{x: value},
        }
        self.__width = max(self.__width, x)
        self.__height = max(self.__height, y)

    def get(self, x, y):
        return self.__dots.get(y, {}).get(x)

    def read(self):
        rows = sorted(list(self.__dots.keys()))

        return [
            (x, y)
            for y in rows
            for x in sorted(list(
                self.__dots[y]
            ))
        ]

    def print(self):
        print(self.__dots)
        for y in range(self.__height + 1):
            row = ''.join([
                self.__dots.get(y, {}).get(x, '.')
                for x in range(self.__width + 1)
            ])
            print(row)

    @property
    def width(self) -> int:
        return self.__width

    @property
    def height(self) -> int:
        return self.__height


def parse_args():
    parser = argparse.ArgumentParser()

    parser.add_argument('input')

    return parser.parse_args()


def _read_data(input_file):
    """
    Return incidence map
    """
    with open(input_file) as _input:
        lines = _input.read().splitlines()

    image = Image()
    instructions_start = 0
    instructions = []

    for idx, line in enumerate(lines):
        if line == '':
            instructions_start = idx + 1
            break

        x, y = line.split(',')
        x = int(x)
        y = int(y)

        image.add_dot(x, y, '#')

    for line in lines[instructions_start:]:
        instructions.append(line)

    return image, instructions


def fold(image: Image, instruction):
    pattern = re.compile(r'fold along (.*)=(.*)')

    direction, fold_line = pattern.match(instruction).groups()
    fold_line = int(fold_line)

    post_fold_image = Image()

    if direction == 'x':
        post_fold_width = max(
            fold_line - 0,
            image.width - fold_line,
        )
        fold_x = fold_line

        post_fold_height = image.height
        fold_y = image.height

    elif direction == 'y':
        post_fold_width = image.width
        fold_x = image.width

        post_fold_height = max(
            fold_line - 0,
            image.height - fold_line,
        )
        fold_y = fold_line

    else:
        raise RuntimeError('unexpected direction')

    print('post_fold_width', post_fold_width)
    print('fold_x', fold_x)

    print('post_fold_height', post_fold_height)
    print('fold_y', fold_y)

    for dot in image.read():
        x, y = dot

        if image.get(x, y) != '#':
            continue

        post_fold_image.add_dot(
            post_fold_width - abs(x - fold_x),
            post_fold_height - abs(y - fold_y),
            image.get(x, y)
        )

    if not post_fold_image.get(post_fold_width, post_fold_height):
        post_fold_image.add_dot(post_fold_width - 1, post_fold_height - 1, '.')

    return post_fold_image


def run(input_file: str) -> None:
    image, instructions = _read_data(input_file)
    image.print()

    for instruction in instructions:
        print(f'performing instruction - {instruction}')
        image = fold(image, instruction)

    image.print()


if __name__ == '__main__':
    args = parse_args()

    run(args.input)
