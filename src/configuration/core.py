from typing import Any, Callable, Tuple

class ConfigurationRule:
    def __init__(self, description: str, predicate: Callable[[Any], bool]):
        self._predicate = predicate

        self.description = description
        self.name = None

    def __set_name__(self, owner, name):
        self.name = name

    def __call__(self, value: Any) -> bool:
        return self._predicate(value)


class ConfigurationField:
    """
    Represents a configuration file field
    """

    def __init__(self, dtype: type, rules: Tuple[ConfigurationRule, ...] | ConfigurationRule | None = None,
                 default: Any = None, is_optional: bool = False):
        """
        :param dtype: value must match this data type
        :param rules: rules to apply to the value
        :param default: default value
        :param is_optional: True if the field is optional
        """
        self._dtype = dtype
        self.is_optional = is_optional
        self.name = None

        if rules is None:
            normalized_rules = ()
        elif isinstance(rules, tuple):
            normalized_rules = rules
        else:
            normalized_rules = (rules,)

        for rule in normalized_rules:
            if not isinstance(rule, ConfigurationRule):
                raise TypeError(
                    f"Configuration rule must be '{ConfigurationRule.__name__}' but got '{rule.__class__.__name__}'")
        self._rules = normalized_rules

        if default is not None:
            if not isinstance(default, dtype):
                raise TypeError(f"Default value must be '{dtype.__name__}' but got '{type(default).__name__}'")

            for rule in self._rules:
                if not rule(default):
                    raise ValueError(f"Invalid default value '{default}' - {rule.description} ({rule.name})")

        self.default = default

    def __set_name__(self, _, name):
        """
        Descriptor helper that sets the name of this field
        :param name: name of the field
        """
        self.name = name

    def __get__(self, instance, _):
        """
        Retrieves the value for the field
        :param instance: instance of configuration class
        :return: saved value of the field otherwise default or None
        """
        if instance is None: return self
        return instance.__dict__.get(self.name, self.default)

    def __set__(self, instance, value):
        """
        Sets the value for the field
        :param instance: instance of configuration class
        :param value: value to set, must match data type and fulfill rules
        """

        if not isinstance(value, self._dtype):
            raise TypeError(f"'{self.name}' must be {self._dtype.__name__}")

        if self._rules:
            for rule in self._rules:
                if not rule(value):
                    raise ValueError(f"Invalid value '{value}' - {rule.description} ({rule.name})")

        instance.__dict__[self.name] = value


def configuration(cls):
    """
    Decorator to register configuration class.
    :param cls: class that represents configuration
    :return: cls with updated constructor
    """
    configuration_fields = {k: v for k, v in cls.__dict__.items() if isinstance(v, ConfigurationField)}

    def __init__(self, **kwargs):
        for k in kwargs:
            if k not in configuration_fields:
                raise ValueError(f"Unknown field '{k}' found")

        for field in configuration_fields.values():
            if not field.is_optional and not field.default and field.name not in kwargs:
                raise ValueError(f"Required field '{field.name}' is missing and has no default values.")
            else:
                setattr(self, field.name, kwargs.get(field.name, field.default))

    cls.__init__ = __init__
    return cls