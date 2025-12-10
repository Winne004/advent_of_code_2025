import sys
from dataclasses import dataclass
from itertools import combinations
from math import ceil
from pathlib import Path
from typing import Any

sys.path.insert(0, str(Path(__file__).parent.parent))
from utils.file_helpers import FileHandler, Parser


@dataclass(frozen=True)
class RedTile:
    x: int
    y: int


@dataclass
class Square:
    top_left: RedTile
    bottom_right: RedTile
    top_right: RedTile
    bottom_left: RedTile
    area: int


class LineParser(Parser):
    def parse(self, line: str) -> RedTile:
        x, y = line.strip().split(",")
        return RedTile(int(x), int(y))


def calc_max_area(input_tiles: list[RedTile]) -> int:
    max_area = 0
    for tile_1, tile_2 in combinations(input_tiles, 2):
        max_area = max(
            max_area,
            (abs(tile_1.x - tile_2.x) + 1) * (abs(tile_1.y - tile_2.y) + 1),
        )
    return max_area


def calc_square_coords(tile_1: RedTile, tile_2: RedTile) -> Square:
    top_left = RedTile(min(tile_1.x, tile_2.x), min(tile_1.y, tile_2.y))
    bottom_right = RedTile(max(tile_1.x, tile_2.x), max(tile_1.y, tile_2.y))
    top_right = RedTile(bottom_right.x, top_left.y)
    bottom_left = RedTile(top_left.x, bottom_right.y)
    return Square(
        top_left=top_left,
        bottom_right=bottom_right,
        top_right=top_right,
        bottom_left=bottom_left,
        area=(top_right.x - top_left.x + 1) * (bottom_left.y - top_left.y + 1),
    )


def generate_all_coords_in_square(square: Square) -> set[RedTile]:
    points: set[RedTile] = set()
    for x in range(square.top_left.x, square.top_right.x + 1):
        for y in range(square.top_left.y, square.bottom_right.y + 1):
            points.add(RedTile(x, y))
    return points


def build_index(loop: list[RedTile]) -> dict[RedTile, int]:
    return {tile: i for i, tile in enumerate(loop)}


def rectangle_bounds(r1: RedTile, r2: RedTile) -> tuple[int, int, int, int]:
    min_x = min(r1.x, r2.x)
    max_x = max(r1.x, r2.x)
    min_y = min(r1.y, r2.y)
    max_y = max(r1.y, r2.y)
    return min_x, max_x, min_y, max_y


def segment_crosses_interior(
    n1: RedTile,
    n2: RedTile,
    min_x: int,
    max_x: int,
    min_y: int,
    max_y: int,
) -> bool:
    if n1.x == n2.x:
        seg_x = n1.x
        if min_x < seg_x < max_x:
            y_start = min(n1.y, n2.y)
            y_end = max(n1.y, n2.y)
            for y in range(y_start, y_end + 1):
                if min_y < y < max_y:
                    return True

    elif n1.y == n2.y:
        seg_y = n1.y
        if min_y < seg_y < max_y:
            x_start = min(n1.x, n2.x)
            x_end = max(n1.x, n2.x)
            for x in range(x_start, x_end + 1):
                if min_x < x < max_x:
                    return True

    return False


def is_valid_rectangle(
    r1: RedTile,
    r2: RedTile,
    loop: list[RedTile],
    index: dict[RedTile, int],
) -> bool:
    start = index[r1]
    length = len(loop)

    min_x, max_x, min_y, max_y = rectangle_bounds(r1, r2)

    for d in range(ceil(length / 2)):
        for i in (start + d, start - d):
            n1 = loop[i % length]
            n2 = loop[(i + 1) % length]

            if segment_crosses_interior(n1, n2, min_x, max_x, min_y, max_y):
                return False

    return True


def get_input(parser: Parser) -> list[Any]:
    input_path = Path() / "day_9" / "input.txt"
    file = FileHandler(input_path, parser=parser).read_lines()
    return list(file)


def day_9_pt_1() -> None:
    red_tiles: list[RedTile] = get_input(LineParser())
    print("Red tiles:", red_tiles)

    max_area_part1 = calc_max_area(red_tiles)
    print(f"Pt. 1 Result (any tiles, just corner reds): {max_area_part1}\n")

    index = build_index(red_tiles)

    candidates: list[tuple[int, RedTile, RedTile]] = []
    for t1, t2 in combinations(red_tiles, 2):
        area = (abs(t1.x - t2.x) + 1) * (abs(t1.y - t2.y) + 1)
        candidates.append((area, t1, t2))

    candidates.sort(key=lambda x: x[0], reverse=True)

    best_area = 0
    best_square: Square | None = None

    for area, t1, t2 in candidates:
        if not is_valid_rectangle(t1, t2, red_tiles, index):
            continue

        best_area = area
        best_square = calc_square_coords(t1, t2)
        print(
            "Best valid rectangle found:",
            t1,
            t2,
            (abs(t1.x - t2.x) + 1),
            "*",
            (abs(t1.y - t2.y) + 1),
            "=",
            area,
        )
        break

    print(f"Pt. 2 Result (max area using only red/green tiles): {best_area}")
    if best_square:
        print(f"Best square: {best_square}")


if __name__ == "__main__":
    day_9_pt_1()
