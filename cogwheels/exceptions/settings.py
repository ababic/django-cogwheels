from django.core.exceptions import ImproperlyConfigured

# -----------------------------------------------------------------------------
# Errors relating to a specific setting value
# -----------------------------------------------------------------------------


class SettingValueError(ImproperlyConfigured, ValueError):
    """There is a problem with a setting value."""
    pass


class SettingValueTypeError(SettingValueError):
    """The value of a setting is not the correct type."""
    pass


class SettingValueFormatError(SettingValueError):
    """The value of a setting is the correct type, but is incorrectly
    formatted."""
    pass


class SettingValueImportError(SettingValueError):
    """The value of a setting is the correct type, and correctly formatted,
    but the specified model, module or object could not be imported.
    """
    pass


class DefaultSettingValueMixin:
    """Used as a mixin for exception classes that concern a 'default' setting
    value specifically (i.e. one provided by the app maintainer)."""
    pass


class DefaultSettingValueTypeError(DefaultSettingValueMixin, SettingValueTypeError):
    """As SettingValueTypeError, but specifically for a 'default' value."""
    pass


class DefaultSettingValueFormatError(DefaultSettingValueMixin, SettingValueFormatError):
    """As SettingValueFormatError, but specifically for a default value."""
    pass


class DefaultSettingValueImportError(DefaultSettingValueMixin, SettingValueImportError):
    """As SettingValueImportError, but specifically for a default value."""
    pass
