"""Copy the bundled front-page image to the harness output directory.

The entry image lives in this repository as ``entry.png``. This program
does nothing but hand that exact file to the harness: it reads the bytes,
checks they really are a PNG, and writes them unchanged to
``$MAKEFUN_OUTPUT_DIR/entry.png``.

No network, no clock, no randomness -- the output bytes are always
identical to the bundled image.
"""

import os
from pathlib import Path

PNG_MAGIC = b"\x89PNG\r\n\x1a\n"
MAX_BYTES = 1_048_576  # competition cap: the entry image must fit in 1 MiB
DEST_NAME = "entry.png"


def bundled_image() -> Path:
    """Path of the image shipped in this repository."""
    return Path(__file__).resolve().parent / "entry.png"


def output_dir() -> Path:
    """Output directory named by the harness environment."""
    raw = os.environ.get("MAKEFUN_OUTPUT_DIR")
    if not raw:
        raise SystemExit("MAKEFUN_OUTPUT_DIR is not set; nothing to write to")
    return Path(raw)


def checked_bytes(path: Path) -> bytes:
    """Read *path* and confirm it holds a real, non-empty PNG."""
    if not path.is_file():
        raise SystemExit(f"bundled image missing: {path}")
    data = path.read_bytes()
    if not data:
        raise SystemExit(f"bundled image is empty: {path}")
    if len(data) > MAX_BYTES:
        raise SystemExit(f"bundled image exceeds 1 MiB ({len(data)} bytes): {path}")
    if data[: len(PNG_MAGIC)] != PNG_MAGIC:
        raise SystemExit(f"bundled image is not a PNG: {path}")
    return data


def place(data: bytes, directory: Path) -> Path:
    """Write *data* to ``entry.png`` inside *directory*."""
    directory.mkdir(parents=True, exist_ok=True)
    target = directory / DEST_NAME
    target.write_bytes(data)
    return target


def main() -> None:
    data = checked_bytes(bundled_image())
    target = place(data, output_dir())
    print(f"wrote {len(data)} bytes to {target}")


if __name__ == "__main__":
    main()
