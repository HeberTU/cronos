# -*- coding: utf-8 -*-
"""This module test the domain model module.

Created on: 21/6/22
@author: Heber Trujillo <heber.trj.urt@gmail.com>
Licence,
"""
from datetime import (
    date,
    timedelta,
)
from typing import Callable

import pytest

from corelib.allocation.domain.model import (
    Batch,
    OrderLine,
    allocate,
)
from corelib.exceptions import OutOfStock

today = date.today()
tomorrow = today + timedelta(days=1)
later = tomorrow + timedelta(days=10)


@pytest.mark.unit
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


@pytest.mark.unit
@pytest.mark.parametrize(
    "batch_line", [["SMALL-TABLE", "SMALL-TABLE", 20, 10]], indirect=True
)
def test_can_allocate_if_available_greater_than_required(batch_line: Callable):
    """Test line gets allocated if sku matches and qty are correct."""
    batch, line = batch_line

    assert batch.can_allocate(line)


@pytest.mark.unit
@pytest.mark.parametrize(
    "batch_line", [["SMALL-TABLE", "SMALL-TABLE", 20, 25]], indirect=True
)
def test_cannot_allocate_if_available_smaller_than_required(
    batch_line: Callable,
):
    """Test line allocated fails if sku matches and qty are incorrect."""
    batch, line = batch_line
    assert not batch.can_allocate(line)


@pytest.mark.unit
@pytest.mark.parametrize(
    "batch_line", [["SMALL-TABLE", "BIG-TABLE", 20, 2]], indirect=True
)
def test_cannot_allocate_if_skus_do_not_match(batch_line: Callable):
    """Test line allocated fails if sku not matche and qty are correct."""
    batch, line = batch_line
    assert not batch.can_allocate(line)


@pytest.mark.unit
@pytest.mark.parametrize(
    "batch_line", [["SMALL-TABLE", "SMALL-TABLE", 20, 20]], indirect=True
)
def test_can_allocate_if_available_equal_to_required(batch_line: Callable):
    """Test line gets allocated if sku matches and qty are correct."""
    batch, line = batch_line
    assert batch.can_allocate(line)


@pytest.mark.unit
@pytest.mark.parametrize(
    "batch_line", [["ANGULAR-DESK", "ANGULAR-DESK", 20, 2]], indirect=True
)
def test_allocation_is_idempotent(batch_line: Callable):
    """Test that the same line does not get allocated multiple times."""
    batch, line = batch_line
    batch.allocate(line)
    batch.allocate(line)
    assert batch.available_quantity == 18


@pytest.mark.unit
def test_prefers_current_stock_batches_to_shipments():
    """Test allocate function will assing order line to stock."""
    in_stck_batch = Batch("in-stock-batch", "RETRO_CLOCK", 100, eta=None)
    shipment_batch = Batch("shipment", "RETRO_CLOCK", 100, eta=tomorrow)
    line = OrderLine("oref", "RETRO_CLOCK", 10)

    allocate(line=line, batches=[in_stck_batch, shipment_batch])

    assert in_stck_batch.available_quantity == 90
    assert shipment_batch.available_quantity == 100


@pytest.mark.unit
def test_prefers_earlier_batches():
    """Test allocate func will prefer allocate to earliest batche."""
    earliest = Batch("speedy-batch", "MINIMAL-TABLE", 100, eta=today)
    medium = Batch("normal-batch", "MINIMAL-TABLE", 100, eta=tomorrow)
    latest = Batch("slow-batch", "MINIMAL-TABLE", 100, eta=later)

    line = OrderLine("oref", "MINIMAL-TABLE", 10)

    allocate(line=line, batches=[earliest, medium, latest])

    assert earliest.available_quantity == 90
    assert medium.available_quantity == 100
    assert latest.available_quantity == 100


@pytest.mark.unit
def test_returns_allocated_batch_ref():
    """Test allocate func will return the batch reference."""
    in_stck_batch = Batch("in-stock-batch", "RETRO_CLOCK", 100, eta=None)
    shipment_batch = Batch("shipment", "RETRO_CLOCK", 100, eta=tomorrow)
    line = OrderLine("oref", "RETRO_CLOCK", 10)

    allocation = allocate(line=line, batches=[in_stck_batch, shipment_batch])

    assert allocation == in_stck_batch.reference


@pytest.mark.unit
def test_raises_out_of_stock_exception_if_cannot_allocate():
    """Test if we get out of stock when no batch can allocate line."""
    batch = Batch("batch1", "SMALL-DESK", 10, eta=today)
    allocate(line=OrderLine("order1", "SMALL-DESK", 10), batches=[batch])

    with pytest.raises(OutOfStock, match="SMALL-DESK"):
        allocate(line=OrderLine("order2", "SMALL-DESK", 11), batches=[batch])
