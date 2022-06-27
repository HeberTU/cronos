# -*- coding: utf-8 -*-
"""Repository module.

This module contains the repository pattern, shich is an abstraction over
persistent storage.

Created on: 20/6/22
@author: Heber Trujillo <heber.trj.urt@gmail.com>
Licence,
"""
from abc import ABC, abstractmethod
from typing import List

from sqlalchemy.orm.session import Session

from corelib.allocation.domain.model import Batch, Reference


class AbstractRepository(ABC):
    """Abstract repository."""

    @abstractmethod
    def add(self, batch: Batch) -> None:
        """Add new batch in the repository.

        Args:
            batch: Order batch that will be added to the repository.

        Returns:
            None
        """
        raise NotImplementedError

    @abstractmethod
    def get(self, reference: Reference) -> Batch:
        """Return a previously added item.

        Args:
            reference: Order batch reference.

        Returns:
            batch: Order batch.
        """
        raise NotImplementedError


class SQLAlchemyRepository(AbstractRepository):
    """SQL repository."""

    def __init__(self, session: Session):
        """Initialize a sql repository with the provided session.

        Args:
            session: Database session.
        """
        self.session = session

    def add(self, batch: Batch) -> None:
        """Add new batch in the SQL database via repository pattern.

        Args:
            batch: Order batch that will be added to the repository.

        Returns:
            None
        """
        self.session.add(batch)

    def get(self, reference: Reference) -> Batch:
        """Return a previously added item to de SQL database via repository.

        Args:
            reference: Order batch reference.

        Returns:
            batch: Order batch.
        """
        return self.session.query(Batch).filter_by(reference=reference).one()

    def list(self) -> List[Batch]:
        """Return all the order batches saved in SQL database.

        Returns:
            batches: List of all batches in SQL database.
        """
        return self.session.query(Batch).all()
