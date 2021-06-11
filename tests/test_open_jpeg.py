from pathlib import Path


def test_open_jpeg(test_data_root: Path):
    filepath = test_data_root / "comics.jpg"
    assert filepath.exists()
