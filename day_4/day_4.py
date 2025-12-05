import sys
from collections.abc import Generator
from pathlib import Path
from typing import Any

sys.path.insert(0, str(Path(__file__).parent.parent))
from utils.file_helpers import FileHandler, Parser


class GridParser(Parser):
    def parse(self, line: str) -> list[str]:
        line = line.strip()
        return list(line)


class Grid:
    def __init__(self, lines: list[list[str]]) -> None:
        self.lines = lines

    def generate_adjacency_coords(
        self,
        row: int,
        col: int,
    ) -> Generator[tuple[int, int], Any]:
        for r in range(-1, 2):
            for c in range(-1, 2):
                if r == 0 and c == 0:
                    continue
                yield (row + r, col + c)

    def is_in_bounds(self, row: int, col: int) -> bool:
        return 0 <= row < len(self.lines) and 0 <= col < len(self.lines[0])

    def check_adjacent(self, row: int, col: int) -> int:
        adjacent_values = []
        for r, c in self.generate_adjacency_coords(row, col):
            if self.is_in_bounds(r, c):
                adjacent_values.append(self.lines[r][c])
        return adjacent_values.count("@")

    def iterate_grid(self) -> Generator[tuple[int, int], Any]:
        for r in range(len(self.lines)):
            for c in range(len(self.lines[0])):
                yield (r, c)


def day_4_pt_1() -> None:
    input_path = Path() / "day_4" / "input.txt"
    file = FileHandler(input_path, GridParser()).read_lines()
    lines = list(file)
    print(lines)
    grid = Grid(lines)
    res = 0
    previous_val = -1
    while previous_val != res:
        previous_val = res
        for r, c in grid.iterate_grid():
            if lines[r][c] == "@" and grid.check_adjacent(r, c) < 4:
                res += 1
                lines[r][c] = "."

    print(f"Pt 1 Result: {res}")


if __name__ == "__main__":
    day_4_pt_1()
