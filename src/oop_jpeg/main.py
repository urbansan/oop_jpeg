

from enum import Enum

class Mood(Enum):
    cos = 1
    dwa = 2


print(getattr(Mood, Mood.cos.name).value)