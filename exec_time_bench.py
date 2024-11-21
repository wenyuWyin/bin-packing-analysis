from macpacking.reader import BinppReader
from macpacking.model import BinPacker
from macpacking.algorithms.offline import (NextFit as off_nf,
                                           FirstFit as off_ff,
                                           BestFit as off_bf,
                                           WorstFit as off_wf)
from macpacking.algorithms.online import (NextFit as on_nf,
                                          FirstFit as on_ff,
                                          BestFit as on_bf,
                                          WorstFit as on_wf,
                                          RefinedFirstFit as on_rff)
import pyperf


def do_bench(algos: tuple([BinPacker]), case: str) -> None:
    '''
        run the benchmark over a set of algorithm and the baseline
    '''
    runner = pyperf.Runner()
    # run benchmark on each online algorithm
    for algo in algos[0]:
        name = case.split('\\')[-1]
        data = BinppReader(case).online()
        binpacker = algo()
        runner.bench_func(
            f'Online {algo.__name__} at {name}', binpacker, data)
    # run benchmark on each offline algorithm
    for algo in algos[1]:
        name = case.split('\\')[-1]
        data = BinppReader(case).offline()
        binpacker = algo()
        runner.bench_func(
            f'Offline {algo.__name__} at {name}', binpacker, data)


def main():
    '''
        Running the complete benchmark
    '''
    offline_algos = [off_nf, off_ff, off_bf, off_wf]
    online_algos = [on_nf, on_ff, on_bf, on_wf, on_rff]
    case = '_datasets\\binpp-hard\\HARD0.BPP.txt'
    do_bench((online_algos, offline_algos), case)


if __name__ == "__main__":
    main()
