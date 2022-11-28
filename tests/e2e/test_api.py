# -*- coding: utf-8 -*-
"""This module test the API.

Created on: 20/6/22
@author: Heber Trujillo <heber.trj.urt@gmail.com>
Licence,
"""
import uuid


def random_suffix() -> str:
    """Get a random suffix."""
    return uuid.uuid4().hex[:6]


def random_sku(name: str = "") -> str:
    """Get a random sku.

    Args:
        name: name od the article.

    Returns:
        random_sku: name of the article plus a random suffix.
    """
    return f"sku-{name}-{random_suffix()}"


def random_batchref(name: str = "") -> str:
    """Get a random batch reference.

    Args:
        name: name of the batch reference

    Returns:
        random_batchref: a randomly batch name generated.
    """
    return f"batch-{name}-{random_suffix()}"


def random_orderid(name: str = "") -> str:
    """Get a random order id.

    Args:
        name: name of the order id

    Returns:
        random_orderid: a random order id generated.
    """
    return f"order-{name}-{random_suffix()}"
