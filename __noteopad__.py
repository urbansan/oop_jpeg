from pathlib import Path
from oop_jpeg import Jpeg

bale_jpg = Path(__file__).parent / "tests" / "data" / "bale.jpg"

Jpeg(bale_jpg)


