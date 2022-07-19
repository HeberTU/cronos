# -*- coding: utf-8 -*-
"""Test fixtures.

Created on: 20/6/22
@author: Heber Trujillo <heber.trj.urt@gmail.com>
Licence,
"""
import time
from datetime import date
from pathlib import Path
from typing import (
    Callable,
    Tuple,
)

import pytest
import requests
from _pytest.fixtures import FixtureRequest
from requests.exceptions import ConnectionError
from sqlalchemy import create_engine
from sqlalchemy.engine.base import Engine
from sqlalchemy.exc import OperationalError
from sqlalchemy.orm import (
    clear_mappers,
    sessionmaker,
)
from sqlalchemy.orm.session import Session

import corelib.allocation.config as config
from corelib.allocation.adapters.orm import (
    metadata,
    start_mappers,
)
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


@pytest.fixture
def session(in_memory_db: Engine) -> Session:
    """Create a session bound to in memory database."""
    start_mappers()
    yield sessionmaker(bind=in_memory_db, expire_on_commit=False)()
    clear_mappers()


@pytest.fixture
def files() -> Tuple[Path, Path, Path]:
    """Create a temporary file and return its path."""
    files_dict = {
        "./test_1.txt": "Cronos test file",
        "./test_1_identical.txt": "Cronos test file",
        "./test_2.txt": "Cronos test file.",
    }

    file_paths = []
    for name, content in files_dict.items():
        with open(name, "w") as file:
            file.write(content)

        file_paths.append(Path(name))

    return tuple(file_paths)


def wait_for_postgres_to_come_up(engine: Engine):
    """Wait for postgres connection."""
    deadline = time.time() + 10
    while time.time() < deadline:
        try:
            return engine.connect()
        except OperationalError:
            time.sleep(0.5)
    pytest.fail("Postgres never came up")


def wait_for_webapp_to_come_up():
    """Wait for web app connection."""
    deadline = time.time() + 10
    url = config.get_api_url()
    while time.time() < deadline:
        try:
            return requests.get(url)
        except ConnectionError:
            time.sleep(0.5)
    pytest.fail("API never came up")


@pytest.fixture(scope="session")
def postgres_db() -> Engine:
    """Create the domain models in prostgres."""
    engine = create_engine(config.get_postgres_uri())
    wait_for_postgres_to_come_up(engine)
    metadata.create_all(engine)
    return engine


@pytest.fixture
def postgres_session(postgres_db: Engine) -> Session:
    """Start the mappers and return the session to interact."""
    start_mappers()
    yield sessionmaker(bind=postgres_db)()
    clear_mappers()


@pytest.fixture
def add_stock(postgres_session: Session) -> Callable:
    """Add stock to test.

    Args:
        postgres_session: postgres session.

    Returns:
        _add_stock
    """
    batches_added = set()
    skus_added = set()

    def _add_stock(lines):
        for ref, sku, qty, eta in lines:
            postgres_session.execute(
                "INSERT INTO batches "
                "(reference, sku, _purchased_quantity, eta)"
                " VALUES (:ref, :sku, :qty, :eta)",
                dict(ref=ref, sku=sku, qty=qty, eta=eta),
            )
            [[batch_id]] = postgres_session.execute(
                "SELECT id FROM batches WHERE reference=:ref AND sku=:sku",
                dict(ref=ref, sku=sku),
            )
            batches_added.add(batch_id)
            skus_added.add(sku)
        postgres_session.commit()

    yield _add_stock

    for batch_id in batches_added:
        postgres_session.execute(
            "DELETE FROM allocations WHERE batch_id=:batch_id",
            dict(batch_id=batch_id),
        )
        postgres_session.execute(
            "DELETE FROM batches WHERE id=:batch_id",
            dict(batch_id=batch_id),
        )
    for sku in skus_added:
        postgres_session.execute(
            "DELETE FROM order_lines WHERE sku=:sku",
            dict(sku=sku),
        )
        postgres_session.commit()


@pytest.fixture
def restart_api():
    """Restore API."""
    (Path(__file__).parent / "flask_app.py").touch()
    time.sleep(0.5)
    wait_for_webapp_to_come_up()
