"""General Fields for PyIncus Models."""

from __future__ import annotations

from enum import Enum
from typing import Any

from ..config import Unset
from ..exceptions import PyIncusException


class ModelField:
    """Should be the default class field value of all fields of any model."""

    def __init__(self, field_name: str):
        """Init model_field class."""
        self.field_name = field_name

    def __eq__(self, other) -> FilterQuery:  # type: ignore
        """Return Filter Query for an equality."""
        return FilterQuery(self.field_name, FilterOperation.EQUALS, other)

    def __hash__(self) -> int:
        """Hash model field."""
        return hash(self.field_name)

    def __and__(self, other) -> FilterQuery:
        """Return Filter Query for an and."""
        return FilterQuery(self.field_name, FilterOperation.AND, other)

    def __or__(self, other) -> FilterQuery:
        """Return Filter Query for an or."""
        return FilterQuery(self.field_name, FilterOperation.OR, other)

    def __ne__(self, other) -> FilterQuery:  # type: ignore
        """Return Filter Query for an innequality."""
        return FilterQuery(self.field_name, FilterOperation.NOT_EQUALS, other)

    def __invert__(self) -> FilterQuery:
        """Return Filter Query for a not."""
        return FilterQuery(self.field_name, FilterOperation.NOT)


class FilterOperation(Enum):
    """Operations able to filter fields by."""

    NOT = 'not'
    EQUALS = 'eq'
    AND = 'and'
    OR = 'or'
    NOT_EQUALS = 'ne'


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
        """Init  the Filter Query."""
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
            return f'not {self.second_value!r}'

        return ' '.join(
            map(
                repr,
                (
                    self.first_value,
                    self._repr_mapping[self.operation],
                    self.second_value,
                ),
            )
        )

    def __str__(self):
        """Return the used representation."""
        if self.second_value is Unset:
            return f'not {self.first_value!r}'

        return ' '.join(
            map(
                repr,
                (self.first_value, self.operation.value, self.second_value),
            )
        )
