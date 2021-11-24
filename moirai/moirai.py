from pathlib import Path
from enum import Enum
from typing import List
from dataclasses import dataclass
from string import ascii_letters
from json import dump

import docutils.nodes
import docutils.parsers.rst
import docutils.utils
import docutils.frontend

from ptpython.repl import embed

LLVM_PLATFORMS = [
    "AArch64",
    "AMDGPU",
    "ARC",
    "ARM",
    "AVR",
    "BPF",
    "CSKY",
    "Hexagon",
    "Lanai",
    "M68k",
    "Mips",
    "MSP430",
    "NVPTX",
    "PowerPC",
    "RISCV",
    "Sparc",
    "SystemZ",
    "VE",
    "WebAssembly",
    "X86",
    "XCore"
]

class SectionInfo:
    def __init__(self) -> None:
        self.title: str = ""
        self.asm_string: str = ""
        self.defs: List[str] = []
        self.uses: List[str] = []
        self.predicates: List[str] = []
        self.constraints: List[str] = []

class DockerfileGenerator:
    @classmethod
    def generate(cls, platforms: List[str], ) -> str:
        """
        Generate a Dockerfile for the given platforms.

        :param platforms: List of platforms to generate Dockerfiles for.
        :return: Dockerfile contents.
        """
        template = Path(__file__).with_name("res") / "Dockerfile.template"
        with template.open() as f:
            contents = f.read()

        template_lines = [
            "RUN mkdir /output"
        ]
        for platform in platforms:
            template_lines.append(
                f"RUN llvm-tblgen-13 --gen-instr-docs /llvm-project/llvm/lib/Target/{platform}/{platform}.td "
                f"-I=/llvm-project/llvm/include > /output/{platform}.rst -I/llvm-project/llvm/lib/Target/{platform}"
            )

        return contents.format(
            template="\n".join(template_lines)
        )

class DocParser:
    """Parse an RST document output by `llvm-tblgen` and output a JSON document"""

    def __init__(self, path: Path) -> None:
        self.path = path
        self.instructions = []

    def parse(self) -> None:
        for docfile in self.path.iterdir():
            if not docfile.is_file() or docfile.suffix != ".rst":
                continue

            with docfile.open("r") as f:
                doc = self.parse_doc(f.read())
                with docfile.with_name(docfile.with_suffix(".json").name).open("w") as f:
                    self.interpret_doc(doc)
                    dump(self.instructions, f, sort_keys=True, indent=4)

    def parse_doc(self, contents: str) -> docutils.nodes.document:
        parser = docutils.parsers.rst.Parser()
        components = (docutils.parsers.rst.Parser,)
        settings = docutils.frontend.OptionParser(components=components).get_default_values()
        document = docutils.utils.new_document("<rst-doc>", settings=settings)
        parser.parse(contents, document)
        return document

    def interpret_doc(self, doc: docutils.nodes.document) -> str:

        class SectionVisitor(docutils.nodes.GenericNodeVisitor):
            def __init__(self, document: docutils.nodes.document, parser: "DocParser") -> None:
                super().__init__(document)
                self.document = document
                self.parser = parser

            def visit_section(self, node: docutils.nodes.section) -> None:
                if "arm-instructions" in node.attributes.get("ids"):
                    return

                parts = {}
                for child in node.children:
                    if child.tagname == "title":
                        parts["title"] = child.astext()
                    elif child.tagname == "paragraph":
                        name = "".join(filter(lambda l: l in ascii_letters, child.children[0].astext())).lower().strip()
                        parts[name] = list(filter(lambda t: t != ", ", map(lambda n: n.astext(), child.children[1:])))

                    elif child.tagname == "bullet_list":
                        items = list(map(lambda n: (n[0].astext(), n[1].astext()), map(lambda n: n.children, child.children[0]))) 
                        for item in items:
                            if item[0] not in parts:
                                parts[item[0].lower().strip()] = []
                            parts[item[0].lower().strip()].append(item[1])
                if len(parts.keys()) > 1:
                    self.parser.instructions.append(parts)

            def default_visit(self, _: docutils.nodes.Node) -> None:
                pass

        doc.walk(SectionVisitor(doc, self))
        





