import sys
from itertools import combinations
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))
from utils.file_helpers import FileHandler, Parser


class StripParser(Parser):
    def parse(self, line: str) -> list[str]:
        line = line.strip()
        return list(line)


def day_3() -> None:
    res = 0
    input_path = Path() / "day_3" / "input.txt"
    file = FileHandler(input_path, StripParser()).read_lines()
    for line in file:
        "".join(line)
        max_val = 0
        for prod in combinations(line, 2):
            max_val = max(max_val, int("".join(prod)))
        res += max_val
    print(f"Result: {res}")


if __name__ == "__main__":
    day_3()
