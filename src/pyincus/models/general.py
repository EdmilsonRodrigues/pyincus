"""General Fields for PyIncus Models."""

from __future__ import annotations

from enum import Enum
from typing import Any

from ..config import Unset
from ..exceptions import PyIncusException


class ModelField:
    """Should be the default class field value of all fields of any model."""

    def __init__(self, cls, field_name: str):
        """Init model_field class."""
        self.field_name = field_name
        self.cls = cls

    def __eq__(self, other) -> FilterQuery:  # type: ignore
        """Return Filter Query for an equality."""
        return FilterQuery(self, FilterOperation.EQUALS, other)

    def __ne__(self, other) -> FilterQuery:  # type: ignore
        """Return Filter Query for an innequality."""
        return FilterQuery(self, FilterOperation.NOT_EQUALS, other)

    def __hash__(self) -> int:
        """Hash model field."""
        return hash(self.field_name)

    def __repr__(self) -> str:
        """Representation of ModelField."""
        return f'{self.cls.__name__}.{self.field_name}'

    def __str__(self) -> str:
        """Field name."""
        return self.field_name


class FilterOperation(Enum):
    """Operations able to filter fields by."""

    NOT = 'not'
    EQUALS = 'eq'
    AND = 'and'
    OR = 'or'
    NOT_EQUALS = 'ne'

    def __str__(self) -> str:
        """Return operation representation."""
        return self.value

    @classmethod
    def get_model_options(cls):
        """Return options that can be used to compare ModelField to a value."""
        return (cls.EQUALS, cls.NOT_EQUALS)


class FilterQuery:
    """Representation of queries on filter operations."""

    _repr_mapping = {
        FilterOperation.EQUALS: '==',
        FilterOperation.AND: 'and',
        FilterOperation.OR: 'or',
        FilterOperation.NOT_EQUALS: '!=',
    }

    def __init__(
        self,
        first_value,
        operation: FilterOperation,
        second_value: Any = Unset,
    ):
        """Init the Filter Query."""
        if second_value is Unset and operation != FilterOperation.NOT:
            raise PyIncusException(
                "Second value must always be set if operation isn't 'not'"
            )
        self.first_value = first_value
        self.operation = operation
        self.second_value = second_value

    def __repr__(self):
        """Return a programming-like representation."""
        if self.second_value is Unset:
            return f'not {self.first_value!r}'

        return ' '.join((
            repr(self.first_value),
            str(self._repr_mapping[self.operation]),
            repr(self.second_value),
        ))

    def __str__(self):
        """Return the used representation."""
        if self.second_value is Unset:
            return f'not {self.first_value}'

        stringify = str if isinstance(self.second_value, type(self)) else repr
        return f'{self.first_value} {self.operation} ' + stringify(
            self.second_value
        )

    def __eq__(self, other):
        """Evaluate equality between two queries."""
        return str(self) == str(other)

    def __hash__(self):
        """Hashes the query."""
        return hash(str(self))

    def __and__(self, other) -> FilterQuery:
        """Return Filter Query for an and."""
        return FilterQuery(self, FilterOperation.AND, other)

    def __or__(self, other) -> FilterQuery:
        """Return Filter Query for an or."""
        return FilterQuery(self, FilterOperation.OR, other)

    def __invert__(self) -> FilterQuery:
        """Return Filter Query for a not."""
        return FilterQuery(self, FilterOperation.NOT)
