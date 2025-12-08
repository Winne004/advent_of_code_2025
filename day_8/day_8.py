import math
import sys
from collections import defaultdict
from collections.abc import Iterator
from dataclasses import dataclass
from itertools import product
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


class Circuits:
    def __init__(self) -> None:
        self.circuits = defaultdict(list)

    def add_connection(self, junction_1: Coords, junction_2: Coords) -> None:
        self.circuits[junction_1].append(junction_2)
        self.circuits[junction_2].append(junction_1)

    def dfs(self):
        def helper(start: Coords, visited: set[Coords]) -> int:
            visited.add(start)
            count = 1
            for neighbor in self.circuits[start]:
                if neighbor not in visited:
                    count += helper(neighbor, visited)
            return count

        visited = set()
        for circuit in self.circuits:
            if circuit in visited:
                continue
            count = helper(circuit, visited)
            print(f"Circuit starting at {circuit} visits: {count} junctions")


class LineParser(Parser):
    def parse(self, line: str) -> Coords:
        x, y, z = line.strip().split(",")
        return Coords(int(x), int(y), int(z))


def day_8_pt_1() -> None:
    input: list[Coords] = get_input(LineParser())
    print(f"Pt. 1 Result: {input}")
    dist = math.dist(input[0], input[1])
    print(f"Distance between points: {dist}")
    distances = []
    seen = set()
    for p1, p2 in product(input, repeat=2):
        if (p1, p2) in seen or (p2, p1) in seen:
            continue
        seen.add((p1, p2))
        dist = math.dist(p1, p2)
        if p1 != p2:
            distances.append((dist, (p1, p2)))

    circuits = Circuits()

    distances.sort(key=lambda x: x[0], reverse=True)
    for x in range(10):
        closest_points = distances.pop()
        print(
            f" {x} Closest points are {closest_points[1]} with a distance of {closest_points[0]}",
        )
        circuits.add_connection(
            junction_1=closest_points[1][0],
            junction_2=closest_points[1][1],
        )
    print(f"Circuits: {circuits.circuits}")
    print("DFS Traversal of Circuits:")
    circuits.dfs()


def get_input(parser: Parser) -> list[Any]:
    input_path = Path() / "day_8" / "input.txt"
    file = FileHandler(input_path, parser=parser).read_lines()
    return list(file)


if __name__ == "__main__":
    day_8_pt_1()
