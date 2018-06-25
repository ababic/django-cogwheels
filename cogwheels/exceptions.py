from django.core.exceptions import ImproperlyConfigured


class DeprecationsValueError(ImproperlyConfigured):
    """There is a problem with a settings helper's 'deprecations' value."""
    pass


class InvalidDeprecationDefinitionError(DeprecationsValueError):
    """There is a problem with a one or more AppSettingDeprecation definitions
    in a settings helper's 'deprecations' value."""
    pass


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


class DefaultSettingValueError(SettingValueError):
    """As SettingValueError, but specifically for a default setting value."""
    pass


class DefaultSettingValueTypeError(DefaultSettingValueError, SettingValueTypeError):
    """As SettingValueTypeError, but specifically for a default setting value.
    """
    pass


class DefaultSettingValueFormatError(DefaultSettingValueError, SettingValueFormatError):
    """As SettingValueFormatError, but specifically for a default setting
    value."""
    pass


class DefaultSettingValueImportError(DefaultSettingValueError, SettingValueImportError):
    """As SettingValueImportError, but specifically for a default setting
    value."""
    pass
