import warnings


COMMON_ATTRIBUTE_WARNING_FORMAT = (
    "Please update your code to reference 'settings.{replacement_name}' "
    "instead, as continuing to reference 'settings.{setting_name}' will raise "
    "an AttributeError after support is removed in {removed_in_version}."
)
RENAMED_ATTRIBUTE_WARNING_FORMAT = (
    "The {setting_name} settings helper attribute has been renamed to "
    "{replacement_name}. "
) + COMMON_ATTRIBUTE_WARNING_FORMAT

REPLACED_ATTRIBUTE_WARNING_FORMAT = (
    "The {setting_name} settings helper attribute is deprecated in favour "
    "of using {replacement_name}. "
) + COMMON_ATTRIBUTE_WARNING_FORMAT

SIMPLE_DEPRECATION_WARNING_FORMAT = (
    "The {setting_name} settings helper attribute is deprecated. Please "
    "remove any references to 'settings.{setting_name}' from your project, as "
    "this will raise an AttributeError after support is removed in "
    "{removed_in_version}."
)

COMMON_OLD_SETTING_USED_WARNING_FORMAT = (
    "Please update your Django settings to use the new setting, otherwise the "
    "app will revert to its default behaviour in {removed_in_version} ("
    "when support for {prefix}_{setting_name} will be removed entirely)."
)

RENAMED_OLD_SETTING_USED_WARNING_FORMAT = (
    "The {prefix}_{setting_name} setting has been renamed to "
    "{prefix}_{replacement_name}. "
) + COMMON_OLD_SETTING_USED_WARNING_FORMAT

REPLACED_OLD_SETTING_USER_WARNING_FORMAT = (
    "The {prefix}_{setting_name} setting is deprecated in favour of using "
    "{prefix}_{replacement_name}. "
) + COMMON_OLD_SETTING_USED_WARNING_FORMAT


class DeprecatedAppSetting:
    """
    An instance of ``DeprecatedAppSetting`` stores details about a deprecated
    app setting, and helps to raise warnings related with that deprecation.
    """
    def __init__(
        self, setting_name, renamed_to=None, replaced_by=None,
        warning_category=None, additional_guidance=None
    ):
        self.setting_name = setting_name
        self.replacement_name = renamed_to or replaced_by
        self.is_renamed = renamed_to is not None
        self.warning_category = warning_category or DeprecationWarning
        self.additional_guidance = additional_guidance
        self._prefix = ''
        self.is_imminent = not issubclass(
            self.warning_category, PendingDeprecationWarning)

    @property
    def prefix(self):
        return self._prefix

    @prefix.setter
    def prefix(self, value):
        self._prefix = value

    def get_removed_in_version_text(self):
        if self.is_imminent:
            return 'the next version'
        return 'two versions time'

    def _make_warning_message(self, message_format):
        if self.additional_guidance:
            message_format += ' ' + self.additional_guidance
        return message_format.format(
            prefix=self.prefix,
            setting_name=self.setting_name,
            replacement_name=self.replacement_name,
            removed_in_version=self.get_removed_in_version_text(),
        )

    def warn_if_setting_attribute_referenced(self, stacklevel=2):
        message_format = SIMPLE_DEPRECATION_WARNING_FORMAT
        if self.replacement_name is not None:
            message_format = REPLACED_ATTRIBUTE_WARNING_FORMAT
            if self.is_renamed:
                message_format = RENAMED_ATTRIBUTE_WARNING_FORMAT
        warnings.warn(
            self._make_warning_message(message_format),
            category=self.warning_category,
            stacklevel=stacklevel,
        )

    def warn_if_user_using_old_setting_name(self, stacklevel=2):
        warnings.warn(
            self._make_warning_message(
                RENAMED_OLD_SETTING_USED_WARNING_FORMAT if self.is_renamed
                else REPLACED_OLD_SETTING_USER_WARNING_FORMAT
            ),
            category=self.warning_category,
            stacklevel=stacklevel,
        )
