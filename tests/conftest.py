# -*- coding: utf-8 -*-
"""Test fixtures.

Created on: 20/6/22
@author: Heber Trujillo <heber.trj.urt@gmail.com>
Licence,
"""
from datetime import date
from typing import Callable, Tuple

import pytest
from _pytest.fixtures import FixtureRequest, FixtureFunction
from sqlalchemy import create_engine
from sqlalchemy.engine.base import Engine
from sqlalchemy.orm import clear_mappers, sessionmaker
from sqlalchemy.orm.session import Session

from corelib.allocation.adapters.orm import metadata, start_mappers
from corelib.allocation.domain.model import (
    Batch,
    OrderId,
    OrderLine,
    Quantity,
    Reference,
    Sku,
)


def make_batch_and_line(
    order_sku: Sku, batch_sku: Sku, batch_qty: Quantity, line_qty: Quantity
) -> Tuple[Batch, OrderLine]:
    """Create one Batch and OrderLine.

    Args:
        order_sku: order skw.
        batch_sku: batch skw.
        batch_qty: batch available quantity.
        line_qty: line quantity.

    Returns:
        batch: purchased batch.
        line: order line.
    """
    return (
        Batch(
            Reference("batch-001"),
            Sku(batch_sku),
            Quantity(batch_qty),
            eta=date.today(),
        ),
        OrderLine(OrderId("order-123"), Sku(order_sku), Quantity(line_qty)),
    )


@pytest.fixture
def batch_line(request: FixtureRequest) -> Tuple[Batch, OrderLine]:
    """Batch Line fixture."""
    return make_batch_and_line(*request.param)


@pytest.fixture(scope="session")
def in_memory_db() -> Engine:
    """Create an in memory db to test."""
    engine = create_engine(url="sqlite:///:memory:")
    metadata.create_all(engine)
    return engine


@pytest.fixture(scope="session")
def session(in_memory_db: Engine) -> Session:
    """Create a session bound to in memory database."""
    start_mappers()
    yield sessionmaker(bind=in_memory_db)()
    clear_mappers()
