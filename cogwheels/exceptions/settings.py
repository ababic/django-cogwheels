from django.core.exceptions import ImproperlyConfigured

"""
Errors relating to a specific setting value
"""


# -----------------------------------------------------------------------------
# Common setting value errors
# -----------------------------------------------------------------------------

class SettingValueError(ImproperlyConfigured, ValueError):
    """There is a problem with a setting value."""
    pass


class SettingValueTypeInvalid(SettingValueError):
    """The value of a setting is not the correct type."""
    pass


class SettingValueFormatInvalid(SettingValueError):
    """The value of a setting is the correct type, but is incorrectly
    formatted."""
    pass


class SettingValueNotImportable(ImportError, SettingValueError):
    """The value of a setting is the correct type, and correctly formatted,
    but the specified model, module or object could not be imported.
    """
    pass

# -----------------------------------------------------------------------------
# Errors relating to 'default' values (intended for app developers)
# -----------------------------------------------------------------------------


class DefaultValueError:
    """Used as a mixin for exception classes that concern a 'default' setting
    value specifically (i.e. one provided by the app maintainer)."""
    pass


class DefaultValueTypeInvalid(DefaultValueError, SettingValueTypeInvalid):
    """As SettingValueTypeInvalid, but specifically for a 'default' value."""
    pass


class DefaultValueFormatInvalid(DefaultValueError, SettingValueFormatInvalid):
    """As SettingValueFormatInvalid, but specifically for a default value."""
    pass


class DefaultValueNotImportable(DefaultValueError, SettingValueNotImportable):
    """As SettingValueNotImportable, but specifically for a default value."""
    pass


# -----------------------------------------------------------------------------
# Errors relating to 'override' values (intended for app users)
# -----------------------------------------------------------------------------


class OverrideValueError:
    """Used as a mixin for exception classes that concern a 'user-provided'
    setting value specifically (i.e. added to a project's Django's settings to
    override a 'default' value)."""
    pass


class OverrideValueTypeInvalid(OverrideValueError, SettingValueTypeInvalid):
    """As SettingValueTypeInvalid, but specifically for a 'user-provided' value."""
    pass


class OverrideValueFormatInvalid(OverrideValueError, SettingValueFormatInvalid):
    """As SettingValueFormatInvalid, but specifically for a 'user-provided' value."""
    pass


class OverrideValueNotImportable(OverrideValueError, SettingValueNotImportable):
    """As SettingValueNotImportable, but specifically for a 'user-provided' value."""
    pass
