import sys
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


def within_range(value: int, range_tuple: tuple[int, int]) -> bool:
    return range_tuple[0] <= value <= range_tuple[1]


def day_5_pt_1():
    res = 0
    input_path = Path() / "day_5" / "input.txt"
    file = FileHandler(input_path, IngredientParser()).read_lines()
    lines = list(file)
    print(lines)
    ranges = [r["range"] for r in lines if "range" in r]
    ingredients = [i["ingredients"] for i in lines if "ingredients" in i]
    print(ranges, ingredients)
    for ingredient in ingredients:
        if any(within_range(int(ingredient), range_) for range_ in ranges):
            print(f"Ingredient {ingredient} is fresh")
            res += 1
        else:
            print(f"Ingredient {ingredient} is stale")
    print(f"Pt 1 Result: {res}")


if __name__ == "__main__":
    day_5_pt_1()
