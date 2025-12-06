import math
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))
from utils.file_helpers import FileHandler, Parser


class MathParser(Parser):
    def parse(self, line: str) -> list[str]:
        line = line.strip()

        return [obj for obj in line.split(" ") if obj != ""]


def perform_math_operation(problem_line: list[str]) -> int:
    operation = problem_line.pop()
    int_problem_line = [int(x) for x in problem_line]
    match operation:
        case "+":
            return sum(int_problem_line)
        case "*":
            return math.prod(int_problem_line)
        case _:
            raise ValueError(f"Unknown operation: {operation}")


def day_6_pt_1() -> None:
    input = get_input(MathParser())
    input = list(zip(*input, strict=False))
    res = 0
    for problem_line in input:
        res += perform_math_operation(list(problem_line))
    print(res)


def get_input(parser: Parser):
    input_path = Path() / "day_6" / "input.txt"
    file = FileHandler(input_path, parser=parser).read_lines()
    return list(file)


if __name__ == "__main__":
    day_6_pt_1()
