import sys
from pathlib import Path
from typing import Any

sys.path.insert(0, str(Path(__file__).parent.parent))
from utils.file_helpers import FileHandler, Parser


class LineParser(Parser):
    def parse(self, line: str) -> list[str]:
        return list(line.strip())


class Constants:
    START = "S"
    SPLITTER = "^"


class Grid:
    def __init__(self, data: list[list[str]]) -> None:
        self.data = data
        self.seen = set()
        self.splits = 0

    def in_bounds(self, row: int, col: int) -> bool:
        return 0 <= row < len(self.data) and 0 <= col < len(self.data[0])

    def find_start(self) -> tuple[int, int]:
        for r in range(len(self.data)):
            for c in range(len(self.data[0])):
                if self.data[r][c] == Constants.START:
                    return (r, c)
        raise ValueError("Start position not found")

    def recurse(self, row: int, col: int) -> int:
        if not self.in_bounds(row, col):
            return 0
        if (row, col) in self.seen:
            return 0
        self.seen.add((row, col))
        if self.data[row][col] == Constants.SPLITTER:
            self.splits += 1
            return self.recurse(row, col - 1) + self.recurse(row, col + 1)
        return self.recurse(row + 1, col) + 1


def day_7_pt_1() -> None:
    input = get_input(LineParser())
    grid = Grid(input)
    start_row, start_col = grid.find_start()
    grid.recurse(start_row, start_col)
    print(f"The tachyon beam is split a total of: {grid.splits} times")


def get_input(parser: Parser) -> list[Any]:
    input_path = Path() / "day_7" / "input.txt"
    file = FileHandler(input_path, parser=parser).read_lines()
    return list(file)


if __name__ == "__main__":
    day_7_pt_1()
