# -*- coding: utf-8 -*-
"""Object relational mapper module.

Created on: 20/6/22
@author: Heber Trujillo <heber.trj.urt@gmail.com>
Licence,
"""
from sqlalchemy import Column, Integer, MetaData, String, Table
from sqlalchemy.orm import mapper

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


def start_mappers() -> None:
    """Map domain object to database tables.

    Returns:
        None.
    """
    lines_mapper = mapper(class_=model.OrderLine, local_table=order_lines)
    return lines_mapper
