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
            additional_guidance=(
                "The new setting offers much greater flexibility, whilst also "
                "allowing developers to change X without changing Z. Check "
                "out the version X.X release notes for further details: "
                "https://your-django-project.readthedocs.io/en/latest/releases/X.X.html"
            )
        ),
        DeprecatedAppSetting(
            'REPLACED_SETTING_ONE',
            replaced_by='REPLACES_MULTIPLE',
        ),
        DeprecatedAppSetting(
            'REPLACED_SETTING_TWO',
            replaced_by='REPLACES_MULTIPLE',
        ),
        DeprecatedAppSetting(
            'REPLACED_SETTING_THREE',
            replaced_by='REPLACES_MULTIPLE',
        ),
    )


sys.modules[__name__] = TestAppSettingsHelper()
