import sys
from apputils.app_settings import BaseAppSettingsHelper, DeprecatedAppSetting
from apputils.maintenance import warning_classes


class TestAppSettingsHelper(BaseAppSettingsHelper):
    prefix = 'TEST_'
    defaults_path = 'apputils.tests.conf.defaults'
    deprecations = (
        DeprecatedAppSetting('DEPRECATED_SETTING'),
        DeprecatedAppSetting(
            'RENAMED_SETTING',
            renamed_to='RENAMED_TO_SETTING',
            warning_category=warning_classes.removed_in_next_version_warning,
        ),
        DeprecatedAppSetting(
            'REPLACED_SETTING',
            replaced_by='REPLACED_WITH_SETTING',
            warning_category=warning_classes.removed_in_following_version_warning,
        ),
    )


sys.modules[__name__] = TestAppSettingsHelper()
