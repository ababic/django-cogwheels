from django.core.exceptions import ImproperlyConfigured

# -----------------------------------------------------------------------------
# Errors relating to a specific setting value
# -----------------------------------------------------------------------------


class SettingValueError(ImproperlyConfigured, ValueError):
    """There is a problem with a setting value."""
    pass


class InvalidSettingValueType(SettingValueError):
    """The value of a setting is not the correct type."""
    pass


class InvalidSettingValueFormat(SettingValueError):
    """The value of a setting is the correct type, but is incorrectly
    formatted."""
    pass


class UnimportableSettingValue(SettingValueError):
    """The value of a setting is the correct type, and correctly formatted,
    but the specified model, module or object could not be imported.
    """
    pass


class DefaultSettingValueMixin:
    """Used as a mixin for exception classes that concern a 'default' setting
    value specifically (i.e. one provided by the app maintainer)."""
    pass


class InvalidDefaultSettingValueType(DefaultSettingValueMixin, InvalidSettingValueType):
    """As InvalidSettingValueType, but specifically for a 'default' value."""
    pass


class InvalidDefaultSettingValueFormat(DefaultSettingValueMixin, InvalidSettingValueFormat):
    """As InvalidSettingValueFormat, but specifically for a default value."""
    pass


class UnimportableDefaultSettingValue(DefaultSettingValueMixin, UnimportableSettingValue):
    """As UnimportableSettingValue, but specifically for a default value."""
    pass
