from .. import Solution, WeightSet
from ..model import Offline, ExtendOffline
from .online import (NextFit as Nf_online, FirstFit as Ff_online,
                     BestFit as Bf_online, WorstFit as Wf_online)


class NextFit(Offline):

    def _process(self, capacity: int, weights: WeightSet) -> Solution:
        '''An offline version of NextFit, ordering the weigh stream and
        delegating to the online version (avoiding code duplication)'''
        weights = sorted(weights, reverse=True)
        delegation = Nf_online()
        return delegation((capacity, weights))


class FirstFit(Offline):

    def _process(self, capacity: int, weights: WeightSet) -> Solution:
        '''An offline version of FirstFit, ordering the weigh stream and
        delegating to the online version (avoiding code duplication)'''
        weights = sorted(weights, reverse=True)
        delegation = Ff_online()
        return delegation((capacity, weights))


class BestFit(Offline):

    def _process(self, capacity: int, weights: WeightSet) -> Solution:
        '''An offline version of BestFit, ordering the weigh stream and
        delegating to the online version (avoiding code duplication)'''
        weights = sorted(weights, reverse=True)
        delegation = Bf_online()
        return delegation((capacity, weights))


class WorstFit(Offline):

    def _process(self, capacity: int, weights: WeightSet) -> Solution:
        '''An offline version of WorstFit, ordering the weigh stream and
        delegating to the online version (avoiding code duplication)'''
        weights = sorted(weights, reverse=True)
        delegation = Wf_online()
        return delegation((capacity, weights))


class GNP(ExtendOffline):

    def _process(self, weights: WeightSet, num_of_bins: int) -> Solution:
        '''Algorithms for Multiway Number Partitioning'''
        weights = sorted(weights, reverse=True)
        solutions = [[] for _ in range(num_of_bins)]
        current_sums = [0 for _ in range(num_of_bins)]
        for w in weights:
            # add the current item to the bin with minimal weight
            min_sum = min(current_sums)
            index = current_sums.index(min_sum)
            solutions[index].append(w)
            current_sums[index] += w

        return solutions
