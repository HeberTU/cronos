# -*- coding: utf-8 -*-
"""This module test E2E the file system sync.

Created on: 7/7/22
@author: Heber Trujillo <heber.trj.urt@gmail.com>
Licence,
"""
import shutil
import tempfile
from pathlib import Path

from corelib.syncsys.sync import sync


def test_when_a_file_exists_in_the_source_but_not_the_destination():
    """Test when there is a file on source and not in detination."""
    try:
        source = tempfile.mkdtemp()
        dest = tempfile.mkdtemp()

        content = "Useful file."
        (Path(source) / "test-file").write_text(content)

        sync(source, dest)

        expected_path = Path(dest) / "test-file"
        assert expected_path.exists()
        assert expected_path.read_text() == content

    finally:
        shutil.rmtree(source)
        shutil.rmtree(dest)
