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


class SettingValueNotImportable(ImportError, SettingValueError):
    """The value of a setting is the correct type, and correctly formatted,
    but the specified model, module or object could not be imported.
    """
    pass


class DefaultSettingValueError:
    """Used as a mixin for exception classes that concern a 'default' setting
    value specifically (i.e. one provided by the app maintainer)."""
    pass


class InvalidDefaultValueType(DefaultSettingValueError, InvalidSettingValueType):
    """As InvalidSettingValueType, but specifically for a 'default' value."""
    pass


class InvalidDefaultValueFormat(DefaultSettingValueError, InvalidSettingValueFormat):
    """As InvalidSettingValueFormat, but specifically for a default value."""
    pass


class DefaultValueNotImportable(DefaultSettingValueError, SettingValueNotImportable):
    """As SettingValueNotImportable, but specifically for a default value."""
    pass
