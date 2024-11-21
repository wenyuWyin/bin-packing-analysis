from pyperf import BenchmarkSuite
from os.path import exists
import matplotlib.pyplot as plt


class ExecutionAnalyzer():

    def __init__(self, datafile: str) -> None:
        # 'outputs/output.json'
        if not exists(datafile):
            raise UserWarning(
                'Please run the benchmark file before reading the results!')
        self.datafile = datafile

    def extract_benchmark_algos(self) -> set[str]:
        suite = BenchmarkSuite.load(self.datafile)
        context = suite.get_benchmark_names()
        return context

    def load_bench_measurements(self, name: str) -> list[float]:
        '''
            extract the values for a given benchmark
        '''
        suite = BenchmarkSuite.load(self.datafile)
        bench = suite.get_benchmark(name)
        return list(bench.get_values())

    def load_all_measurement(self):
        '''
            extract the results of all benchmarks
        '''
        all_names = self.extract_benchmark_algos()
        names = []
        avg_time = []
        for name in all_names:
            results = self.load_bench_measurements(name)
            substr = 'average execution time is'
            print(f"{name}'s {substr} {sum(results) / len(results)}")
            if 'Refined' in name:
                name = 'Online\nRFF'
            else:
                name = '\n'.join(name.split()[:2])
            names.append(name)
            avg_time.append(sum(results) / len(results))
        return names, avg_time

    def plot_measurement(self):
        x_values, y_values = self.load_all_measurement()
        plt.rc('xtick', labelsize=8)
        plt.bar(x_values, y_values)
        plt.yscale('log')

        # plt.legend(loc='center left', bbox_to_anchor=(1, 0.5))
        plt.title('Average Execution Time of Each Algorithm (ms)')
        plt.xlabel('Algorithm Name')
        plt.ylabel('Average Execution Time')
        plt.show()


def main():
    reader = ExecutionAnalyzer('outputs/output.json')
    reader.plot_measurement()


if __name__ == "__main__":
    main()
