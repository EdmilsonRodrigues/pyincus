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


@pytest.mark.parametrize(
    'cls,class_name',
    (
        (object, 'object'),
        (FilterOperation, 'FilterOperation'),
        (ModelField, 'ModelField'),
        (FilterQuery, 'FilterQuery'),
    ),
)
def test_model_field_representation(cls, class_name, faker):
    """
    Test the representation of the ModelField.

    The representation should show the name of the model and the field.
    """
    field_name = faker.word()
    field = ModelField(cls, field_name)
    expected = f'{class_name}.{field_name}'

    result = repr(field)

    assert result == expected


def test_model_field_string(model_field_generator):
    """
    Test the string convertion of the ModelField.

    The string convertion should be only the field_name in order to
    be used in the query.
    """
    field = model_field_generator()
    expected = field.field_name

    result = str(field)

    assert result == expected


@pytest.mark.parametrize(
    'operation,symbol',
    ((FilterOperation.EQUALS, '=='), (FilterOperation.NOT_EQUALS, '!=')),
)
@pytest.mark.parametrize(
    'cls,class_name',
    (
        (object, 'object'),
        (FilterOperation, 'FilterOperation'),
        (ModelField, 'ModelField'),
        (FilterQuery, 'FilterQuery'),
    ),
)
def test_simple_filter_query_representation(
    faker, operation, symbol, cls, class_name
):
    """
    Test the representation of a simple FilterQuery object.

    It should be clear for debugging reasons, having the class that the model
    field is attached, and its field name, the logical operation and the value.
    """
    field_name, field_value = faker.word(), faker.word()
    model_field = ModelField(cls, field_name)
    query = FilterQuery(model_field, operation, field_value)
    expected = f"{class_name}.{field_name} {symbol} '{field_value}'"

    result = repr(query)

    assert result == expected


@pytest.mark.parametrize(
    'operation,symbol',
    ((FilterOperation.AND, 'and'), (FilterOperation.OR, 'or')),
)
def test_nested_filter_query_representation(random_query, operation, symbol):
    """
    Test the representation of a nested FilterQuery object.

    It should be clear for debugging reasons, having the representation
    of both filter_operations and the operator between them.
    """
    query1, query2 = random_query(), random_query()
    query = FilterQuery(query1, operation, query2)
    expected = f'{query1!r} {symbol} {query2!r}'

    result = repr(query)

    assert result == expected


def test_invert_filter_query_representation(random_query):
    """
    Test the representation of an inverted FilterQuery object.

    It should be clear for debugging reasons, in the format `not repr(query)`.
    """
    query = random_query()
    inverted = FilterQuery(query, FilterOperation.NOT)
    expected = f'not {query!r}'

    result = repr(inverted)

    assert result == expected


@pytest.mark.parametrize(
    'operation',
    (FilterOperation.EQUALS, FilterOperation.NOT_EQUALS),
)
def test_simple_filter_query_string(faker, operation):
    """
    Test the string representation of a simple FilterQuery object.

    It should be a string following the query notation for incus,
    in order to query equality or inequality.
    """
    field_name, field_value = faker.word(), faker.word()
    model_field = ModelField(object, field_name)
    query = FilterQuery(model_field, operation, field_value)
    expected = f"{field_name} {operation.value} '{field_value}'"

    result = str(query)

    assert result == expected


@pytest.mark.parametrize(
    'operation',
    (FilterOperation.AND, FilterOperation.OR),
)
def test_nested_filter_query_string(random_query, operation):
    """
    Test the string representation of a nested FilterQuery object.

    It should be a string following the query notation for incus,
    in order to query conjunction or disjunction of queries.
    """
    query1, query2 = random_query(), random_query()
    query = FilterQuery(query1, operation, query2)
    expected = f'{query1} {operation.value} {query2}'

    result = str(query)

    assert result == expected


def test_invert_filter_query_string(random_query):
    """
    Test the string representation of an inverted FilterQuery object.

    It should be a string following the query notation for incus, in the
    format `not query`.
    """
    query = random_query()
    inverted = FilterQuery(query, FilterOperation.NOT)
    expected = f'not {query}'

    result = str(inverted)

    assert result == expected
