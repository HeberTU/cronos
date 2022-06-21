# -*- coding: utf-8 -*-
"""This module test the domain model module.

Created on: 21/6/22
@author: Heber Trujillo <heber.trj.urt@gmail.com>
Licence,
"""
from datetime import date, timedelta
from typing import Callable

import pytest

today = date.today()
tomorrow = today + timedelta(days=1)
later = tomorrow + timedelta(days=10)


@pytest.mark.parametrize(
    "batch_line", [["SMALL-TABLE", "SMALL-TABLE", 20, 2]], indirect=True
)
def test_allocating_to_a_batch_reduces_the_available_quantity(
    batch_line: Callable,
):
    """Test allocation reduce batch available quantity."""
    batch, line = batch_line
    batch.allocate(line)
    assert batch.available_quantity == 18


@pytest.mark.parametrize(
    "batch_line", [["SMALL-TABLE", "SMALL-TABLE", 20, 10]], indirect=True
)
def test_can_allocate_if_available_greater_than_required(batch_line: Callable):
    """Test line gets allocated if sku matches and qty are correct."""
    batch, line = batch_line

    assert batch.can_allocate(line)


@pytest.mark.parametrize(
    "batch_line", [["SMALL-TABLE", "SMALL-TABLE", 20, 25]], indirect=True
)
def test_cannot_allocate_if_available_smaller_than_required(
    batch_line: Callable,
):
    """Test line allocated fails if sku matches and qty are incorrect."""
    batch, line = batch_line
    assert not batch.can_allocate(line)


@pytest.mark.parametrize(
    "batch_line", [["SMALL-TABLE", "BIG-TABLE", 20, 2]], indirect=True
)
def test_cannot_allocate_if_skus_do_not_match(batch_line: Callable):
    """Test line allocated fails if sku not matche and qty are correct."""
    batch, line = batch_line
    assert not batch.can_allocate(line)


@pytest.mark.parametrize(
    "batch_line", [["SMALL-TABLE", "SMALL-TABLE", 20, 20]], indirect=True
)
def test_can_allocate_if_available_equal_to_required(batch_line: Callable):
    """Test line gets allocated if sku matches and qty are correct."""
    batch, line = batch_line
    assert batch.can_allocate(line)


@pytest.mark.parametrize(
    "batch_line", [["ANGULAR-DESK", "ANGULAR-DESK", 20, 2]], indirect=True
)
def test_allocation_is_idempotent(batch_line: Callable):
    """Test that the same line does not get allocated multiple times."""
    batch, line = batch_line
    batch.allocate(line)
    batch.allocate(line)
    assert batch.available_quantity == 18


def test_prefers_warehouse_batches_to_shipments():
    """Test to do."""
    pytest.fail("todo")


def test_prefers_earlier_batches():
    """Test to do."""
    pytest.fail("todo")
