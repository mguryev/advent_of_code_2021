import argparse
import json
import typing


def parse_args():
    parser = argparse.ArgumentParser()

    parser.add_argument('input')

    return parser.parse_args()


def _read_data(input_file) -> typing.Dict[str, str]:
    """
    Return incidence map
    """
    with open(input_file) as _input:
        lines = _input.read().splitlines()

    incidence_map = {}

    for line in lines:
        node_a, node_b = line.split('-')

        incidence_map[node_a] = incidence_map.get(node_a, []) + [node_b]
        incidence_map[node_b] = incidence_map.get(node_b, []) + [node_a]

    return incidence_map


def find_paths(
    incidence_map: typing.Dict[str, str],
    ignore_node_list: typing.Set[str],
    revisit_list: typing.Set[str],
    path: typing.List[str],
):
    current_node = path[-1]

    if current_node == 'end':
        return [path]

    next_steps = incidence_map[current_node]
    next_steps = set(next_steps).difference(ignore_node_list)

    paths = []

    for next_node in next_steps:
        if next_node in revisit_list:
            # Remove the node from reduce list but don't ignore it
            _revisit_list = revisit_list.difference({next_node})
            _ignore_node_list = ignore_node_list
        elif next_node.islower():
            # minor caves should not be revisited
            _revisit_list = revisit_list
            _ignore_node_list = ignore_node_list.union({next_node})
        else:
            # major caves could be reused
            _revisit_list = revisit_list
            _ignore_node_list = ignore_node_list

        paths += find_paths(
            incidence_map,
            _ignore_node_list,
            _revisit_list,
            path + [next_node],
        )

    return paths


def run(input_file: str) -> None:
    incidence_map = _read_data(input_file)

    print(json.dumps(
        incidence_map
    ))

    results = set()

    nodes_to_revisit = set(
        incidence_map.keys()
    ).difference({
        'start',
        'end',
    })

    for node in nodes_to_revisit:
        paths = find_paths(
            incidence_map,
            ignore_node_list={'start'},
            revisit_list={node},
            path=['start'],
        )

        paths = {
            ','.join(path)
            for path in paths
        }

        results = results.union(paths)

    print('results:')
    for path in results:
        print(path)

    print(len(results))


if __name__ == '__main__':
    args = parse_args()

    run(args.input)
