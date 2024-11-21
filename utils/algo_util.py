from macpacking.model import BinPacker


# method to get the full name of an algorithm
def get_algo_name(algo: BinPacker) -> str:
    parents = algo.__bases__
    return f'{parents[0].__name__} {algo.__name__}'
