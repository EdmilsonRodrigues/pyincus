"""Model Field and Filter Query classes."""

from __future__ import annotations

from enum import Enum
from typing import Any, Self

from ..config import Unset
from ..exceptions import PyIncusException


class ModelField:
    """
    Default value for Models' attributes.

    All models should have instances of this class as their class default value
    for their attributes.

    They will return FilterQuery when tested for equality or inequality.
    They will be instantiated by the BaseIncusMeta.
    """

    def __init__(self, cls: type, field_name: str) -> None:
        """
        Init model_field class.

        :param cls: The model class where this instance is a field.
        :param field_name: The field name of this instance.
        """
        self.cls = cls
        self.field_name = field_name

    def __eq__(self, other) -> FilterQuery:  # type: ignore
        """
        Return Filter Query for an equality.

        :param other: The value to which compare to.
        :returns: A filter query for equality.
        """
        return FilterQuery(self, FilterOperation.EQUALS, other)

    def __ne__(self, other) -> FilterQuery:  # type: ignore
        """
        Return Filter Query for an inequality.

        :param other: The value to which compare to.
        :returns: A filter query for inequality.
        """
        return FilterQuery(self, FilterOperation.NOT_EQUALS, other)

    def __hash__(self) -> int:
        """Hash the model field for sets."""
        return hash(self.field_name)

    def __repr__(self) -> str:
        """Representation of ModelField used for debugging."""
        return f'{self.cls.__name__}.{self.field_name}'

    def __str__(self) -> str:
        """Field name used for queries."""
        return self.field_name


class FilterOperation(Enum):
    """Operations able to filter fields by."""

    NOT = 'not'
    EQUALS = 'eq'
    AND = 'and'
    OR = 'or'
    NOT_EQUALS = 'ne'

    def __str__(self) -> str:
        """Return operation string representation for query."""
        return self.value

    @classmethod
    def get_model_options(cls):
        """Return options that can be used to compare ModelField to a value."""
        return (cls.EQUALS, cls.NOT_EQUALS)


class FilterQuery:
    """
    Representation of queries for filter operations.

    This class contains the information needed to make a query to incus.
    By using str(filter_query) the query in incus query format is returned.
    """

    _repr_mapping = {
        FilterOperation.EQUALS: '==',
        FilterOperation.AND: 'and',
        FilterOperation.OR: 'or',
        FilterOperation.NOT_EQUALS: '!=',
    }

    def __init__(
        self,
        first_value: ModelField | Self,
        operation: FilterOperation,
        second_value: Any = Unset,
    ) -> None:
        """
        Init the Filter Query.

        :param first_value: The value to apply logical operation to.
        :param operation: The logical operation to apply.
        :second_value: The value that the operation will be applied in relation
        to the first one. If the operation is a NOT, this should be Unset.
        """
        if (second_value is Unset) ^ (operation == FilterOperation.NOT):
            raise PyIncusException(
                "Second value must always be set if operation isn't 'not'"
                " and never be set if operation is 'not'"
            )
        self.first_value = first_value
        self.operation = operation
        self.second_value = second_value

    def __repr__(self):
        """Return a programming-like representation, clear for debugging."""
        if self.second_value is Unset:
            return f'not {self.first_value!r}'

        return ' '.join((
            repr(self.first_value),
            str(self._repr_mapping[self.operation]),
            repr(self.second_value),
        ))

    def __str__(self):
        """Return a string with the filter following the incus format."""
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
        return hash(self.first_value)

    def __and__(self, other) -> FilterQuery:
        """Return Filter Query for a conjunction."""
        return FilterQuery(self, FilterOperation.AND, other)

    def __or__(self, other) -> FilterQuery:
        """Return Filter Query for a disjunction."""
        return FilterQuery(self, FilterOperation.OR, other)

    def __invert__(self) -> FilterQuery:
        """Return Filter Query for an inversion."""
        return FilterQuery(self, FilterOperation.NOT)
