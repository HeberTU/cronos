# -*- coding: utf-8 -*-
"""This module that the repository is correctly integrated with database.

Created on: 20/6/22
@author: Heber Trujillo <heber.trj.urt@gmail.com>
Licence,
"""
from _pytest.fixtures import FixtureFunction
from sqlalchemy.engine.cursor import CursorResult
from sqlalchemy.orm.session import Session

from corelib.allocation.adapters.repository import SQLAlchemyRepository
from corelib.allocation.domain.model import (
    Batch,
    OrderLine,
    Reference,
)


def insert_order_line(session: Session) -> CursorResult:
    """Insert order data via raw SQL to test the repo.get() method.

    Args:
        session: Database session.

    Returns:
        orderline_id: Order line database identifier.
    """
    session.execute(
        "INSERT INTO order_lines (orderid, sku, qty)"
        'VALUES ("order1", "GENERIC-SOFA", 12)'
    )

    orderline_id = session.execute(
        "SELECT id FROM order_lines WHERE orderid=:orderid AND sku=:sku",
        dict(orderid="order1", sku="GENERIC-SOFA"),
    )

    return orderline_id


def insert_batch(session: Session, reference: Reference) -> CursorResult:
    """Insert batch  data via raw SQL to test the repo.get() method.

    Args:
        session: Database session.
        reference: Batch reference.

    Returns:
        batch_id: batch database identifier.
    """
    session.execute(
        "INSERT INTO batches (reference, sku, _purchased_quantity, eta)"
        ' VALUES (:reference, "GENERIC-SOFA", 100, null)',
        dict(reference=reference),
    )

    batch_id = session.execute(
        '''SELECT id FROM batches WHERE
        reference=:reference AND sku="GENERIC-SOFA"''',
        dict(reference=reference),
    )

    return batch_id


def insert_allocations(
    session: Session, orderline_id: int, batch_id: int
) -> None:
    """Insert allocation record.

    Args:
        session: Database session.
        orderline_id: Order line database identifier.
        batch_id: batch database identifier.

    Returns:
        None
    """
    session.execute(
        "INSERT INTO allocations (orderline_id, batch_id)"
        " VALUES (:orderline_id, :batch_id)",
        dict(orderline_id=orderline_id, batch_id=batch_id),
    )


def test_repository_can_save_a_batch(session: FixtureFunction):
    """Test if batches are correctly persisted."""
    batch = Batch(ref="batch1", sku="OLD-TABLE", qty=100, eta=None)

    repo = SQLAlchemyRepository(session)

    repo.add(batch)

    session.commit()

    rows = session.execute(
        'SELECT reference, sku, _purchased_quantity, eta FROM "batches"'
    )

    assert list(rows) == [("batch1", "OLD-TABLE", 100, None)]


def test_repository_can_retrieve_a_batch_with_allocations(
    session: FixtureFunction,
):
    """Test."""
    orderline_id = list(insert_order_line(session))[0][0]

    batch_id = list(insert_batch(session, "batch2"))[0][0]
    insert_batch(session, "batch3")

    insert_allocations(session, orderline_id, batch_id)

    repo = SQLAlchemyRepository(session)
    retrieved = repo.get("batch2")
    expected = Batch("batch2", "GENERIC-SOFA", 100, eta=None)
    assert retrieved == expected
    assert retrieved.sku == expected.sku
    assert retrieved._purchased_quantity == expected._purchased_quantity
    assert retrieved._allocations == {
        OrderLine("order1", "GENERIC-SOFA", 12),
    }
