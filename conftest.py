import pytest
from pathlib import Path


@pytest.fixture(scope="session")
def test_data_root():
    return Path(__file__).parent / "tests" / "data"
