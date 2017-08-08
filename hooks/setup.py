#!/usr/bin/env python
import os
from pathlib import PosixPath

target_files = (
    'pre-commit',
)

src_dir = os.path.dirname(os.path.abspath(__file__))
dest_dir = os.path.join(src_dir, os.path.pardir, '.git', 'hooks')

for file in target_files:
    filepath_src = os.path.join(src_dir, file)
    filepath_dest = os.path.join(dest_dir, file)
    if not PosixPath(filepath_dest).is_symlink():
        os.symlink(filepath_src, filepath_dest)
