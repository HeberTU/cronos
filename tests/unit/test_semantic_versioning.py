# -*- coding: utf-8 -*-
"""Release testing module.

Created on: 21/6/22
@author: Heber Trujillo <heber.trj.urt@gmail.com>
Licence,
"""
from corelib import __version__


def test_semantic_version():
    """Test semantic version update."""
    assert __version__ == "0.3.0"
