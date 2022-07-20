# -*- coding: utf-8 -*-
"""Service module for allocation libray.

Created on: 20/6/22
@author: Heber Trujillo <heber.trj.urt@gmail.com>
Licence,
"""
from typing import (
    List,
    Type,
)

from sqlalchemy.orm.session import Session

from corelib.allocation.adapters.repository import AbstractRepository
from corelib.allocation.domain.model import (
    Batch,
    OrderLine,
    Sku,
)
from corelib.allocation.domain.model import allocate as _allocate
from corelib.exceptions import InvalidSku


def is_valid_sku(sku: Sku, batches: List[Batch]) -> bool:
    """Validate if a sku exists in a list of batches.

    Args:
        sku: product identifier.
        batches: list of batches.

    Returns:
        True if sku is in batches list.
    """
    return sku in {b.sku for b in batches}


def allocate(
    line: OrderLine, repo: Type[AbstractRepository], session: Session
) -> str:
    """Allocate order line to available batches for a given repo.

    Args:
        line: Order line to allocate.
        repo: Data repository.
        session: data base session.

    Returns:
        batchref: batch reference to which the order was assigned.
    """
    batches = repo.list()
    if not is_valid_sku(line.sku, batches):
        raise InvalidSku(f"Invalid sku {line.sku}")

    batchref = _allocate(line, batches)

    session.commit()

    return batchref
