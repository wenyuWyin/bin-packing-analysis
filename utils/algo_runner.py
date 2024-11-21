from macpacking.model import Offline, Online, ExtendOffline, BinPacker
from macpacking.reader import DatasetReader, BinppReader, JburkardtReader
from utils.algo_util import get_algo_name
import os


def choose_reader(dataset: str) -> DatasetReader:
    '''
        Choose an appropriate reader based on the dataset given
    '''
    if 'binpp' in dataset:
        return BinppReader(dataset)
    else:
        return JburkardtReader(dataset)


def run_off(algo: Offline, dataset: str) -> list[list[int]]:
    '''
        Run offline algorithms
    '''
    reader: DatasetReader = choose_reader(dataset)
    strategy: Offline = algo()
    result = strategy(reader.offline())
    return result


def run_on(algo: Online, dataset: str) -> list[list[int]]:
    '''
        Run online algorithms
    '''
    reader: DatasetReader = choose_reader(dataset)
    strategy: Online = algo()
    result = strategy(reader.online())
    return result


def run_extend(algo: ExtendOffline, dataset: str,
               bins: int) -> list[list[int]]:
    '''
        Run extended offline algorithms
    '''
    reader: DatasetReader = choose_reader(dataset)
    strategy: ExtendOffline = algo()
    result = strategy(reader.offline(), bins)
    return result


def run_algo(algo: BinPacker, dataset: str, **bins: dict[str: int]):
    '''
        Run any algorithm
    '''
    name = get_algo_name(algo)
    if 'Online' in name:
        return run_on(algo, dataset)
    elif 'ExtendOffline' in name:
        return run_extend(algo, dataset, list(bins.values())[0])
    elif 'Offline' in name:
        return run_off(algo, dataset)


def run_in_folder(algo: BinPacker, data_folder: str, bins: list[int])\
        -> dict[str: list[list[int]]]:
    '''
        Run algorithm on all files in a folder
    '''
    results = {}
    data_folder = f'_datasets/{data_folder}'
    files = os.listdir(data_folder)
    # Run jburkardt dataset differently since the file names
    # have different formats
    if 'jburkardt' in data_folder:
        path = set()
        for f in files:
            path.add(f'_datasets/jburkardt/{f.split("_")[0]}_')
        path.remove('_datasets/jburkardt/_')
        for i, f in enumerate(path):
            # Add path in proper format (e.g., p01_)
            subs = f.split('/')[-1].strip('_')
            results[f'{subs[0]}-{subs[1:]}'] = run_algo(algo, f, bins=bins[i])
    else:
        for i, f in enumerate(files):
            path = f'{data_folder}/{f}'
            results[f.split('.')[0]] = run_algo(algo, path, bins=bins[i])
    return results
