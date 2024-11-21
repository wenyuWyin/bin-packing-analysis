from macpacking.model import BinPacker, Offline, Online
from macpacking.reader import OracleReader
from utils.algo_runner import run_in_folder
from utils.dict_util import find_child_keys
from utils.plot_util import set_attributes
from utils.algo_util import get_algo_name
import matplotlib.pyplot as plt
import os
import re
import json


class Analyst:

    def __init__(self, off_algos: list[Offline],
                 on_algos: list[Online], datasets: list[str],
                 out1: str = 'discrete_out.json',
                 out2: str = 'continuous_out.json',
                 out3: str = 'normalized_out.json') -> None:
        self.datasets = datasets
        self.oracle_readers = []
        for dataset in datasets:
            self.oracle_readers.append(OracleReader(dataset))

        self.off_algos = off_algos
        self.on_algos = on_algos

        self.out1 = out1
        self.out2 = out2
        self.out3 = out3

        # Create data structure to store discrete and continuous results
        # e.g., {<NextFit object>: ['N1C1W1_A': 3, 'N1C1W1_B': 4]}
        self.discrete: dict[BinPacker: dict[str: bool]] = {
            get_algo_name(algo): {} for algo in on_algos + off_algos}
        self.continuous: dict[BinPacker: dict[str: int]] = {
            get_algo_name(algo): {} for algo in on_algos + off_algos}
        self.normalize_continuous: dict[BinPacker: dict[str: int]] = {
            get_algo_name(algo): {} for algo in on_algos + off_algos}

    def obtain_results(self) -> None:
        # Add binpp datasets separately
        # since it is structured a bit differently
        all_path = []
        if 'binpp' in self.datasets:
            all_path = Analyst.gen_binpp_path()
        # Add the rest of datasets
        for dataset in self.datasets:
            if dataset != 'binpp':
                all_path.append(dataset)
        # Conduct tests on all datasets
        for i, path in enumerate(all_path):
            for algo in self.on_algos:
                # [0] * 100 as a place holder
                on_result = run_in_folder(algo, path, [0]*100)
                self.check_result(on_result, algo)
            for algo in self.off_algos:
                off_result = run_in_folder(algo, path, [0]*100)
                self.check_result(off_result, algo)
            if (i % 3 == 0):
                print(".", end="")

    def obtain_op_results(self) -> dict[dict[str: int]]:
        # Extract optimal results from the oracle files
        self.op_results = {}
        for i, reader in enumerate(self.oracle_readers):
            self.op_results[self.datasets[i]] = reader.read_file()

    def check_result(self, result: dict[str: list[list[int]]],
                     algo: BinPacker) -> None:
        # Check result of an algorithm against the optimal solution
        algo = get_algo_name(algo)
        for file, sol in result.items():
            # Check results for binpp dataset
            if re.search(r'N\d{1}C\d{1}W\d{1}', file) is not None:
                op_sol = self.op_results['binpp'][file]
                self.discrete[algo][file] = op_sol == len(sol)
                self.continuous[algo][file] = len(sol) - op_sol
                self.normalize_continuous[algo][file] =\
                    (len(sol) - op_sol) / op_sol
            # Check results for binpp-hard dataset
            elif re.search('HARD', file) is not None:
                op_sol = self.op_results['binpp-hard'][file]
                self.discrete[algo][file] = op_sol == len(sol)
                self.continuous[algo][file] = len(sol) - op_sol
                self.normalize_continuous[algo][file] =\
                    (len(sol) - op_sol) / op_sol
            # Check results for jburkardt dataset
            elif re.search(r'p-\d{2}', file) is not None:
                file = file.replace('-', '_')
                op_sol = self.op_results['jburkardt'][file]
                self.discrete[algo][file] = (
                    op_sol == len(sol))
                self.continuous[algo][file] = len(sol) - op_sol
                self.normalize_continuous[algo][file] =\
                    (len(sol) - op_sol) / op_sol

    @staticmethod
    def gen_binpp_path() -> list[str]:
        '''
            Get all file paths in of binpp dataset
        '''
        all_folder = os.listdir('_datasets/binpp')
        all_folder.remove('_source.txt')
        return [f'binpp/{folder}' for folder in all_folder]

    def write_result(self):
        '''
            Write the result to a .json file
        '''
        with open(f'outputs/{self.out1}', 'w') as f:
            data = json.dumps(self.discrete)
            f.write(data)
        with open(f'outputs/{self.out2}', 'w') as f:
            data = json.dumps(self.continuous)
            f.write(data)
        with open(f'outputs/{self.out3}', 'w') as f:
            data = json.dumps(self.normalize_continuous)
            f.write(data)

    def plot_result(self) -> None:
        '''
            Plot the results
        '''
        # Obtain the resutls if the output files doesn't exist
        f1 = f'outputs/{self.out1}'
        f2 = f'outputs/{self.out2}'
        f3 = f'outputs/{self.out3}'
        if (not os.path.exists(f1) or not os.path.exists(f2)
                or not os.path.exists(f3)):
            self.obtain_results()
            self.write_result()

        ''' Example format for c_result:
        {'Online NextFit': {'N1C1W1_A': 1, 'N1C1W1_B': 1},
        'Online FirstFit': {'N1C1W1_A': 2, 'N1C1W1_B': 1}}'''
        _, _, c_result = Analyst.read_result(f1, f2, f3)

        # Get ticks for the graph
        tick = self._find_tick(find_child_keys(c_result))

        # Plot result for online algorithms
        plt.figure(0, figsize=(14, 8))
        for algo in list(c_result.keys()):
            if 'Online' in algo:
                plt.plot(list(c_result[algo].keys()),
                         list(c_result[algo].values()), label=algo, alpha=0.4)

        plt.xticks(ticks=[i for i in range(len(tick))],
                   labels=tick, rotation=60)
        set_attributes('Continuous Margin of Improvement of Algorithms',
                       'Files', 'Continuous Margin of Improvement')

        # Plot result for offline algorithms
        plt.figure(1, figsize=(14, 8))
        for algo in list(c_result.keys()):
            if 'Offline' in algo:
                plt.plot(list(c_result[algo].keys()),
                         list(c_result[algo].values()), label=algo, alpha=0.4)

        plt.xticks(ticks=[i for i in range(len(tick))],
                   labels=tick, rotation=60)
        set_attributes('Continuous Margin of Improvement of Algorithms',
                       'Files', 'Continuous Margin of Improvement')

    # Private method to find ticks for a plot
    def _find_tick(self, keys: list[str]) -> list[str]:
        ticks = []
        for k in keys:
            key = self._check_binpp(k)
            if not key:
                key = self._check_hard(k)
            if not key:
                key = self._check_jburkardt(k)
            ticks.append(key)
        return ticks

    # Private method to determine the tick for a binpp dataset
    def _check_binpp(self, key: str):
        if 'binpp' not in self.datasets:
            return ""
        binpp = os.listdir('_datasets/binpp')
        binpp.remove('_source.txt')
        name = key.split('_')[0]
        if name in binpp and 'A' in key:
            return name
        else:
            return ""

    # Private method to determine the tick for a hard dataset
    def _check_hard(self, key: str):
        if 'binpp-hard' not in self.datasets:
            return ""
        if 'HARD' in key and '0' in key:
            return key[:-1]
        else:
            return ""

    # Private method to determine the tick for a jburkardt dataset
    def _check_jburkardt(self, key: str):
        if 'jburkardt' not in self.datasets:
            return ""
        if 'p' in key and '1' in key:
            return key[0]
        else:
            return ""

    # Static method to read result file
    @staticmethod
    def read_result(f1: str,
                    f2: str,
                    f3: str) -> tuple[dict[BinPacker: dict[str, int]],
                                      dict[BinPacker: dict[str, bool]],
                                      dict[BinPacker: dict[str, float]]]:
        result = []
        with open(f1, 'r') as f:
            result.append(json.load(f))
        with open(f2, 'r') as f:
            result.append(json.load(f))
        with open(f3, 'r') as f:
            result.append(json.load(f))
        return tuple(result)
