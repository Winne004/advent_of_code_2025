import sys
from dataclasses import dataclass, field
from functools import cache
from pathlib import Path
from typing import Any

sys.path.insert(0, str(Path(__file__).parent.parent))
from utils.file_helpers import FileHandler, Parser


@dataclass
class Node:
    value: str
    outputs: list[str]

    def __hash__(self) -> int:
        return hash(self.value)


@dataclass
class Nodes:
    nodes: dict[str, Node] = field(default_factory=dict)

    def add_node(self, node: Node) -> None:
        if node.value not in self.nodes:
            self.nodes[node.value] = node

    def dfs(self, start: Node, target: str = "out") -> int:
        @cache
        def helper(node: Node, path: str) -> int:
            tmp = 0
            if node.value == target:
                return 1

            for neighbor in node.outputs:
                tmp += helper(self.nodes[neighbor], path)
            return tmp

        return helper(start, "")

    def dfs_pt2(self, start: Node, target: str = "out") -> int:
        @cache
        def helper(
            node: Node,
            path: str,
            fft: bool = False,
            dac: bool = False,
        ) -> int:
            tmp = 0

            if node.value == "fft":
                fft = True

            if node.value == "dac":
                dac = True

            if node.value == target and fft and dac:
                return 1

            for neighbor in node.outputs:
                tmp += helper(self.nodes[neighbor], path, fft, dac)
            return tmp

        return helper(start, "")


class LineParser(Parser):
    def parse(self, line: str) -> Node:
        parts = line.split(":")
        node_value = parts[0].strip()
        instructions = parts[1].split(" ")
        return Node(
            value=node_value,
            outputs=[instr.strip() for instr in instructions if instr],
        )


def get_input(parser: Parser) -> list[Any]:
    input_path = Path() / "day_11" / "input.txt"
    file = FileHandler(input_path, parser=parser).read_lines()
    return list(file)


def day_11_pt_1() -> None:
    nodes = get_input(LineParser())
    node_map = Nodes()
    for node in nodes:
        node_map.add_node(node)
    node_map.add_node(Node(value="out", outputs=[]))

    node_map.dfs(node_map.nodes["you"])

    print(
        f"Total unique paths from 'you' to 'out': {node_map.dfs(node_map.nodes['you'])}",
    )

    print(
        f"Total unique paths from 'svr' to 'out': {node_map.dfs_pt2(node_map.nodes['svr'])}",
    )


if __name__ == "__main__":
    day_11_pt_1()
