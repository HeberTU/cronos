# -*- coding: utf-8 -*-
"""This module contains the Domain Model use to capture the business logic.

Created on: 20/6/22
@author: Heber Trujillo <heber.trj.urt@gmail.com>
Licence,
"""

from dataclasses import dataclass
from datetime import date
from typing import NewType, Optional

OrderId = NewType("OrderId", str)
Quantity = NewType("Quantity", int)
Sku = NewType("Quantity", int)
Reference = NewType("Reference", str)


@dataclass(frozen=True)
class OrderLine:
    """Represent an order line within a Customer order."""

    orderid: OrderId
    sku: Sku
    qty: Quantity


class Batch:
    """Model for the batches of stock that the purchasing department orders."""

    def __init__(
        self, ref: Reference, sku: Sku, qty: Quantity, eta: Optional[date]
    ):
        """Initialize a Batch instance.

        Args:
            ref: Reference number to track the batch.
            sku: Prodict identifier.
            qty: Purchased quantity.
            eta: Estimated time of arrival.
        """
        self.reference = ref
        self.sku = sku
        self.eta = eta
        self._purchased_quantity = qty
        self._allocations = set()

    def allocate(self, line: OrderLine):
        """Allocate customer order line to order batch.

         The order line quantity only gets alloctated to batch if order
         quantity is less or equal than batch available quantity and the SKUs
         matche.

        Args:
            line: Customer order line.

        Returns:
            None
        """
        if self.can_allocate(line):
            self._allocations.add(line)

    def deallocate(self, line: OrderLine):
        """Deallocate customer order line to order batch.

         The order line only ggets deallocated if it as previously allocated
         to the batch.

        Args:
            line: Customer order line.

        Returns:
            None
        """
        if line in self._allocations:
            self._allocations.remove(line)

    @property
    def allocated_quantity(self) -> int:
        """Calculate number of allocated items inside the batch."""
        return sum(line.qty for line in self._allocations)

    @property
    def available_quantity(self) -> int:
        """Calculate number of available items inside the batch."""
        return self._purchased_quantity - self.allocated_quantity

    def can_allocate(self, line: OrderLine) -> bool:
        """Test if the customer order line can be allocated to the batch.

        An order line only can be allocated if its sku matches the batch sku
        and its quantity <= batch available quantity.

        Args:
            line:

        Returns:
            True if customer order line can be allocated to batch.
        """
        return self.sku == line.sku and line.qty <= self.available_quantity
