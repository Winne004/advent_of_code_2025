import math
import sys
from enum import StrEnum
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))
from utils.file_helpers import FileHandler, Parser


class MathParser(Parser):
    def parse(self, line: str) -> list[str]:
        line = line.strip()

        return [obj for obj in line.split(" ") if obj != ""]


class MathParserPt2(Parser):
    def parse(self, line: str) -> str:
        return line


class Operators(StrEnum):
    ADD = "+"
    MULTIPLY = "*"


def perform_math_operation(problem_line: list[str]) -> int:
    operation = problem_line.pop()
    int_problem_line = [int(x) for x in problem_line]
    match operation:
        case Operators.ADD:
            return sum(int_problem_line)
        case Operators.MULTIPLY:
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


def day_6_pt_2() -> None:
    res = 0
    raw_input = get_input(MathParserPt2())
    columns = list(zip(*raw_input, strict=False))
    numbers = [col[:-1] for col in columns]
    operators = [
        col[-1]
        for col in columns
        if col[-1] == Operators.ADD or col[-1] == Operators.MULTIPLY
    ]
    parser_input = []
    tmp = []
    for col in numbers:
        col = "".join(col).strip()
        if not col:
            parser_input.append(tmp)
            tmp = []
        else:
            tmp.append(col)
    parser_input.append(tmp)
    print(parser_input)
    print(operators)
    resulitng = zip(parser_input, operators, strict=True)
    for problem_line, operator in resulitng:
        res += perform_math_operation([*problem_line, operator])
    print(res)


def get_input(parser: Parser):
    input_path = Path() / "day_6" / "input.txt"
    file = FileHandler(input_path, parser=parser).read_lines()
    return list(file)


if __name__ == "__main__":
    day_6_pt_1()
    day_6_pt_2()
