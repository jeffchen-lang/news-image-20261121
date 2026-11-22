"""Hand the bundled front-page image to the harness, unchanged.

The entry image ships in this repository as ``entry.png``. This program
streams those exact bytes to ``$MAKEFUN_OUTPUT_DIR/entry.png`` and checks
on the way that the file really is a PNG: the first eight bytes must be
the PNG signature. It takes no network, no clock and no randomness, so
two runs always produce byte-identical output.
"""

import hashlib
import os
import shutil
import sys

SIGNATURE = b"\x89PNG\r\n\x1a\n"
CHUNK = 65536
MAX_BYTES = 1048576  # competition cap: the entry image must fit in 1 MiB
TARGET = "entry.png"


def paths():
    here = os.path.dirname(os.path.abspath(__file__))
    src = os.path.join(here, "entry.png")
    outdir = os.environ.get("MAKEFUN_OUTPUT_DIR")
    if not outdir:
        sys.exit("MAKEFUN_OUTPUT_DIR is not set; nowhere to write the image")
    return src, os.path.join(outdir, TARGET)


def stream_copy(src, dst):
    """Copy *src* to *dst* in chunks, returning (bytes, sha256 hex)."""
    digest = hashlib.sha256()
    total = 0
    with open(src, "rb") as fin, open(dst, "wb") as fout:
        head = fin.read(len(SIGNATURE))
        if head != SIGNATURE:
            sys.exit("bundled image is not a PNG (bad signature)")
        digest.update(head)
        fout.write(head)
        total += len(head)
        while True:
            block = fin.read(CHUNK)
            if not block:
                break
            total += len(block)
            if total > MAX_BYTES:
                sys.exit("bundled image exceeds 1 MiB (%d bytes)" % total)
            digest.update(block)
            fout.write(block)
    return total, digest.hexdigest()


def verify(dst, expect_digest, expect_total):
    """Re-read *dst* and confirm it matches what was streamed."""
    digest = hashlib.sha256()
    total = 0
    with open(dst, "rb") as fin:
        while True:
            block = fin.read(CHUNK)
            if not block:
                break
            digest.update(block)
            total += len(block)
    if total != expect_total or digest.hexdigest() != expect_digest:
        sys.exit("written image does not match the bundled image")


def main():
    src, dst = paths()
    if not os.path.isfile(src):
        sys.exit("bundled image missing: " + src)
    os.makedirs(os.path.dirname(dst), exist_ok=True)
    total, digest = stream_copy(src, dst)
    verify(dst, digest, total)
    print("wrote %d bytes to %s (sha256 %s)" % (total, dst, digest))


if __name__ == "__main__":
    main()
