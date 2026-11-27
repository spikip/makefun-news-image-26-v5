"""Deliver the finished v5 digest picture to the grading sandbox.

The picture itself lives next to this file as entry.png — it was drawn
by render.py in this same repository. This little program does not draw
anything: it only hands the finished file over. It reads the bytes,
walks the PNG chunk by chunk to make sure the file is whole (a real
header, real image data, a proper closing chunk), checks the contest
limits on size and dimensions, and then copies the bytes unchanged into
the folder the harness points at with MAKEFUN_OUTPUT_DIR.

Everything here uses the standard library. Nothing is fetched from the
network, the clock is never read, and no random numbers appear anywhere,
so every run hands over exactly the same bytes.
"""
import hashlib, os, struct, sys

LIMIT_BYTES = 1048576
LIMIT_SIDE = 1024
MAGIC = b"\x89PNG\r\n\x1a\n"
CHUNK_HEAD = 12


def _check_png(blob):
    """Walk the chunks of blob; return (width, height) or raise."""
    if len(blob) > LIMIT_BYTES:
        raise ValueError("picture is %d bytes, past the 1 MiB cap"
                         % len(blob))
    if blob[:8] != MAGIC:
        raise ValueError("picture does not start with the PNG signature")
    if blob[25] not in (0, 2, 3, 4, 6):
        raise ValueError("picture has colour type %d, which PNG forbids"
                         % blob[25])
    pos = 8
    seen_data = False
    seen_end = False
    size = (0, 0)
    while pos + 8 <= len(blob):
        length, kind = struct.unpack(">I4s", blob[pos:pos + 8])
        if pos + CHUNK_HEAD + length > len(blob):
            raise ValueError("picture ends in the middle of a chunk")
        if kind == b"IHDR":
            if length != 13:
                raise ValueError("picture has a malformed IHDR chunk")
            size = struct.unpack(">II", blob[pos + 8:pos + 16])
            if size[0] > LIMIT_SIDE or size[1] > LIMIT_SIDE:
                raise ValueError("picture is %dx%d, past the 1024x1024 cap"
                                 % size)
        elif kind == b"IDAT":
            seen_data = True
        elif kind == b"IEND":
            seen_end = True
        pos += CHUNK_HEAD + length
    if size == (0, 0):
        raise ValueError("picture has no IHDR chunk")
    if not seen_data:
        raise ValueError("picture carries no image data (no IDAT chunk)")
    if not seen_end:
        raise ValueError("picture is cut off: no IEND chunk at the end")
    return size


def _deliver():
    folder = os.path.dirname(os.path.abspath(__file__))
    with open(os.path.join(folder, "entry.png"), "rb") as handle:
        blob = handle.read()
    width, height = _check_png(blob)
    target_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    os.makedirs(target_dir, exist_ok=True)
    target = os.path.join(target_dir, "entry.png")
    with open(target, "wb") as handle:
        handle.write(blob)
    with open(target, "rb") as handle:
        landed = handle.read()
    digest = hashlib.sha256(blob).hexdigest()
    if len(landed) != len(blob):
        raise ValueError("the copy in %s is %d bytes, expected %d"
                         % (target_dir, len(landed), len(blob)))
    if hashlib.sha256(landed).hexdigest() != digest:
        raise ValueError("the copy in %s does not match entry.png"
                         % target_dir)
    print("entry.png handed over: %dx%d, %d bytes, sha256 %s... -> %s"
          % (width, height, len(blob), digest[:12], target))
    return 0


raise SystemExit(_deliver())
