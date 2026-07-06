from __future__ import annotations

import argparse
from pathlib import Path
from typing import TYPE_CHECKING


class Namespace(argparse.Namespace):
    if TYPE_CHECKING:
        target: Path
        output: Path
        chunk: int


parser = argparse.ArgumentParser(formatter_class=argparse.ArgumentDefaultsHelpFormatter)
parser.add_argument("target", type=Path, help="Path to the target file to split")
parser.add_argument("-o", "--output", type=Path, default=Path.cwd(), help="Output directory")
parser.add_argument("-c", "--chunk", type=int, default=50, help="Size of each chunk in MB")
namespace = parser.parse_args(namespace=Namespace())

namespace.output.mkdir(parents=True, exist_ok=True)
with namespace.target.open("rb") as f_target:
    chunk_size = namespace.chunk * 1024 * 1024
    chunk_index = 0
    while True:
        chunk = f_target.read(chunk_size)
        if not chunk:
            break

        chunk_file = namespace.output / f"{namespace.target.name}.{chunk_index}"
        with chunk_file.open("wb") as f_chunk:
            f_chunk.write(chunk)

        chunk_index += 1
