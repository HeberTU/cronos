# -*- coding: utf-8 -*-
"""This module implements the synchronization logic using SHA-1.

Created on: 7/7/22
@author: Heber Trujillo <heber.trj.urt@gmail.com>
Licence,
"""
import hashlib
import os
import shutil
from pathlib import Path
from typing import Dict

BLOCKSIZE = 65536


def hash_file(path: Path) -> str:
    """Hash a file.

    Args:
        path: file path.

    Returns:
        hash: file hash representation.
    """
    hasher = hashlib.sha1()
    with path.open("rb") as file:
        buf = file.read(BLOCKSIZE)
        while buf:
            hasher.update(buf)
            buf = file.read(BLOCKSIZE)
    return hasher.hexdigest()


def read_paths_and_hashes(root: Path) -> Dict[str, str]:
    """Create a hash mapping for all the files in the root path.

    Args:
        root: root path directory.

    Returns:
        hashes: hash mapping of files at root derectory.
    """
    hashes = {}
    for folder, _, files in os.walk(root):
        for file in files:
            hashes[hash_file(Path(folder) / file)] = file
    return hashes


def sync(source: Path, dest: Path) -> None:
    """Synchronize two file directories.

    Args:
        source: source directory.
        dest: destination directory.

    Returns:
        None.
    """
    # Walk the source folder and build a dict of filenames and their hashes
    source_hashes = {}
    for folder, _, files in os.walk(source):
        for fn in files:
            source_hashes[hash_file(Path(folder) / fn)] = fn

    seen = set()  # Keep track of the files we've found in the target

    # Walk the target folder and get the filenames and hashes
    for folder, _, files in os.walk(dest):
        for fn in files:
            dest_path = Path(folder) / fn
            dest_hash = hash_file(dest_path)
            seen.add(dest_hash)

            # if there's a file in target that's not in source, delete it
            if dest_hash not in source_hashes:
                dest_path.remove()

            # if there's a file in target that has a different path in source,
            # move it to the correct path
            elif dest_hash in source_hashes and fn != source_hashes[dest_hash]:
                shutil.move(dest_path, Path(folder) / source_hashes[dest_hash])

    # for every file that appears in source but not target, copy the file to
    # the target
    for src_hash, fn in source_hashes.items():
        if src_hash not in seen:
            shutil.copy(Path(source) / fn, Path(dest) / fn)
