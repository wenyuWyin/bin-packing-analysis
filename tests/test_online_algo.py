from macpacking.algorithms.online import (NextFit as on_nf,
                                          FirstFit as on_ff,
                                          BestFit as on_bf,
                                          WorstFit as on_wf,
                                          RefinedFirstFit as on_rff)
from macpacking.model import Online, BinPacker
from macpacking.reader import DatasetReader, JburkardtReader
import pytest


@pytest.fixture
def run_algo(algo: BinPacker, dataset: str) -> list[list[int]]:
    reader: DatasetReader = JburkardtReader(dataset)
    strategy: Online = algo()
    result = strategy(reader.online())
    return result


@pytest.mark.parametrize(['algo', 'dataset'],
                         [(on_nf, '_datasets/jburkardt/p02_')])
def test_on_nf(run_algo):
    assert run_algo == [[32, 6, 37], [43, 3, 7, 46],
                        [79, 19], [64], [50], [99], [94], [18]]


@pytest.mark.parametrize(['algo', 'dataset'],
                         [(on_ff, '_datasets/jburkardt/p02_')])
def test_on_ff(run_algo):
    assert run_algo == [[32, 6, 37, 3, 7], [43, 46],
                        [79, 19], [64, 18], [50], [99], [94]]


@pytest.mark.parametrize(['algo', 'dataset'],
                         [(on_bf, '_datasets/jburkardt/p02_')])
def test_on_bf(run_algo):
    assert run_algo == [[32, 6, 37, 3, 7], [43, 46],
                        [79, 19], [64, 18], [50], [99], [94]]


@pytest.mark.parametrize(['algo', 'dataset'],
                         [(on_wf, '_datasets/jburkardt/p02_')])
def test_on_wf(run_algo):
    assert run_algo == [[32, 6, 37, 19], [
        43, 3, 7, 46], [79], [64], [50, 18], [99], [94]]


@pytest.mark.parametrize(['algo', 'dataset'],
                         [(on_rff, '_datasets/jburkardt/p02_')])
def test_on_rff(run_algo):
    assert run_algo == [[32, 6, 37, 3, 7], [43, 46],
                        [79, 19], [64, 18], [50], [99], [94]]
