from macpacking.algorithms.offline import (NextFit as off_nf,
                                           FirstFit as off_ff,
                                           BestFit as off_bf,
                                           WorstFit as off_wf,
                                           GNP as gnp)
from macpacking.model import ExtendOffline, Offline, BinPacker
from macpacking.reader import DatasetReader, JburkardtReader
import pytest


@pytest.fixture
def run_algo(algo: BinPacker, dataset: str) -> list[list[int]]:
    reader: DatasetReader = JburkardtReader(dataset)
    strategy: Offline = algo()
    result = strategy(reader.offline())
    return result


@pytest.mark.parametrize(['algo', 'dataset'],
                         [(off_nf, '_datasets/jburkardt/p02_')])
def test_off_nf(run_algo):
    assert run_algo == [[99], [94], [79], [64], [
        50, 46], [43, 37], [32, 19, 18, 7, 6, 3]]


@pytest.mark.parametrize(['algo', 'dataset'],
                         [(off_ff, '_datasets/jburkardt/p02_')])
def test_off_ff(run_algo):
    assert run_algo == [[99], [94, 3], [79, 19],
                        [64, 32], [50, 46], [43, 37, 18], [7, 6]]


@pytest.mark.parametrize(['algo', 'dataset'],
                         [(off_bf, '_datasets/jburkardt/p02_')])
def test_off_bf(run_algo):
    assert run_algo == [[99], [94, 6], [79, 18, 3],
                        [64, 32], [50, 46], [43, 37, 19], [7]]


@pytest.mark.parametrize(['algo', 'dataset'],
                         [(off_wf, '_datasets/jburkardt/p02_')])
def test_off_wf(run_algo):
    assert run_algo == [[99], [94], [79, 19], [
        64, 32], [50, 46], [43, 37, 18], [7, 6, 3]]


@pytest.fixture
def run_extend_algo(algo: BinPacker, dataset: str, bin_num: int)\
        -> list[list[int]]:
    reader: DatasetReader = JburkardtReader(dataset)
    strategy: ExtendOffline = algo()
    result = strategy(reader.offline(), bin_num)
    return result


@pytest.mark.parametrize(['algo', 'dataset', 'bin_num'],
                         [(gnp, '_datasets/jburkardt/p02_', 3)])
def test_extendoff_gnp(run_extend_algo):
    assert run_extend_algo == [[99, 46, 32, 19, 3],
                               [94, 50, 37, 18], [79, 64, 43, 7, 6]]
