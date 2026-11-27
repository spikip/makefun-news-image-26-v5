#!/usr/bin/env python3
"""Hand the v5 digest image to the grader for news-image-20261126.

render.py (next to this file) draws the whole page and saves it as
entry.png. This entrypoint only delivers that file: it reads the bytes,
checks them against the contest limits (a whole PNG, at most 1 MiB and
1024 by 1024), and copies them byte for byte into the output directory
the harness provides through $MAKEFUN_OUTPUT_DIR (default /output). It
then reads the delivered copy back and confirms it matches, so a short
or truncated write fails loudly instead of reaching the judge.

Standard library only. No network, no clock, no randomness — the same
bytes go out on every run, so two runs write identical files.
"""
import hashlib
import os
import struct
import sys

MAX_BYTES = 1_048_576
MAX_SIDE = 1024
PNG_MAGIC = b"\x89PNG\r\n\x1a\n"
PNG_TAIL = b"IEND\xaeB`\x82"


def load_checked(path):
    with open(path, "rb") as fh:
        data = fh.read()
    if len(data) > MAX_BYTES:
        raise ValueError("entry.png is %d bytes, over the 1 MiB limit"
                         % len(data))
    if not data.startswith(PNG_MAGIC):
        raise ValueError("entry.png is not a PNG file")
    if not data.endswith(PNG_TAIL):
        raise ValueError("entry.png is truncated: no IEND chunk at the end")
    ihdr_len, ihdr_type = struct.unpack(">I4s", data[8:16])
    if ihdr_len != 13 or ihdr_type != b"IHDR":
        raise ValueError("entry.png has a broken IHDR chunk")
    width, height = struct.unpack(">II", data[16:24])
    if width > MAX_SIDE or height > MAX_SIDE:
        raise ValueError("entry.png is %dx%d, over the 1024x1024 limit"
                         % (width, height))
    if data[25] not in (0, 2, 3, 4, 6):
        raise ValueError("entry.png has unknown PNG colour type %d"
                         % data[25])
    if b"IDAT" not in data:
        raise ValueError("entry.png has no image data (no IDAT chunk)")
    return data


def main():
    here = os.path.dirname(os.path.abspath(__file__))
    data = load_checked(os.path.join(here, "entry.png"))
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    os.makedirs(out_dir, exist_ok=True)
    target = os.path.join(out_dir, "entry.png")
    with open(target, "wb") as fh:
        fh.write(data)
    with open(target, "rb") as fh:
        landed = fh.read()
    if hashlib.sha256(landed).hexdigest() != hashlib.sha256(data).hexdigest():
        raise ValueError("the delivered copy does not match entry.png")
    width, height = struct.unpack(">II", data[16:24])
    print("entry.png delivered: %dx%d, %d bytes (sha256 %s...) -> %s"
          % (width, height, len(data),
             hashlib.sha256(data).hexdigest()[:12], target))
    return 0


if __name__ == "__main__":
    sys.exit(main())
