import warnings
from django.utils.translation import ugettext_lazy as _


class DeprecatedAppSetting:
    """
    An instance of ``DeprecatedAppSetting`` stores details about a deprecated
    app setting, and helps to raise warnings related with that deprecation.
    """
    def __init__(self, setting_name, renamed_to=None, replaced_by=None,
                 warning_category=None):
        self.setting_name = setting_name
        self.replacement_name = renamed_to or replaced_by
        self.is_renamed = renamed_to is not None
        self.warning_category = warning_category or DeprecationWarning
        self._prefix = ''

    @property
    def prefix(self):
        return self._prefix

    @prefix.setter
    def prefix(self, value):
        self._prefix = value

    def warn_if_referenced_directly(self):
        if self.replacement_name is not None:
            if self.is_renamed:
                msg = _(
                    "The {setting_name} app setting has been renamed to "
                    "{replacement_name}. You should update your code to "
                    "reference this new setting instead."
                )
            else:
                msg = _(
                    "The {setting_name} app setting is deprecated in favour "
                    "of using {replacement_name}. You should update your code "
                    "to reference this new setting instead. However, we would "
                    "recommend looking at the release notes for more "
                    "information beforehand."
                )
        else:
            msg = _(
                "The {setting_name} app setting is deprecated. You may want "
                "to check the latest release notes for more information."
            )
        warnings.warn(
            msg.format(
                setting_name=self.setting_name,
                replacement_name=self.replacement_name,
            ),
            category=self.warning_category
        )

    def warn_if_deprecated_value_used_by_replacement(self):
        warnings.warn(_(
            "The {setting_name} setting has been renamed to "
            "{replacement_name}. Please update your project's "
            "Django settings to use this new name instead, or your "
            "override will fail to work in future versions."
        ).format(
            setting_name=self.prefix + self.setting_name,
            replacement_name=self.prefix + self.replacement_name,
        ), category=self.warning_category)
