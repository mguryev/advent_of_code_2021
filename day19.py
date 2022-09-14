import argparse
import itertools
import re
import typing

from dataclasses import dataclass


def parse_args():
    parser = argparse.ArgumentParser()

    parser.add_argument('input')

    return parser.parse_args()


def _read_data(input_file) -> typing.List['Scanner']:
    with open(input_file) as _input:
        lines = _input.read().splitlines()

    scanners = []

    scanner_pattern = re.compile(r'-* scanner (\d*) ---')

    while lines:
        next_line = lines.pop(0)
        scanner_id = scanner_pattern.match(next_line).group(0)
        new_scanner = Scanner(
            id=scanner_id,
            x=0, y=0, z=0,
            beacons=[]
        )

        while lines and lines[0] != '':
            next_line = lines.pop(0)
            x, y, z = next_line.split(',')

            new_scanner.beacons.append(
                Beacon(int(x), int(y), int(z))
            )
        else:
            # remove empty line
            if lines:
                lines.pop(0)

        scanners.append(new_scanner)

    return scanners


@dataclass(frozen=True)
class Beacon:
    x: int
    y: int
    z: int


@dataclass
class Scanner:
    id: str
    x: int
    y: int
    z: int
    beacons: typing.List[Beacon]


def fingerprint_beacon(beacon: Beacon, neighbours: typing.List[Beacon]):
    fingerprint = []

    for neighbour in neighbours:
        distance = pow((
                pow(beacon.x - neighbour.x, 2)
                + pow(beacon.y - neighbour.y, 2)
                + pow(beacon.z - neighbour.z, 2)
        ), 0.5)

        fingerprint.append((distance, neighbour))

    return sorted(fingerprint)


def fingerprints_match(
        fingerprints_a: typing.List[typing.Tuple[float, Beacon]],
        fingerprints_b: typing.List[typing.Tuple[float, Beacon]],
):
    matching_fingerprints = []

    fingerprints_a = sorted(fingerprints_a)
    fingerprints_b = sorted(fingerprints_b)

    while fingerprints_a and fingerprints_b:
        distance_a, _ = fingerprints_a[0]
        distance_b, _ = fingerprints_b[0]

        if distance_a == distance_b:
            matching_fingerprints.append(distance_a)
            fingerprints_a.pop(0)
            fingerprints_b.pop(0)
            continue

        if distance_a < distance_b:
            fingerprints_a.pop(0)
            continue

        if distance_a > distance_b:
            fingerprints_b.pop(0)
            continue

    return len(matching_fingerprints) >= 10


def translate(distance, translation: typing.List[int]):
    translated = list(distance)

    for coord, translation in zip(distance, translation):
        if translation < 0:
            coord *= -1

        translated[abs(translation) - 1] = coord

    return translated


def overlap_scanners(mapped_scanner: Scanner, to_map_scanner: Scanner):
    fingerprints_a = {
        beacon: fingerprint_beacon(beacon, mapped_scanner.beacons[:idx] + mapped_scanner.beacons[idx + 1:])
        for idx, beacon in enumerate(mapped_scanner.beacons)
    }

    fingerprints_b = {
        beacon: fingerprint_beacon(beacon, to_map_scanner.beacons[:idx] + to_map_scanner.beacons[idx + 1:])
        for idx, beacon in enumerate(to_map_scanner.beacons)
    }

    matching_beacons_a = {}
    matching_beacons_b = {}

    for beacon_a, beacon_b in itertools.product(fingerprints_a.keys(), fingerprints_b.keys()):
        if not fingerprints_match(fingerprints_a[beacon_a], fingerprints_b[beacon_b]):
            continue

        matching_beacons_a[beacon_a] = matching_beacons_a.get(beacon_a, []) + [beacon_b]
        matching_beacons_b[beacon_b] = matching_beacons_b.get(beacon_b, []) + [beacon_a]

    matching_beacons = []

    for beacon_a in matching_beacons_a.keys():
        if len(matching_beacons_a[beacon_a]) > 1:
            continue

        beacon_b = matching_beacons_a[beacon_a][0]

        if len(matching_beacons_b[beacon_b]) > 1:
            continue

        matching_beacons.append((
            beacon_a, beacon_b
        ))

    if len(matching_beacons) < 12:
        raise ValueError('scanners dont match')

    matching_beacon_a = list(matching_beacons_a.keys())[0]
    matching_beacon_b = matching_beacons_a[matching_beacon_a][0]

    distances_a = [
        [
            matching_beacon_a.x - neighbour.x,
            matching_beacon_a.y - neighbour.y,
            matching_beacon_a.z - neighbour.z,
        ]
        for distance, neighbour in fingerprints_a[matching_beacon_a]
        if neighbour in matching_beacons_a
    ]

    distances_b = [
        [
            matching_beacon_b.x - neighbour.x,
            matching_beacon_b.y - neighbour.y,
            matching_beacon_b.z - neighbour.z,
        ]
        for distance, neighbour in fingerprints_b[matching_beacon_b]
        if neighbour in matching_beacons_b
    ]

    for translate_x, translate_y, translate_z in itertools.product(
            [1, -1], [2, -2], [3, -3],
    ):
        matching_translation = None

        for translation in itertools.permutations(
                [translate_x, translate_y, translate_z], 3
        ):
            translated_distances = [
                translate(distance, translation)
                for distance in distances_b
            ]

            if sorted(distances_a) == sorted(translated_distances):
                matching_translation = translation
                break

        if matching_translation:
            break
    else:
        raise RuntimeError('could not translate coords')

    matching_beacon_b = Beacon(
        *translate(
            (matching_beacon_b.x, matching_beacon_b.y, matching_beacon_b.z),
            matching_translation
        )
    )

    updated_scanner = Scanner(
        id=to_map_scanner.id,
        x=(matching_beacon_a.x - matching_beacon_b.x),
        y=(matching_beacon_a.y - matching_beacon_b.y),
        z=(matching_beacon_a.z - matching_beacon_b.z),
        beacons=[]
    )

    for beacon in to_map_scanner.beacons:
        translated_coords = translate(
            (beacon.x, beacon.y, beacon.z),
            matching_translation,
        )
        x, y, z = translated_coords

        translated_beacon = Beacon(
            updated_scanner.x + x,
            updated_scanner.y + y,
            updated_scanner.z + z,
        )

        updated_scanner.beacons.append(translated_beacon)

    return updated_scanner


def run(input_file: str) -> None:
    scanners = _read_data(input_file)

    mapped_scanners = [scanners[0]]
    scanners.pop(0)

    while scanners:
        for idx, scanner in enumerate(scanners):
            updated_scanner = None

            for mapped_scanner in mapped_scanners:
                try:
                    updated_scanner = overlap_scanners(mapped_scanner, scanner)
                    break

                except ValueError:
                    continue

            if not updated_scanner:
                continue

            mapped_scanners.append(updated_scanner)
            scanners.pop(idx)
            break

        else:
            raise RuntimeError('Could not map a scanner')

    beacons = set()

    for scanner in mapped_scanners:
        for b in scanner.beacons:
            beacons.add((b.x, b.y, b.z))

    for s in mapped_scanners:
        print(s.id, s.x, s.y, s.z)

    print(len(beacons))

    max_distance = 0

    for a, b in itertools.combinations(mapped_scanners, r=2):
        distance = abs(a.x - b.x) + abs(a.y - b.y) + abs(a.z - b.z)
        max_distance = max([max_distance, distance])

    print(max_distance)


if __name__ == '__main__':
    args = parse_args()

    run(args.input)
