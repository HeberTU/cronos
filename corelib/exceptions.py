# -*- coding: utf-8 -*-
"""Exceptions module.

Created on: 23/6/22
@author: Heber Trujillo <heber.trj.urt@gmail.com>
Licence,
"""


class OutOfStock(Exception):
    """Exception to express that there is no batch to allocate line."""

    pass


class InvalidSku(Exception):
    """Exception to express that SKU from an order line is invalid."""

    pass
