from abc import ABC, abstractmethod
from os import path
from random import shuffle, seed
from . import WeightSet, WeightStream
import csv


class DatasetReader(ABC):

    def offline(self) -> WeightSet:
        '''Return a WeightSet to support an offline algorithm'''
        (capacity, weights) = self._load_data_from_disk()
        seed(42)          # always produce the same shuffled result
        shuffle(weights)  # side effect shuffling
        return (capacity, weights)

    def online(self) -> WeightStream:
        '''Return a WeighStream, to support an online algorithm'''
        (capacity, weights) = self.offline()

        def iterator():  # Wrapping the contents into an iterator
            for w in weights:
                yield w  # yields the current value and moves to the next one

        return (capacity, iterator())

    @abstractmethod
    def _load_data_from_disk(self) -> WeightSet:
        '''Method that read the data from disk, depending on the file format'''
        pass


class BinppReader(DatasetReader):
    '''Read problem description according to the BinPP format'''

    def __init__(self, filename: str) -> None:
        if not path.exists(filename):
            raise ValueError(f'Unkown file [{filename}]')
        self.__filename = filename

    def _load_data_from_disk(self) -> WeightSet:
        with open(self.__filename, 'r') as reader:
            nb_objects: int = int(reader.readline())
            capacity: int = int(reader.readline())
            weights = []
            for _ in range(nb_objects):
                weights.append(int(reader.readline()))
            return (capacity, weights)


class JburkardtReader(DatasetReader):
    '''Read problem description according to the Jburkardt format
       Input: filename should be in format: p0<n>_'''

    def __init__(self, filename: str) -> None:
        c_filename = filename + 'c.txt'
        w_filename = filename + 'w.txt'
        if not path.exists(c_filename) or not path.exists(w_filename):
            raise ValueError(f'Unkown file [{filename}]')
        self.__c_filename = c_filename
        self.__w_filename = w_filename

    def _load_data_from_disk(self) -> WeightSet:
        capacity: int = self._load_c_file()
        weights: list[int] = self._load_w_file()
        return (capacity, weights)

    # get capacity from file
    def _load_c_file(self) -> int:
        with open(self.__c_filename, 'r') as reader:
            return int(reader.readline())

    # get weights from file
    def _load_w_file(self) -> list[int]:
        with open(self.__w_filename, 'r') as reader:
            # Get rid of empty lines at the end of the file
            content = reader.readlines()
            content = [line for line in content if line != '\n']
            weights = []
            for line in content:
                weights.append(int(line.strip()))
            return weights


class OracleReader():
    '''Read optimal solutions of each dataset'''

    def __init__(self, file_name):
        self.path = '_datasets/' + file_name + '_oracle.csv'

    def read_file(self) -> dict[str: int]:
        ''' Read .csv files '''
        with open(self.path, newline='') as csvfile:
            spamreader = csv.reader(csvfile)
            next(spamreader, None)
            # parse the opened file
            optimal_sol = {}
            for row in spamreader:
                optimal_sol[row[0]] = int(row[1])
            return optimal_sol
