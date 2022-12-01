# -*- coding: utf-8 -*-
"""Release testing module.

Created on: 21/6/22
@author: Heber Trujillo <heber.trj.urt@gmail.com>
Licence,
"""
import pytest

from corelib import __version__


@pytest.mark.unit
def test_semantic_version():
    """Test semantic version update."""
    assert __version__ == "0.4.1"
