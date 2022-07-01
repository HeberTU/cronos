# -*- coding: utf-8 -*-
"""Repository module.

This module contains the repository pattern, shich is an abstraction over
persistent storage.

Created on: 20/6/22
@author: Heber Trujillo <heber.trj.urt@gmail.com>
Licence,
"""
from abc import (
    ABC,
    abstractmethod,
)
from enum import Enum
from typing import (
    List,
    Type,
)

from sqlalchemy.orm.session import Session

from corelib.allocation.domain.model import (
    Batch,
    Reference,
)


class RepositoryTyep(Enum):
    """Available repository implementations (adapters)."""

    sql: str = "SQLAlchemyRepository"
    in_memory: str = "InMemoryRepository"


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


class InMemoryRepository(AbstractRepository):
    """In memory repository."""

    def __init__(self, batches: List[Batch]):
        """Initialize a in-memory repo using a python set."""
        self._batches = set(batches)

    def add(self, batch: Batch) -> None:
        """Add batch to oir repository if it was not already on it.

        Args:
            batch: Order batch that will be added to the repository.

        Returns:
            None
        """
        self._batches.add(batch)

    def get(self, reference: Reference) -> Batch:
        """Return a previously added to the in-memory repository.

        Args:
            reference: Order batch reference.

        Returns:
            batch: Order batch.
        """
        return next(b for b in self._batches if b.reference == reference)

    def list(self) -> List[Batch]:
        """Return all the order batches saved in the repository.

        Returns:
            batches: List of all batches in SQL database.
        """
        return list(self._batches)


def repository_maker(
    repository_type: RepositoryTyep,
) -> Type[AbstractRepository]:
    """Return the Repository class according to specifications.

    Args:
        repository_type: Type of repository class

    Returns:
        Repository: repository class
    """
    implementations = {
        cls.__name__: cls for cls in AbstractRepository.__subclasses__()
    }

    try:
        cls = implementations.get(repository_type.value)
    except KeyError:
        raise NotImplementedError

    return cls
