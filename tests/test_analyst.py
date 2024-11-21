import pytest
from macpacking.analyst import Analyst
from macpacking.algorithms.offline import (NextFit as off_nf,
                                           FirstFit as off_ff,
                                           BestFit as off_bf,
                                           WorstFit as off_wf)
from macpacking.algorithms.online import (NextFit as on_nf,
                                          FirstFit as on_ff,
                                          BestFit as on_bf,
                                          WorstFit as on_wf)
from utils.algo_util import get_algo_name


@pytest.fixture
def setup_analyst1() -> Analyst:
    analyst = Analyst([off_nf, off_ff, off_bf, off_wf], [
                      on_nf, on_ff, on_bf, on_wf], ['jburkardt'])
    analyst.obtain_op_results()
    analyst.obtain_results()
    return analyst


@pytest.fixture
def setup_analyst2() -> Analyst:
    analyst = Analyst([off_nf, off_ff, off_bf, off_wf], [
                      on_nf, on_ff, on_bf, on_wf],
                      ['binpp', 'binpp-hard', 'jburkardt'],
                      'test_discrete_out.json',
                      'test_continuous_out.json',
                      'test_normalized_out.json')
    analyst.obtain_op_results()
    analyst.obtain_results()
    return analyst


def test_result(setup_analyst1):
    assert not setup_analyst1.discrete[get_algo_name(on_nf)]['p_02']
    assert not setup_analyst1.discrete[get_algo_name(off_nf)]['p_04']
    assert not setup_analyst1.discrete[get_algo_name(off_wf)]['p_04']
    assert setup_analyst1.discrete[get_algo_name(off_wf)]['p_03']

    assert setup_analyst1.continuous[get_algo_name(on_nf)]['p_02'] == 1
    assert setup_analyst1.continuous[get_algo_name(off_nf)]['p_04'] == 1
    assert setup_analyst1.continuous[get_algo_name(off_wf)]['p_04'] == 1
    assert setup_analyst1.continuous[get_algo_name(off_wf)]['p_03'] == 0


def test_read_write(setup_analyst2):
    setup_analyst2.write_result()
    assert Analyst.read_result('outputs/test_discrete_out.json',
                               'outputs/test_continuous_out.json',
                               'outputs/test_normalized_out.json') == \
        (setup_analyst2.discrete,
         setup_analyst2.continuous,
         setup_analyst2.normalize_continuous)


def test_utils():
    assert len(Analyst.gen_binpp_path()) == 36
