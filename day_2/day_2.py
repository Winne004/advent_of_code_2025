import sys
from collections.abc import Generator
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))
from utils import FileHandler


def yeild_numbers(id: str) -> Generator[int]:
    start, end = id.split("-")
    yield from range(int(start), int(end) + 1)


def is_repeated_twice(id_: int) -> bool:
    str_id = str(id_)
    l, r = str_id[: len(str_id) // 2], str_id[len(str_id) // 2 :]
    return l == r


def day_2() -> None:
    res = 0
    input_path = Path() / "day_2" / "input.txt"
    file = FileHandler(input_path).read_lines()
    line = next(file)
    ids = line.strip().split(",")
    for id_ in ids:
        for number in yeild_numbers(id_):
            if is_repeated_twice(number):
                print(f"Found repeated twice number: {number}")
                res += number
    print(f"Result: {res}")


if __name__ == "__main__":
    day_2()
