from macpacking.model import BinPacker
from utils.algo_runner import run_in_folder
from utils.plot_util import set_attributes, gen_color
from macpacking.reader import OracleReader
from utils.algo_util import get_algo_name
import matplotlib.pyplot as plt
from statistics import stdev


class BenchMarking():
    '''
        Class to benchmark various algorithms
    '''

    dataset = '_datasets/binpp/N1C2W1/N1C2W1_D.BPP.txt'

    def __init__(self, min_n: int, max_n: int, min_c: int, max_c: int,
                 min_w: int, max_w: int, algos: list[BinPacker]) -> None:
        self.algos = algos
        self.n_range = (min_n, max_n)
        self.c_range = (min_c, max_c)
        self.w_range = (min_w, max_w)

        # All results for online and offline algorithms
        # e.g., {NextFit: {(1, 1, 1): [[23, 24, 22],
        #                              [12.3, 15.3, 13.8],
        #                              [5.4, 3.1, 6.2]],
        #                  (2, 1, 1): [[...], [...], [...]]}}
        # Each tuple indicates different N_C_W_ folder
        self.bench_result:\
            dict[BinPacker: dict[tuple[int, int, int]:
                                 [list[int], list[float], list[float]]]] =\
            {get_algo_name(algo): {(n, c, w): [[], [], []]
                                   for n in range(min_n, max_n + 1)
                                   for c in range(min_c, max_c + 1)
                                   for w in range(min_w, max_w + 1)}
             for algo in self.algos}

        # Results for number of bins used
        self.num_bins: dict[str: list[int]] = {
            get_algo_name(algo): [] for algo in self.algos}
        # Results for average unused room in the bins
        self.cp_diff: dict[str: list[float]] = {
            get_algo_name(algo): [] for algo in self.algos}
        # Results for average standard deviation of loads in bins
        self.avg_load: dict[str: list[float]] = {
            get_algo_name(algo): [] for algo in self.algos}

    def get_result(self, param: int) -> None:
        '''
            Generate and update result for each dataset
        '''

        # get algorithms' results
        for algo in self.algos:
            name = get_algo_name(algo)
            # Calculate average number of bins
            bins = self.bench_result[name][param][0]
            avg_bins = sum(bins) / len(bins)
            substr = f'{"average number of bins:":<33}'
            print(f'{name:<25} {substr} {avg_bins:>10}')

            self.num_bins[name].append(avg_bins)

            # Calculate average unused room in bins
            cp_diff = self.bench_result[name][param][1]
            avg_cp_diff = sum(cp_diff) / len(cp_diff)
            substr = f'{"average unused room:":<33}'
            print(
                f'{"":<25} {substr} {round(avg_cp_diff, 2):>10}')

            self.cp_diff[name].append(avg_cp_diff)

            # Calculate average standard deviation for loads
            stdevs = self.bench_result[name][param][2]
            avg_stdev = sum(stdevs) / len(stdevs)
            substr = f'{"standard deviation of loads:":<33}'
            print(
                f'{"":<25} {substr} {round(avg_stdev, 2):>10}')

            self.avg_load[name].append(avg_stdev)

    def do_benchmark(self, nob=True, ur=True, stdv=True) -> None:
        '''
            Function to benchmark all algorithms
        '''
        # Do benchmark on all datasets
        for w in range(self.w_range[0], self.w_range[1] + 1):
            if w == 3:
                continue
            for c in range(self.c_range[0], self.c_range[1] + 1):
                for n in range(self.n_range[0], self.n_range[1] + 1):
                    # Convert input to number
                    lb = check_min_weight(w)
                    cp = check_capacity(c)
                    size = check_size(n)
                    s1 = f'Benchmarking {size} items'
                    s = f'{s1}, {cp} capacity, [{lb}, 100] weights'
                    print(f'****** {s} ******')
                    # Get file paths
                    folder = get_folder(n, c, w)
                    # run algorithm
                    for algo in self.algos:
                        name = get_algo_name(algo)
                        result = run_in_folder(
                            algo, f'binpp/{folder}', get_fixed_bins(folder))
                        for sol in list(result.values()):
                            cp_list = [cp - sum(bin) for bin in sol]
                            avg_cp_diff = sum(cp_list) / len(cp_list)
                            load_list = [sum(bin) for bin in sol]
                            # Record the results
                            self.bench_result[name][(n, c, w)][0].append(
                                len(sol))
                            self.bench_result[name][(n, c, w)][1].append(
                                avg_cp_diff)
                            self.bench_result[name][(n, c, w)][2].append(
                                stdev(load_list))

                    # Analyze the results
                    self.get_result((n, c, w))

                    print("========================================")
                    print()

        self.plot_results(nob=nob, ur=ur, stdv=stdv, w=1, c=1)

    def _plot_result(self, x_values: list[int],
                     on_result: dict[str: list[int]],
                     off_result: dict[str: list[int]],
                     fix_params: dict[str: int],
                     color_list: list[str]) -> None:
        needed_index = self.filter_result(fix_params)

        # plot online algorithm's results
        i = 0
        for algo, values in on_result.items():
            plt.plot(
                x_values, [v for i, v in enumerate(values)
                           if i in needed_index], label=algo,
                color=color_list[i], linewidth=2, alpha=0.7)
            i += 1

        # plot offline algorithm's results
        i = 0
        for algo, values in off_result.items():
            plt.plot(
                x_values, [v for i, v in enumerate(values)
                           if i in needed_index], ':', label=algo,
                color=color_list[i], linewidth=2, alpha=0.7)
            i += 1

    def plot_results(self, nob=True, ur=True, stdv=True,
                     **fix_params: dict[str: int]) -> None:
        '''
            Plot result with two parameters among (n, c, w) being fixed
            Input: **fix_params must contain two parameters that specify
                   the value of the fixed parameters
            Example input: fix_params = {'c': 1, 'w': 1}
        '''
        if len(fix_params) != 2:
            raise ValueError("At least two parameters need to be fixed.")
        # plot number of bins used
        if 'n' not in fix_params.keys():
            x_values = [check_size(i)
                        for i in range(self.n_range[0], self.n_range[1] + 1)]
        if 'c' not in fix_params.keys():
            x_values = [check_capacity(i)
                        for i in range(self.c_range[0], self.c_range[1] + 1)]
        if 'w' not in fix_params.keys():
            x_values = [check_min_weight(i)
                        for i in range(self.c_range[0], self.c_range[1] + 1)]

        colors = gen_color(max(self.find_num_algo()))

        if nob:
            plt.figure(0)
            on_result = {algo: result
                         for algo, result in self.num_bins.items()
                         if 'Online' in algo}
            off_result = {algo: result
                          for algo, result in self.num_bins.items()
                          if 'Offline' in algo}
            self._plot_result(x_values, on_result,
                              off_result, fix_params, colors)
            set_attributes('Number of Bins Used vs. Number of Items',
                           'Number of Items', 'Number of Bins Used')
        if ur:
            plt.figure(1)
            on_result = {algo: result
                         for algo, result in self.cp_diff.items()
                         if 'Online' in algo}
            off_result = {algo: result
                          for algo, result in self.cp_diff.items()
                          if 'Offline' in algo}
            self._plot_result(x_values, on_result,
                              off_result, fix_params, colors)
            substr = 'Average Unused Room in the Bins vs. Number of Items'
            set_attributes(substr,
                           'Number of Items',
                           'Average Unused Room in the Bins')
        if stdv:
            plt.figure(2)
            on_result = {algo: result
                         for algo, result in self.avg_load.items()
                         if 'Online' in algo}
            off_result = {algo: result
                          for algo, result in self.avg_load.items()
                          if 'Offline' in algo}
            self._plot_result(x_values, on_result,
                              off_result, fix_params, colors)
            substr = 'Standard Deviation of the loads vs. Number of Items'
            set_attributes(substr,
                           'Number of Items',
                           'Standard Deviation of Bin Loads')

        plt.show()

    def filter_result(self, fix_params: dict[str: int]):
        '''
            Extract needed results for graphing based on what parameters
            are fixed
        '''
        needed_index = []
        counter = 0
        for w in range(self.w_range[0], self.w_range[1] + 1):
            if w == 3:
                continue
            for c in range(self.c_range[0], self.c_range[1] + 1):
                for n in range(self.n_range[0], self.n_range[1] + 1):
                    # For every combination of w, c, and n,
                    # check if it will be plotted
                    if not BenchMarking.match_param('w', fix_params, w):
                        break
                    if not BenchMarking.match_param('c', fix_params, c):
                        break
                    if not BenchMarking.match_param('n', fix_params, n):
                        break
                    needed_index.append(counter)
                    counter += 1
        return needed_index

    @staticmethod
    def match_param(param: str, param_dict: dict[str: int], val: int):
        if param in param_dict.keys():
            if param_dict['w'] == val:
                return True
            else:
                return False
        return True

    def find_num_algo(self):
        return (len([0 for algo in self.algos
                     if 'Online' in get_algo_name(algo)]),
                len([0 for algo in self.algos
                    if 'Offline' in get_algo_name(algo)]))


def get_folder(n: int, c: int, w: int) -> str:
    '''
        Get path to the folder with given dataset characteristics
    '''
    return f'N{n}C{c}W{w}'


def check_capacity(c: int) -> int:
    '''
        Generate capacity with given folder number
    '''
    capacity_list = [100, 120, 150]
    return capacity_list[c - 1]


def check_size(n: int) -> int:
    '''
        Generate size with given folder number
    '''
    size_list = [50, 100, 200, 500]
    return size_list[n - 1]


def check_min_weight(w: int) -> int:
    '''
        Generate the minimal weight of an item with given folder number
    '''
    weight_list = [1, 20, 30]
    return weight_list[w - 1 - (w > 3)]


def get_fixed_bins(folder_name: str) -> list[int]:
    '''
        Extract optimal results from the oracle files
    '''
    reader = OracleReader('Binpp')
    op_results = reader.read_file()
    return [value for key, value in op_results.items() if folder_name in key]
