# -*- coding: utf-8 -*-
"""This module test E2E the file system sync.

Created on: 7/7/22
@author: Heber Trujillo <heber.trj.urt@gmail.com>
Licence,
"""
import shutil
import tempfile
from pathlib import Path

import pytest

from corelib.syncsys.sync import sync


@pytest.mark.e2e
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


@pytest.mark.e2e
def test_when_a_file_has_been_renamed_in_the_source():
    """Test when file has been renamed in the source directory."""
    try:
        source = tempfile.mkdtemp()
        dest = tempfile.mkdtemp()

        content = "This file was renamed."
        source_path = Path(source) / "source-filname"
        old_det_path = Path(dest) / "dest-filename"
        expected_dest_path = Path(dest) / "source-filname"

        source_path.write_text(content)
        old_det_path.write_text(content)

        sync(source, dest)

        assert old_det_path.exists() is False
        assert expected_dest_path.read_text() == content

    finally:
        shutil.rmtree(source)
        shutil.rmtree(dest)


@pytest.mark.e2e
def test_when_a_file_exists_in_the_destination_but_not_the_source():
    """Test when file has been renamed in the source directory."""
    try:
        source = tempfile.mkdtemp()
        dest = tempfile.mkdtemp()

        content = "This file was renamed."
        det_path = Path(dest) / "dest-filename"

        det_path.write_text(content)

        sync(source, dest)

        assert det_path.exists() is False

    finally:
        shutil.rmtree(source)
        shutil.rmtree(dest)
