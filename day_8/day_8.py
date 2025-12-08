import math
import sys
from collections import defaultdict
from collections.abc import Iterator
from dataclasses import dataclass
from itertools import product
from operator import attrgetter
from pathlib import Path
from typing import Any

sys.path.insert(0, str(Path(__file__).parent.parent))
from utils.file_helpers import FileHandler, Parser


@dataclass(frozen=True)
class Coords:
    x: int
    y: int
    z: int

    def __iter__(self) -> Iterator[int]:
        return iter((self.x, self.y, self.z))


@dataclass(frozen=True)
class Distance:
    distance: float
    point_1: Coords
    point_2: Coords


class Circuits:
    def __init__(self) -> None:
        self.circuits = defaultdict(list)

    def add_connection(self, junction_1: Coords, junction_2: Coords) -> None:
        self.circuits[junction_1].append(junction_2)
        self.circuits[junction_2].append(junction_1)

    def dfs(self) -> list[Any]:
        def helper(start: Coords, visited: set[Coords]) -> int:
            visited.add(start)
            count = 1
            for neighbor in self.circuits[start]:
                if neighbor not in visited:
                    count += helper(neighbor, visited)
            return count

        visited = set()
        counts = []
        for circuit in self.circuits:
            if circuit in visited:
                continue
            count = helper(circuit, visited)
            counts.append(count)
        return counts


class LineParser(Parser):
    def parse(self, line: str) -> Coords:
        x, y, z = line.strip().split(",")
        return Coords(int(x), int(y), int(z))


def calc_distances(input: list[Coords]) -> list[Distance]:
    distances = []
    seen = set()
    for p1, p2 in product(input, repeat=2):
        if (p1, p2) in seen or (p2, p1) in seen:
            continue
        seen.add((p1, p2))
        dist = math.dist(p1, p2)
        if p1 != p2:
            distances.append(Distance(dist, p1, p2))
    return distances


def day_8_pt_1() -> None:
    input: list[Coords] = get_input(LineParser())

    distances = calc_distances(input)
    circuits = Circuits()

    distances.sort(key=attrgetter("distance"), reverse=True)
    for _ in range(1000):
        closest_points = distances.pop()
        circuits.add_connection(
            junction_1=closest_points.point_1,
            junction_2=closest_points.point_2,
        )
    counts = circuits.dfs()
    print(
        f"Counts of junctions visited in each circuit: {sorted(counts, reverse=True)[:3]}",
    )
    print(f"Pt. 1 Result: {math.prod(sorted(counts, reverse=True)[:3])}")

    while not all(coord in circuits.circuits for coord in input):
        closest_points = distances.pop()
        circuits.add_connection(
            junction_1=closest_points.point_1,
            junction_2=closest_points.point_2,
        )

    print(f"Part 2 Result: {closest_points.point_1.x * closest_points.point_2.x}")


def get_input(parser: Parser) -> list[Any]:
    input_path = Path() / "day_8" / "input.txt"
    file = FileHandler(input_path, parser=parser).read_lines()
    return list(file)


if __name__ == "__main__":
    day_8_pt_1()
