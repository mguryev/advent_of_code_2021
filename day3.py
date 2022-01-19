import argparse


def parse_args():
    parser = argparse.ArgumentParser()

    parser.add_argument('input')

    return parser.parse_args()


def _read_data(input_file):
    with open(input_file) as _input:
        data = _input.read().splitlines()

    return data


def _get_common_digit(data, digit_position):
    digits_occurence = {'0': 0, '1': 0}

    for datum in data:
        digit = datum[digit_position]
        digits_occurence[digit] += 1

    most_common_digit = (
        '1'
        if digits_occurence['1'] >= digits_occurence['0']
        else '0'
    )

    return most_common_digit


def calculate_power_rate(input_file):
    data = _read_data(input_file)
    datum_length = len(data[0])

    common_digits = []

    for digit_position in range(datum_length):
        common_digit = _get_common_digit(data, digit_position)
        common_digits.append(common_digit)

    gamma_rate = ''.join(common_digits)
    gamma_rate = int(gamma_rate, 2)

    epsilon_rate_mask = int('1' * datum_length, 2)
    epsilon_rate = gamma_rate ^ epsilon_rate_mask

    return gamma_rate * epsilon_rate


# def _oxygen_generator_filter(datum_length):
#     def mask_producer(digit_position, common_digit):
#         return common_digit << (datum_length - digit_position)
#     return mask_producer
#
#
# def _oxygen_scrubber_mask(datum_length):
#     def mask_producer(digit_position, common_digit):
#         return common_digit << (datum_length - digit_position)
#     return mask_producer

def _oxygen_generator_filter(digit_position, common_digit):
    def filter(datum):
        return datum[digit_position] == common_digit
    return filter


def _oxygen_scrubber_filter(digit_position, common_digit):
    def filter(datum):
        return datum[digit_position] != common_digit
    return filter


def _calculate_oxy_rate(filter_producer, data):
    datum_length = len(data[0])

    for digit_position in range(datum_length):
        common_digit = _get_common_digit(data, digit_position)

        rate_filter = filter_producer(digit_position, common_digit)

        data = filter(rate_filter, data)
        data = list(data)

        if len(data) == 1:
            break

    return int(data[0], 2)


def calculate_support_rating(input_file):
    data = _read_data(input_file)

    generator_rate = _calculate_oxy_rate(_oxygen_generator_filter, data)
    scrubber_rate = _calculate_oxy_rate(_oxygen_scrubber_filter, data)

    return generator_rate * scrubber_rate


if __name__ == '__main__':
    args = parse_args()
    result = calculate_power_rate(args.input)
    print('power consumption rate', result)

    result = calculate_support_rating(args.input)
    print('life support rating', result)
