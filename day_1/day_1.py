import sys
from dataclasses import dataclass
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))
from utils import FileHandler
from utils.file_helpers import Parser


@dataclass
class Rotation:
    direction: str
    amount: int


class DayOneInputParser(Parser):
    def parse(self, line: str) -> Rotation:
        line = line.strip()
        "".join(char for char in line if char.isalnum())
        return Rotation(line[0], int(line[1:].strip()))


class Safe:
    def __init__(self) -> None:
        self._dial_pos: int = 50
        self._dial_size: int = 100

    def rotate(self, rotation: Rotation) -> None:
        if rotation.direction == "L":
            self._dial_pos -= rotation.amount
        elif rotation.direction == "R":
            self._dial_pos += rotation.amount

        self._dial_pos %= self._dial_size

    @property
    def current_position(self) -> int:
        return self._dial_pos


def pt_1() -> None:
    res = 0
    input_path = Path() / "day_1" / "input.txt"
    print(input_path.absolute())
    input = FileHandler(input_path, parser=DayOneInputParser())
    safe = Safe()
    for line in input.read_lines():
        safe.rotate(line)
        print(safe.current_position)
        if safe.current_position == 0:
            res += 1

    print(f"Result: {res}")


if __name__ == "__main__":
    pt_1()
