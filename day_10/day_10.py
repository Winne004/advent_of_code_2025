import sys
from collections import deque
from dataclasses import dataclass
from enum import StrEnum
from pathlib import Path
from typing import Any

sys.path.insert(0, str(Path(__file__).parent.parent))
from utils.file_helpers import FileHandler, Parser


@dataclass(frozen=True)
class Button:
    button: tuple[int, ...]


@dataclass(frozen=True)
class IndicatorLight:
    diagram: list[str]
    wiring_schematic: list[Button]
    Joltage: None | int = None


class LineParser(Parser):
    def parse(self, line: str) -> IndicatorLight:
        input_ = line.strip().split(" ")
        diagram = [char for char in input_[0] if char in ("#", ".")]
        buttons = [
            Button(tuple(int(char) for char in coord if char.isdigit()))
            for coord in input_
            if coord[0] == "("
        ]
        return IndicatorLight(diagram=diagram, wiring_schematic=buttons)


class Constants(StrEnum):
    LIGHT_ON = "#"
    LIGHT_OFF = "."


def apply_wiring_schematic(
    light: list[str],
    button: Button,
) -> list[str]:
    toggle = {
        Constants.LIGHT_ON.value: Constants.LIGHT_OFF.value,
        Constants.LIGHT_OFF.value: Constants.LIGHT_ON.value,
    }

    for pos in button.button:
        light[pos] = toggle[light[pos]]
    return light


def bfs_toggle_lights(light: list[str], indicator_light: IndicatorLight) -> int:
    start_tuple = tuple(light)
    queue = deque([(light, 0)])
    visited = {start_tuple}

    if light == indicator_light.diagram:
        return 0

    while queue:
        current_light, current_depth = queue.popleft()

        for button in indicator_light.wiring_schematic:
            new_light = apply_wiring_schematic(current_light.copy(), button)
            light_tuple = tuple(new_light)

            if new_light == indicator_light.diagram:
                return current_depth + 1

            if light_tuple not in visited:
                visited.add(light_tuple)
                queue.append((new_light, current_depth + 1))

    raise ValueError("No solution found to toggle lights.")


def get_input(parser: Parser) -> list[Any]:
    input_path = Path() / "day_10" / "input.txt"
    file = FileHandler(input_path, parser=parser).read_lines()
    return list(file)


def day_10_pt_1() -> None:
    indicator_lights: list[IndicatorLight] = get_input(LineParser())
    print("Indicator Lights:", indicator_lights)
    res = 0
    for indicator_light in indicator_lights:
        res += bfs_toggle_lights(
            [Constants.LIGHT_OFF.value] * len(indicator_light.diagram),
            indicator_light,
        )
    print("Result:", res)


if __name__ == "__main__":
    day_10_pt_1()
