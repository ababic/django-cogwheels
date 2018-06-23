import sys
from apputils.app_settings import BaseAppSettingsHelper, DeprecatedAppSetting
from apputils.maintenance import warning_classes


class TestAppSettingsHelper(BaseAppSettingsHelper):
    deprecations = (
        DeprecatedAppSetting('DEPRECATED_SETTING'),
        DeprecatedAppSetting(
            'RENAMED_SETTING_OLD',
            renamed_to='RENAMED_SETTING_NEW',
            warning_category=warning_classes.removed_in_next_version_warning,
        ),
        DeprecatedAppSetting(
            'REPLACED_SETTING_OLD',
            replaced_by='REPLACED_SETTING_NEW',
            warning_category=warning_classes.removed_in_following_version_warning,
        ),
    )


sys.modules[__name__] = TestAppSettingsHelper()
