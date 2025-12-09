import sys
from dataclasses import dataclass
from itertools import combinations
from pathlib import Path
from typing import Any

sys.path.insert(0, str(Path(__file__).parent.parent))
from utils.file_helpers import FileHandler, Parser


@dataclass(frozen=True)
class RedTile:
    x: int
    y: int


class LineParser(Parser):
    def parse(self, line: str) -> RedTile:
        x, y = line.strip().split(",")
        return RedTile(int(x), int(y))


def calc_max_area(input: list[RedTile]) -> int:
    max_area = 0
    for tile_1, tile_2 in combinations(input, 2):
        max_area = max(
            max_area,
            (abs(tile_1.x - tile_2.x) + 1) * (abs(tile_1.y - tile_2.y) + 1),
        )
    return max_area


def day_8_pt_1() -> None:
    input = get_input(LineParser())
    print(input)
    max_area = calc_max_area(input)

    print(f"Pt. 1 Result: {max_area}")


def get_input(parser: Parser) -> list[Any]:
    input_path = Path() / "day_9" / "input.txt"
    file = FileHandler(input_path, parser=parser).read_lines()
    return list(file)


if __name__ == "__main__":
    day_8_pt_1()
