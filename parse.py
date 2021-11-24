from pathlib import Path
from dataclasses import dataclass
from typing import List

docs = ["ARM.doc", "Mips.doc"]


@dataclass
class InstrInfoText:
    asm: str
    flags: List[str]


for doc in docs:
    docpath = Path(__file__).with_name(doc)
    with docpath.open("r") as f:
        doc_contents = f.read()
