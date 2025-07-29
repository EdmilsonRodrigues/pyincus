"""Test ModelField and FilterQuery."""

import random

import pytest

from pyincus.models.general import FilterOperation, FilterQuery, ModelField


@pytest.fixture
def model_field_generator(faker):
    """Generate a model field."""
    return lambda: ModelField(object, faker.word())


@pytest.fixture
def random_query(faker, model_field_generator):
    """Generate a FilterQuery with a random value."""
    field = model_field_generator()
    operator = random.choice(FilterOperation.get_model_options())
    return lambda: FilterQuery(field, operator, faker.word())


def test_model_field_value_equality(
    faker, model_field_generator, random_query
):
    """
    Test model field simple equality.

    When a model field is tested for equality with a value, it should
    return a filter query.
    """
    field = model_field_generator()
    value = faker.word()
    expected = FilterQuery(field, FilterOperation.EQUALS, value)

    result = field == expected.second_value

    assert result == expected


def test_model_field_value_inequality(
    faker, model_field_generator, random_query
):
    """
    Test model field simple inequality.

    When a model field is tested for inequality with a value, it should
    return a filter query.
    """
    field = model_field_generator()
    value = faker.word()
    expected = FilterQuery(field, FilterOperation.NOT_EQUALS, value)

    result = field != expected.second_value

    assert result == expected


def test_filter_query_conjunction(faker, model_field_generator, random_query):
    """
    Test conjuntion between two filter queries.

    When two filter queries are tested for conjunction, it should return a new
    filter query for it.
    """
    query1, query2 = random_query(), random_query()

    expected = FilterQuery(query1, FilterOperation.AND, query2)

    result = query1 & query2

    assert result == expected


def test_filter_query_disjunction(faker, model_field_generator, random_query):
    """
    Test disjunction between two filter queries.

    When two filter queries are tested for disjunction, it should return a new
    filter query for it.
    """
    query1, query2 = random_query(), random_query()

    expected = FilterQuery(query1, FilterOperation.OR, query2)

    result = query1 | query2

    assert result == expected


def test_filter_query_inversion(faker, model_field_generator, random_query):
    """
    Test inversion of a filter query.

    If a filter query is inverted, it should return a new filter query for it.
    """
    query = random_query()

    expected = FilterQuery(query, FilterOperation.NOT)

    result = ~query

    assert result == expected
