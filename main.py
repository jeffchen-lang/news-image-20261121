#!/usr/bin/env python3
"""Place the Saturday 21 November 2026 front page at the output path.

The finished infographic lives in this repository as entry.png: a dense
one-page newspaper summary of Saturday 21 November 2026, led by Bitcoin's
crash to a two-year low and followed by 39 further stories, with a stat
strip, a region bar, a world map with numbered pins and a date check. This
program only moves that image into the directory the grader names.

It needs nothing but the Python standard library, opens no network
connection, reads no clock and makes no random choices, so two runs write
identical bytes. It first confirms the file beside it really is a PNG by
its magic header, and writes nothing if the image is missing or damaged.
"""

import os
import sys

IMAGE_NAME = "entry.png"
PNG_MAGIC = b"\x89PNG\r\n\x1a\n"


def fail(message):
    """Write the problem to stderr and exit without producing output."""
    sys.stderr.write("news-image-20261121: " + message + "\n")
    raise SystemExit(1)


def read_entry_image():
    """Return the bytes of entry.png after checking its PNG header."""
    here = os.path.dirname(os.path.abspath(__file__))
    image_path = os.path.join(here, IMAGE_NAME)
    if not os.path.isfile(image_path):
        fail(IMAGE_NAME + " is not present next to main.py")
    with open(image_path, "rb") as source:
        data = source.read()
    if data[: len(PNG_MAGIC)] != PNG_MAGIC:
        fail(IMAGE_NAME + " does not start with the PNG magic header")
    if len(data) == 0:
        fail(IMAGE_NAME + " is empty")
    return data


def main():
    """Copy the checked image to $MAKEFUN_OUTPUT_DIR/entry.png."""
    output_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "")
    if not output_dir:
        fail("MAKEFUN_OUTPUT_DIR is not set")
    image = read_entry_image()
    os.makedirs(output_dir, exist_ok=True)
    destination = os.path.join(output_dir, IMAGE_NAME)
    with open(destination, "wb") as target:
        target.write(image)


if __name__ == "__main__":
    main()
