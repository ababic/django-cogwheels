from django.core.exceptions import ImproperlyConfigured

# -----------------------------------------------------------------------------
# Errors relating to a settings heleper's 'deprecation' value
# -----------------------------------------------------------------------------


class DeprecationsValueError(ImproperlyConfigured):
    """There is a problem with a settings helper's 'deprecations' value."""
    pass


class InvalidDeprecationDefinitionError(DeprecationsValueError):
    """There is a problem with a one or more AppSettingDeprecation definitions
    in a settings helper's 'deprecations' list."""
    pass


class DuplicateDeprecationError(InvalidDeprecationDefinitionError):
    """The same setting name has been used for more than one
    AppSettingDeprecation definitions in a setting helper's 'deprecations' "
    "list."""
    pass


class DuplicateReplacementDeprecationError(InvalidDeprecationDefinitionError):
    """The same replacement setting name has been used for more than one
    AppSettingDeprecation definition in a setting helper's 'deprecations' "
    "list."""
    pass
