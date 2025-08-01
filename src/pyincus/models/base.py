"""Base Metaclass and Class for be subclassed by other models."""

from ..config import Unset
from ..exceptions import PyIncusException
from .fields import ModelField


class BaseIncusMeta(type):
    """
    Metaclass for Incus Models.

    Uses ModelField as default for classes and generates __init__ for
    the models based on the annotations.
    """

    def __new__(cls, name, bases, attrs):
        """
        Instantiate the incus model.

        Uses the ModelField as default value for class for all annotations.
        """
        new_class_model_fields = {}
        methods = []
        secret_attributes = []
        for item in attrs.items():
            attr, value = item

            if callable(value) or isinstance(value, property):
                methods.append(item)
            elif attr.startswith('_'):
                secret_attributes.append(item)
            else:
                new_class_model_fields |= (item,)

        model_fields = []
        for attr in attrs.get('__annotations__', {}):
            if attr.startswith('_'):
                continue
            model_fields.append((attr, ModelField(cls, attr)))
            new_class_model_fields.setdefault(attr, Unset)

        new_class = type(
            name, bases, dict((*secret_attributes, *methods, *model_fields))
        )
        new_class.__init__ = cls._init
        if '__post_init__' not in vars(new_class):
            new_class.__post_init__ = cls._post_init
        new_class._model_fields = new_class_model_fields
        return new_class

    def _init(self, **kwargs):
        """
        Initialize the incus model.

        Initialize the class with the required fields in the annotations.
        """
        kwargs = self._model_fields | kwargs
        unsets = []
        for field, value in kwargs.items():
            if field not in self._model_fields:
                continue
            if value is Unset:
                unsets.append(field)
            elif not unsets:
                setattr(self, field, value)

        if unsets:
            raise PyIncusException(
                f'The required fields {unsets} are missing.'
            )

        self.__post_init__(**kwargs)

    def _post_init(self, **kwargs):
        """Will be called after the initialization."""


def incus_model(cls: type):
    """Apply BaseIncusMeta to class."""
    return BaseIncusMeta(cls.__name__, tuple(cls.mro()), vars(cls))
