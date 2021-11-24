from pathlib import Path
from json import load
from enum import Enum
from dataclasses import dataclass

class InstrInfoBuilder:
    def __init__(self, specfile: Path) -> None:
        self.specfile = specfile
        self.raw_spec = load(self.specfile.open("r"))