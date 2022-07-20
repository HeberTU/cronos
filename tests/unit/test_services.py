# -*- coding: utf-8 -*-
"""Test module for servide layer.

Created on: 20/6/22
@author: Heber Trujillo <heber.trj.urt@gmail.com>
Licence,
"""
import pytest

from corelib.allocation.adapters.repository import InMemoryRepository
from corelib.allocation.domain.model import (
    Batch,
    OrderLine,
)
from corelib.allocation.service_layer.services import allocate
from corelib.exceptions import InvalidSku


class FakeSession:
    """Fake session."""

    committed = False

    def commit(self):
        """Fake commit action."""
        self.committed = True


def test_returns_allocation():
    """Test allocation success."""
    line = OrderLine("o1", "COMPLICATED-LAMP", 10)
    batch = Batch("b1", "COMPLICATED-LAMP", 100, eta=None)
    repo = InMemoryRepository([batch])

    result = allocate(line, repo, FakeSession())

    assert result == "b1"


def test_error_for_invalid_sku():
    """Test the rght exception raises for invalid SKU."""
    line = OrderLine("o1", "NONEXISTENTSKU", 10)
    batch = Batch("b1", "AREALSKU", 100, eta=None)
    repo = InMemoryRepository([batch])

    with pytest.raises(InvalidSku, match="Invalid sku NONEXISTENTSKU"):
        allocate(line, repo, FakeSession())


def test_commits():
    """Test that data was persisted."""
    line = OrderLine("o1", "OMINOUS-MIRROR", 10)
    batch = Batch("b1", "OMINOUS-MIRROR", 100, eta=None)
    repo = InMemoryRepository([batch])
    session = FakeSession()

    allocate(line, repo, session)
    assert session.committed is True
