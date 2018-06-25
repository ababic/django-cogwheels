import sys

from cogwheels import BaseAppSettingsHelper, DeprecatedAppSetting


class TestAppSettingsHelper(BaseAppSettingsHelper):
    deprecations = (
        DeprecatedAppSetting('DEPRECATED_SETTING'),
        DeprecatedAppSetting(
            'RENAMED_SETTING_OLD',
            renamed_to='RENAMED_SETTING_NEW',
            warning_category=DeprecationWarning,
        ),
        DeprecatedAppSetting(
            'REPLACED_SETTING_OLD',
            replaced_by='REPLACED_SETTING_NEW',
            warning_category=PendingDeprecationWarning,
        ),
    )


sys.modules[__name__] = TestAppSettingsHelper()
