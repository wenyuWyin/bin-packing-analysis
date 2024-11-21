from typing import Any


def find_child_keys(d: dict) -> list[Any]:
    '''
        Find keys of a nested dictionary
        Example Usage:
        input: d = {'a': {'1': [], '2': []}, 'b': {'1': [], '2': []}}
        output: ['1', '2']
        note: use this when the keys in all nested dictionaries are the same
    '''
    return d[list(d.keys())[0]].keys()
