#!/usr/bin/env python3
"""Entry point for news-image-20261120.

Copies the pre-drawn front page (entry.png, drawn by draw.py in this
repository) to the output directory. Standard library only, no network,
fully deterministic: the same bytes every run.
"""
import os
import shutil


def main():
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "out")
    os.makedirs(out_dir, exist_ok=True)
    here = os.path.dirname(os.path.abspath(__file__))
    src = os.path.join(here, "entry.png")
    dst = os.path.join(out_dir, "entry.png")
    shutil.copyfile(src, dst)


if __name__ == "__main__":
    main()
