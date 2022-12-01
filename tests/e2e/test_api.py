# -*- coding: utf-8 -*-
"""This module test the API.

Created on: 20/6/22
@author: Heber Trujillo <heber.trj.urt@gmail.com>
Licence,
"""
import uuid
from typing import Callable

import pytest
import requests

import corelib.allocation.config as config


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


@pytest.mark.usefixtures("restart_api")
def test_happy_path_returns_201_and_allocated_batch(add_stock: Callable):
    """Test e2e aPI service layer."""
    sku, othersku = random_sku(), random_sku("other")
    earlybatch = random_batchref(1)
    laterbatch = random_batchref(2)
    otherbatch = random_batchref(3)
    add_stock(
        [
            (laterbatch, sku, 100, "2011-01-02"),
            (earlybatch, sku, 100, "2011-01-01"),
            (otherbatch, othersku, 100, None),
        ]
    )
    data = {"orderid": random_orderid(), "sku": sku, "qty": 3}
    url = config.get_api_url()

    r = requests.post(f"{url}/allocate", json=data)

    assert r.status_code == 201
    assert r.json()["batchref"] == earlybatch
