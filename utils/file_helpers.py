from collections.abc import Generator
from pathlib import Path
from typing import IO, Any, Protocol


class Parser(Protocol):
    def parse(self, line: str) -> Any: ...


class FileHandler:
    def __init__(self, base_path: Path, parser: Parser | None = None) -> None:
        self.base_path = Path(base_path)
        self._file = self.open_file(self.base_path)
        self.parser = parser

    def open_file(self, filepath: Path, mode="r") -> IO[Any]:
        return Path.open(filepath, mode)

    def read_lines(self) -> Generator[Any]:
        lines = self._file.readlines()
        for line in lines:
            yield self.parser.parse(line) if self.parser else line
