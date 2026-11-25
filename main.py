"""Entry program: copy the committed front page to /output/entry.png.

Standard library only. No network, no fonts, no Pillow needed at run time:
the image is drawn at build time by render.py and shipped in this repo.
Both runs write the same bytes because the source file never changes.
"""
import os
import shutil
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.join(HERE, "entry.png")


def main():
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    os.makedirs(out_dir, exist_ok=True)
    dst = os.path.join(out_dir, "entry.png")
    if not os.path.isfile(SRC):
        print("missing source image:", SRC, file=sys.stderr)
        sys.exit(1)
    shutil.copyfile(SRC, dst)
    if os.path.getsize(dst) != os.path.getsize(SRC):
        print("copy size mismatch", file=sys.stderr)
        sys.exit(1)
    print("wrote", dst, os.path.getsize(dst), "bytes (identical to source)")


if __name__ == "__main__":
    main()
