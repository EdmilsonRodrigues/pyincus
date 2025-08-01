"""Test Base Metaclass and class."""

import asyncio

import pytest

from pyincus.models.base import ModelField, PyIncusException, incus_model


@pytest.fixture
def test_value_int(faker):  # noqa: D103
    return faker.pyint()


@pytest.fixture
def test_value_string_1(faker):  # noqa: D103
    return faker.word()


@pytest.fixture
def test_value_string_2(faker):  # noqa: D103
    return faker.word()


@pytest.fixture
def test_value_string_3(faker):  # noqa: D103
    return faker.word()


@pytest.fixture
def AttributeTestClass(  # noqa: D103
    test_value_string_1, test_value_string_2, test_value_string_3
):
    @incus_model
    class TestClass:
        a: int  # type: ignore
        b: str = test_value_string_1  # type: ignore
        _c: int  # type: ignore
        _d: str = test_value_string_2  # type: ignore

        @property
        def e(self):
            return test_value_string_3

    return TestClass


def test_incus_model_attributes_default_to_model_field(
    AttributeTestClass, test_value_int, test_value_string_2
):
    """
    Test if an Incus Model public attributes will be turned into ModelField.

    If the attribute is public, it must be turned into a ModelField.
    If it is a private or protected attribute, it will not be changed.
    If it has a default value, it must continue having.
    If it is a property, it should not be changed.
    """
    assert isinstance(AttributeTestClass.a, ModelField)
    assert isinstance(AttributeTestClass.b, ModelField)
    assert AttributeTestClass.a.field_name == 'a'
    assert AttributeTestClass.b.field_name == 'b'
    assert AttributeTestClass._d == test_value_string_2


def test_incus_model_instance_attributes_set_by_constructor(  # noqa: PLR0913, PLR0917
    faker,
    AttributeTestClass,
    test_value_int,
    test_value_string_1,
    test_value_string_2,
    test_value_string_3,
):
    """
    Test if an Incus Model attributes will be set when instantiating.

    Public Attributes should be set on instantiation.
    Private Attributes should not be set on instantiaion.
    New attributes will not be set on instantiation.
    Default values must remain.
    """
    test_instance = AttributeTestClass(
        a=test_value_int,
        _c=faker.word(),
        _d=faker.word(),
        f=faker.pyint(),
        e=faker.word(),
    )
    assert test_instance.a == test_value_int
    assert test_instance.b == test_value_string_1
    assert test_instance._d == test_value_string_2
    assert test_instance.e == test_value_string_3
    assert not hasattr(test_instance, 'f')
    assert not hasattr(test_instance, '_c')


def test_incus_model_required_attributes_must_be_set(AttributeTestClass):
    """Test if an exception is raised when requireds attributes are not set."""
    with pytest.raises(PyIncusException):
        AttributeTestClass()


def test_incus_model_attributes_with_default_values_are_overwritten(
    AttributeTestClass, test_value_string_3
):
    """
    Test overwriting Incus Model instances attributes with default values.

    Incus Model instances with default attributes will be overwritten if
    passed in instantiation.
    """
    test_instance = AttributeTestClass(
        a=test_value_string_3, b=test_value_string_3
    )

    assert test_instance.b == test_value_string_3


def test_incus_model_methods_are_set(faker):
    """Test if an Incus Model has working methods."""

    def test_func_(self):
        return RETURN_FUNC

    @incus_model
    class TestClass:
        def test_func_a(self, a: int) -> int:  # noqa: PLR6301
            """Synchronous function with annotations."""
            return a

        test_func = test_func_

        async def test_func_b(self, b):  # noqa: PLR6301
            """Asynchronous function without annotations."""
            return b

    test_instance = TestClass()
    RETURN_FUNC = faker.pyint()

    assert test_instance.test_func_a(RETURN_FUNC) == RETURN_FUNC
    assert test_instance.test_func() == RETURN_FUNC
    assert (
        asyncio.new_event_loop().run_until_complete(
            test_instance.test_func_b(RETURN_FUNC)
        )
        == RETURN_FUNC
    )


def test_post_init(faker):
    """
    Test if __post_init__ is called.

    After the auto-generated __init__, the incus model should run the
    method __post_init__, with signature: __post_init__(self, **kwargs)
    with kwargs being the attributes passed when instantiating the object.
    """
    post_value = faker.pyint()
    post_salt = faker.pyint()
    pre_value = faker.pyint()

    @incus_model
    class TestClass:
        a: int
        _b: int

        def __post_init__(self, **kwargs):
            """Add salt to values."""
            self.a += post_salt
            self._b = kwargs.get('_b', 0)
            self._b += post_salt

    # Assert post init is run always
    test_instance = TestClass(a=pre_value, _b=post_value)
    assert test_instance.a == pre_value + post_salt
    assert test_instance._b == post_value + post_salt
