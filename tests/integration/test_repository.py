# -*- coding: utf-8 -*-
"""This module that the repository is correctly integrated with database.

Created on: 20/6/22
@author: Heber Trujillo <heber.trj.urt@gmail.com>
Licence,
"""
from _pytest.fixtures import FixtureFunction

from corelib.allocation.adapters.repository import SQLAlchemyRepository
from corelib.allocation.domain.model import Batch


def test_repository_can_Save_a_batch(session: FixtureFunction):
    """Test if batches are correctly persisted."""
    batch = Batch(ref="batch1", sku="OLD-TABLE", qty=100, eta=None)

    repo = SQLAlchemyRepository(session)

    repo.add(batch)

    session.commit()

    rows = list(
        session.execute(
            'SELECT reference, sku, _purchased_quantity, eta FROM "batches"'
        )
    )

    assert rows == [("batch1", "OLD-TABLE", 100, None)]
