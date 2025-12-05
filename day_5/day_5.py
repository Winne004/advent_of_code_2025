import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Any

sys.path.insert(0, str(Path(__file__).parent.parent))
from utils.file_helpers import FileHandler, Parser


class IngredientParser(Parser):
    def parse(self, line: str) -> dict[str, Any] | None:
        line = line.strip()
        if "-" in line:
            range = line.split("-")
            return {"range": (int(range[0]), int(range[1]))}
        return {"ingredients": line} if line else {}


@dataclass
class FreshIngredientIDRange:
    start: int
    end: int

    def __hash__(self) -> int:
        return hash((self.start, self.end))


def within_range(value: int, range_tuple: tuple[int, int]) -> bool:
    return range_tuple[0] <= value <= range_tuple[1]


def generate_contiguous_ranges(
    id_range: FreshIngredientIDRange,
    ranges: list[FreshIngredientIDRange],
) -> FreshIngredientIDRange:
    # Ugly and inefficient but works
    # Sorting would help but not implemented
    for range_ in ranges:
        if within_range(
            id_range.start,
            (range_.start - 1, range_.end + 1),
        ) or within_range(id_range.end, (range_.start - 1, range_.end + 1)):
            id_range.end = max(id_range.end, range_.end)
            id_range.start = min(id_range.start, range_.start)
    return id_range


def day_5_pt_1():
    res = 0
    input_path = Path() / "day_5" / "input.txt"
    file = FileHandler(input_path, IngredientParser()).read_lines()
    lines = list(file)
    print(lines)
    ranges = [FreshIngredientIDRange(*r["range"]) for r in lines if "range" in r]
    ingredients = [i["ingredients"] for i in lines if "ingredients" in i]
    print(ranges, ingredients)
    for ingredient in ingredients:
        if any(
            within_range(int(ingredient), (range_.start, range_.end))
            for range_ in ranges
        ):
            print(f"Ingredient {ingredient} is fresh")
            res += 1
        else:
            print(f"Ingredient {ingredient} is stale")
    print(f"Pt 1 Result: {res}")

    # Pt. 2
    previous_ranges = None
    while previous_ranges != ranges:
        previous_ranges = [FreshIngredientIDRange(r.start, r.end) for r in ranges]
        for i, range_ in enumerate(ranges):
            ranges[i] = generate_contiguous_ranges(range_, ranges)

    unique_ranges = set(ranges)
    total_coverage = sum(r.end - r.start + 1 for r in unique_ranges)

    print(f"Pt 2 Result - ingredient IDs considered fresh: {total_coverage}")


if __name__ == "__main__":
    day_5_pt_1()
