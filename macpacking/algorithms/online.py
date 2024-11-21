from .. import Solution, WeightStream
from ..model import Online
from .categorize import normalize


class NextFit(Online):

    def _process(self, capacity: int, stream: WeightStream) -> Solution:
        bin_index = 0
        solution = [[]]
        remaining = capacity
        for w in stream:
            if remaining >= w:
                solution[bin_index].append(w)
                remaining = remaining - w
            else:
                bin_index += 1
                solution.append([w])
                remaining = capacity - w
        return solution


class WorstOnline(Online):

    def _process(self, capacity: int, stream: WeightStream) -> Solution:
        solution = []
        # Create a bin for each item
        for w in stream:
            solution.append([w])
        return solution


class FirstFit(Online):

    def _process(self, capacity: int, stream: WeightStream) -> Solution:
        solution = [[]]
        for w in stream:
            bin_index = 0
            # From the first bin, find the bin where
            # the current item can fit in
            while bin_index < len(solution):
                if sum(solution[bin_index]) + w < capacity:
                    solution[bin_index].append(w)
                    break
                # Create a bin if no bin can hold the current item
                if bin_index == len(solution) - 1:
                    solution.append([w])
                    break
                bin_index += 1
        return solution


class BestFit(Online):

    def _process(self, capacity: int, stream: WeightStream) -> Solution:
        solution = [[[], capacity]]
        for w in stream:
            min_diff = capacity
            insert_index = -1
            bin_index = 0
            # find the bin with the maximum load which the item can fit in
            while bin_index < len(solution):
                # Check if the current bin is the best bin to insert the item
                if solution[bin_index][1] <= min_diff:
                    # Check if the item fits into the bin
                    if solution[bin_index][1] - w >= 0:
                        insert_index = bin_index
                        min_diff = solution[bin_index][1]
                bin_index += 1
            # Create a new bin if the current item fits into no bin
            if insert_index == -1:
                solution.append([[w], capacity - w])
            # Insert the item into the appropriate bin
            else:
                solution[insert_index][0].append(w)
                solution[insert_index][1] -= w
        return [s[0] for s in solution]


class WorstFit(Online):

    def _process(self, capacity: int, stream: WeightStream) -> Solution:
        solution = [[[], capacity]]
        for w in stream:
            bin_index = 0
            max_space = -1
            max_index = 0
            # find the bin with the maximum unused space
            # which the item can fit in
            while bin_index < len(solution):
                c = solution[bin_index][1]
                if c >= w and c - w > max_space:
                    # store the bin's index and max_space
                    max_index = bin_index
                    max_space = c - w
                bin_index += 1
            # if not find such a bin, create new bin
            if max_space == -1:
                solution.append([[w], capacity - w])
            # insert the item into the correct bin
            else:
                solution[max_index][0].append(w)
                solution[max_index][1] -= w
        return [s[0] for s in solution]


class RefinedFirstFit(Online):

    def _process(self, capacity: int, stream: WeightStream) -> Solution:
        solution = [[[]], [[]], [[]], [[]]]
        i = 0
        # Normalize/Categorize the weights
        for w in stream:
            size_class = normalize(w, capacity)
            # add A1 item into Class 1
            if size_class == 0:
                solution[0] = RefinedFirstFit._first_fit(
                    capacity, w, solution[0])
            # add B1 item into Class 2
            elif size_class == 1:
                solution[1] = RefinedFirstFit._first_fit(
                    capacity, w, solution[1])
            elif size_class == 2:
                i += 1
                if (i % 6 == 0 or i % 7 == 0 or i % 8 == 0 or i % 9 == 0):
                    solution[0] = RefinedFirstFit._first_fit(
                        capacity, w, solution[0])
                # Otherwise, add to class 3
                else:
                    solution[2] = RefinedFirstFit._first_fit(
                        capacity, w, solution[2])
            # add X item into Class 4
            else:
                solution[3] = RefinedFirstFit._first_fit(
                    capacity, w, solution[3])

        all_solution = solution[0] + solution[1] + solution[2] + solution[3]

        return [sol for sol in all_solution if sol]

    @staticmethod
    def _first_fit(capacity: int, current_w: int,
                   bins: list[list[int]]) -> list[list[int]]:
        # first fit algorithm specifically for refined fit
        for i, bin in enumerate(bins):
            if sum(bin) + current_w < capacity:
                bin.append(current_w)
                break
            # add the item as a new list if every bin fails to hold it
            if i == len(bins) - 1:
                bins.append([current_w])
                break
        return bins
