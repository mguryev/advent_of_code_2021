import argparse
import functools
import itertools
import heapq
import operator
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

    translated_input = ''.join([
        bit
        for char in lines[0]
        for bit in format(int(char, 16), '04b')
    ])

    return translated_input


class Packet:
    def __init__(self, version, packet_type, sub_packets):
        self.version = version
        self.packet_type = packet_type
        self.sub_packets = sub_packets

    @staticmethod
    def parse(
        packet_version,
        packet_type,
        stream,
    ) -> typing.Tuple['Packet', str]:
        raise NotImplemented

    def value(self):
        raise NotImplemented

    # version: int
    # type: int
    # value: str
    # sub_packets: typing.List['Packet']


class PacketLiteral(Packet):
    def __init__(self, version, packet_type, value):
        super().__init__(version, packet_type, [])
        self.__value = value

    @staticmethod
    def parse(
        packet_version,
        packet_type,
        stream,
    ) -> typing.Tuple['Packet', str]:
        value = ''

        while stream:
            next = stream[:5]
            value += next[1:]
            stream = stream[5:]

            if next[0] == '0':
                break
        else:
            raise RuntimeError

        value = int(value, 2)

        return (
            PacketLiteral(
                packet_version,
                packet_type,
                value,
            ),
            stream
        )

    def value(self):
        return self.__value


class PacketOperator(Packet):
    def __init__(self, version, packet_type, sub_packets, operator_fn):
        super().__init__(version, packet_type, sub_packets)
        self.__operator_fn = operator_fn

    @staticmethod
    def __parse_operator(packet_type):
        if packet_type == 0:
            def _sum(*values):
                return functools.reduce(
                    operator.add, values
                )

            return _sum

        if packet_type == 1:
            def prod(*values):
                return functools.reduce(
                    operator.mul, values
                )

            return prod

        if packet_type == 2:
            def _min(*values):
                return min(values)
            return _min

        if packet_type == 3:
            def _max(*values):
                return max(values)
            return _max

        if packet_type == 5:
            return operator.gt

        if packet_type == 6:
            return operator.lt

        if packet_type == 7:
            return operator.eq

    @classmethod
    def parse(
        cls,
        packet_version,
        packet_type,
        stream,
    ) -> typing.Tuple['Packet', str]:
        operator_type = stream[0]
        stream = stream[1:]

        sub_packets = []

        if operator_type == '0':
            packet_length = int(stream[: 15], 2)
            stream = stream[15:]

            content = stream[:packet_length]
            stream = stream[packet_length:]

            while content:
                sub_packet, content = parse_packet(content)
                sub_packets.append(sub_packet)
        else:
            num_sub_packets = int(stream[: 11], 2)
            stream = stream[11:]

            for _ in range(num_sub_packets):
                sub_packet, stream = parse_packet(stream)
                sub_packets.append(sub_packet)

        operator_fn = cls.__parse_operator(packet_type)

        return (
            PacketOperator(
                packet_version,
                packet_type,
                sub_packets,
                operator_fn
            ),
            stream
        )

    def value(self):
        values = [p.value() for p in self.sub_packets]

        print(self.__operator_fn)
        print(values)

        return self.__operator_fn(*values)


def parse_packet(stream: str) -> typing.Tuple[Packet, str]:
    packet_version = int(stream[:3], 2)
    packet_type = int(stream[3:6], 2)
    stream = stream[6:]

    if packet_type == 4:
        return PacketLiteral.parse(
            packet_version, packet_type, stream
        )

    else:
        return PacketOperator.parse(
            packet_version, packet_type, stream
        )


def sum_packet_version(packet: Packet) -> int:
    if not packet.sub_packets:
        return packet.version

    return sum(
        sum_packet_version(p)
        for p in packet.sub_packets
    ) + packet.version


def run(input_file: str) -> None:
    stream = _read_data(input_file)

    packets = []

    versions_sum = 0
    value = 0

    while len(stream) > 7:
        packet, stream = parse_packet(stream)
        packets.append(packet)
        versions_sum += sum_packet_version(packet)
        value = packet.value()

    print('versions sum:', versions_sum)
    print('value:', value)


if __name__ == '__main__':
    args = parse_args()

    run(args.input)
