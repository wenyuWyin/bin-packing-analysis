from .. import Solution
from ..model import Offline, ExtendOffline
import binpacking as bp


class BenMaier(Offline):

    def _process(self, capacity: int, weights: list[int]) -> Solution:
        return bp.to_constant_volume(weights, capacity)


class Partitioning(ExtendOffline):
    '''Baseline for Multiway Number Partitioning'''

    def _process(self, weights: list[int], num_of_bins: int) -> Solution:
        return bp.to_constant_bin_number(weights, num_of_bins)
