from abc import ABC, abstractmethod
from typing import Iterator
from . import WeightStream, WeightSet, Solution


class BinPacker(ABC):
    pass


class Online(BinPacker):

    def __call__(self, ws: WeightStream) -> Solution:
        capacity, stream = ws
        return self._process(capacity, stream)

    @abstractmethod
    def _process(self, c: int, stream: Iterator[int]) -> Solution:
        pass


class Offline(BinPacker):

    def __call__(self, ws: WeightSet) -> Solution:
        capacity, weights = ws
        return self._process(capacity, weights)

    @abstractmethod
    def _process(self, c: int, weights: list[int]) -> Solution:
        pass


class ExtendOffline(BinPacker):
    '''
        Extended offline algorithm for Task 5
    '''

    def __call__(self, ws: WeightSet, bins: int) -> Solution:
        _, weights = ws
        return self._process(weights, bins)

    @abstractmethod
    def _process(self, weights: list[int], bins: int) -> Solution:
        pass
