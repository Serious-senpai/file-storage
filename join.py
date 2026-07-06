from __future__ import annotations

import argparse
import re
from pathlib import Path
from typing import Dict, TYPE_CHECKING


class Namespace(argparse.Namespace):
    if TYPE_CHECKING:
        target: Path
        output: Path


parser = argparse.ArgumentParser(formatter_class=argparse.ArgumentDefaultsHelpFormatter)
parser.add_argument("target", type=Path, help="Path to the directory containing files to join")
parser.add_argument("-o", "--output", type=Path, default=Path.cwd(), help="Original file name")
namespace = parser.parse_args(namespace=Namespace())

pattern = re.compile(r"^" + re.escape(namespace.output.name) + r"\.(\d+)$", flags=re.IGNORECASE)
entries: Dict[int, Path] = {}

for entry in namespace.target.iterdir():
    if entry.is_file():
        match = pattern.fullmatch(entry.name)
        if match is not None:
            index = int(match.group(1))
            entries[index] = entry

with namespace.output.open("wb") as f_output:
    for index in sorted(entries.keys()):
        with entries[index].open("rb") as f_chunk:
            f_output.write(f_chunk.read())
