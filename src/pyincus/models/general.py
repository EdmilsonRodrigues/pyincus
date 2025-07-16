"""General Fields for PyIncus Models."""

from enum import Enum
from typing import Any


class ModelField:
    """Should be the default value of all fields of any model."""

    def __init__(self, field_name: str):
        """Init model_field class."""
        self.field_name = field_name

    def __eq__(self, other):
        return FilterQuery(self.field_name, FilterOperation.EQUALS, other)

    def __and__(self, other):
        return FilterQuery(self.field_name, FilterOperation.AND, other)

    def __or__(self, other):
        return FilterQuery(self.filter_name, FilterOperation.OR, other)


class FilterOperation(Enum):
    NOT = 'not'
    EQUALS = 'eq'
    AND = 'and'
    OR = 'or'
    NOT_EQUALS = 'ne'


class FilterQuery:
    """Representation of queries on filter operations."""

    _repr_mapping = {
        FilterOperation.NOT: 'not',
        FilterOperation.EQUALS: '==',
        FilterOperation.AND: 'and',
        FilterOperation.OR: 'or',
        FilterOperation.NOT_EQUALS: '!=',
    }

    def __init__(
        self, first_value, operation: FilterOperation, second_value: Any
    ):
        """Init  the Filter Query."""
        self.first_value = first_value
        self.operation = operation
        self.second_value = second_value

    def __repr__(self):
        """Return a programming-like representation."""
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
        return ' '.join(
            map(
                repr,
                (self.first_value, self.operation.value, self.second_value),
            )
        )
