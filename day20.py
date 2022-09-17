import argparse
import itertools
import re
import typing

from dataclasses import dataclass


def parse_args():
    parser = argparse.ArgumentParser()

    parser.add_argument('input')

    return parser.parse_args()


def _read_data(input_file):
    with open(input_file) as _input:
        lines = _input.read().splitlines()

    rewrite_map = lines[0]

    image = [
        ''.join([
            pixel
            for x, pixel in enumerate(line)
        ])
        for y, line in enumerate(lines[2:])
    ]

    return rewrite_map, image


def get_image_pixel(image, x, y, default):
    image_size_y = len(image)
    image_size_x = len(image[0])

    if not(
        0 <= x < image_size_x
        and
        0 <= y < image_size_y
    ):
        return default

    return image[y][x]


def read_image_frame(image, x, y, frame_size, default):
    return [
        get_image_pixel(image, x + x_offset, y + y_offset, default)
        for y_offset in range(frame_size)
        for x_offset in range(frame_size)
    ]


def translate_image_frame(rewrite_map, frame):
    pixel_map = {
        '#': '1',
        '.': '0',
    }

    frame = ''.join(pixel_map[p] for p in frame)
    frame_value = int(frame, 2)

    new_pixel = rewrite_map[frame_value]
    return new_pixel


def extend_image(image, pad_with, padding):
    image_size_y = len(image)
    image_size_x = len(image[0]) if image_size_y > 0 else 0

    empty_line = ''.join([pad_with] * (image_size_x + padding * 2))
    line_padding = ''.join([pad_with] * padding)

    return (
        [empty_line] * padding
        +
        [
            line_padding + line + line_padding
            for line in image
        ]
        +
        [empty_line] * padding
    )


def process_image(rewrite_map, image, frame_size, default_pixel):
    result = []

    padding = frame_size - 1

    image_size_y = len(image)
    image_size_x = len(image[0])

    for y in range(-padding, image_size_y):
        line = []
        for x in range(-padding, image_size_x):
            frame = read_image_frame(image, x, y, frame_size, default_pixel)
            new_pixel = translate_image_frame(rewrite_map, frame)

            line.append(new_pixel)

        result.append(''.join(line))

    return result


def print_image(image):
    for line in image:
        print(line)


def run(input_file: str) -> None:
    rewrite_map, image = _read_data(input_file)

    print('original image')
    print_image(image)
    print('')

    default_pixel = '.'
    frame_size = 3

    for layer in range(50):
        print('applying layer', layer)
        image = process_image(rewrite_map, image, frame_size, default_pixel=default_pixel)
        print_image(image)
        print('')

        default_pixel = translate_image_frame(rewrite_map, [default_pixel] * frame_size * frame_size)

    dark_pixels = 0

    for line in image:
        dark_pixels += len([
            pixel for pixel in line if pixel == '#'
        ])

    print('dark pixels:', dark_pixels)


if __name__ == '__main__':
    args = parse_args()

    run(args.input)
