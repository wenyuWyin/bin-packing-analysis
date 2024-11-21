from macpacking.reader import DatasetReader, BinppReader, OracleReader
import pytest


def test_binpp_reader():
    dataset = '_datasets/binpp/N1C1W1/N1C1W1_B.BPP.txt'
    capacity = 100
    oracle = [
        8, 8, 12, 13, 13, 14, 15, 17, 18, 19, 20, 23, 30, 37, 37, 39, 40,
        43, 43, 44, 44, 50, 51, 61, 61, 62, 62, 63, 66, 67, 69, 70, 71,
        72, 75, 76, 76, 79, 83, 83, 88, 92, 92, 93, 93, 97, 97, 97, 99, 100
    ]
    reader: DatasetReader = BinppReader(dataset)
    assert capacity == reader.offline()[0]
    assert oracle == sorted(reader.offline()[1])


# pytest fixture that obtains optimal solutions
@pytest.fixture
def create_reader(dataset: str) -> dict[str: int]:
    reader: OracleReader = OracleReader(dataset)
    return reader.read_file()


# binpp
@pytest.mark.parametrize('dataset', ['binpp'])
def test_binpp_oracle(create_reader):
    optimal = {'N1C1W1_B': 31, 'N1C1W1_C': 20, 'N1C1W1_D': 28}
    for key, value in create_reader.items():
        if key in optimal.keys():
            assert value == optimal[key]


# binpp-hard
@pytest.mark.parametrize('dataset', ['binpp-hard'])
def test_hard_oracle(create_reader):
    optimal = {'HARD0': 56, 'HARD5': 56, 'HARD9': 56}
    for key, value in create_reader.items():
        if key in optimal.keys():
            assert value == optimal[key]


# jburkardt
@pytest.mark.parametrize('dataset', ['jburkardt'])
def test_jburkardt_oracle(create_reader):
    optimal = {'p_01': 4, 'p_02': 7, 'p_04': 7}
    for key, value in create_reader.items():
        if key in optimal.keys():
            assert value == optimal[key]
