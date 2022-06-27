# -*- coding: utf-8 -*-
"""Object relational mapper module.

Created on: 20/6/22
@author: Heber Trujillo <heber.trj.urt@gmail.com>
Licence,
"""
from sqlalchemy import (
    Column,
    Date,
    ForeignKey,
    Integer,
    MetaData,
    String,
    Table,
)
from sqlalchemy.orm import (
    mapper,
    relationship,
)

import corelib.allocation.domain.model as model

metadata = MetaData()

order_lines = Table(
    "order_lines",
    metadata,
    Column("id", Integer, primary_key=True, autoincrement=True),
    Column("sku", String(255)),
    Column("qty", Integer, nullable=False),
    Column("orderid", String(255)),
)

batches = Table(
    "batches",
    metadata,
    Column("id", Integer, primary_key=True, autoincrement=True),
    Column("reference", String(255)),
    Column("sku", String(255)),
    Column("_purchased_quantity", Integer, nullable=False),
    Column("eta", Date, nullable=True),
)


allocations = Table(
    "allocations",
    metadata,
    Column("id", Integer, primary_key=True, autoincrement=True),
    Column("orderline_id", ForeignKey("order_lines.id")),
    Column("batch_id", ForeignKey("batches.id")),
)


def start_mappers() -> None:
    """Map domain object to database tables.

    Returns:
        None.
    """
    lines_mapper = mapper(class_=model.OrderLine, local_table=order_lines)
    mapper(
        model.Batch,
        batches,
        properties={
            "_allocations": relationship(
                lines_mapper,
                secondary=allocations,
                collection_class=set,
            )
        },
    )
    return lines_mapper
