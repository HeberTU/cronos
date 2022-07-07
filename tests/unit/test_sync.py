# -*- coding: utf-8 -*-
"""This module test file system sync.

Created on: 7/7/22
@author: Heber Trujillo <heber.trj.urt@gmail.com>
Licence,
"""
import os
from pathlib import Path
from typing import Tuple

from corelib.syncsys.sync import hash_file


def test_hash_file(files: Tuple[Path, Path, Path]):
    """Test if that hashed object has unique representation."""
    try:
        file_1, file_1_identical, file_2 = files

        hashed_1 = hash_file(file_1)
        hashed_1_identical = hash_file(file_1_identical)
        hashed_2 = hash_file(file_2)

        assert hashed_1 == hashed_1_identical
        assert hashed_1 != hashed_2

    finally:
        os.remove(file_1)
        os.remove(file_1_identical)
        os.remove(file_2)
