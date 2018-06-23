from django.test import override_settings

from apputils.maintenance import warning_classes
from apputils.tests.base import AppSettingTestCase
from apputils.tests.conf import defaults


class TestDeprecatedSetting(AppSettingTestCase):

    def test_referencing_setting_on_settings_module_raises_warning(self):
        expected_message = (
            "The DEPRECATED_SETTING app setting is deprecated. You may "
            "want to check the latest release notes for more information."
        )
        with self.assertWarns(DeprecationWarning, msg=expected_message):
            self.assertEqual(
                self.appsettingshelper.DEPRECATED_SETTING,
                defaults.DEPRECATED_SETTING,
            )


class TestRenamedSetting(AppSettingTestCase):

    def test_referencing_old_setting_on_settings_module_raises_warning(self):
        expected_message = (
            "The RENAMED_SETTING_OLD app setting has been renamed to "
            "RENAMED_SETTING_NEW. You should update your code to reference "
            "this new setting instead."
        )
        with self.assertWarns(
            warning_classes.removed_in_next_version_warning,
            msg=expected_message
        ):
            self.assertEqual(
                self.appsettingshelper.RENAMED_SETTING_OLD,
                defaults.RENAMED_SETTING_OLD,
            )

    @override_settings(APPUTILS_TESTS_RENAMED_SETTING_OLD='ooolaalaa')
    def test_user_defined_setting_with_old_name_still_used_when_new_setting_referenced(self):
        expected_message = (
            "The APPUTILS_TESTS_RENAMED_SETTING_OLD setting has been renamed "
            "to APPUTILS_TESTS_RENAMED_SETTING_NEW. Please update your "
            "project's Django settings to use this new name instead, or your "
            "override will fail to work in future versions."
        )
        with self.assertWarns(
            warning_classes.removed_in_next_version_warning,
            msg=expected_message
        ):
            self.assertEqual(
                self.appsettingshelper.RENAMED_SETTING_NEW,
                'ooolaalaa'
            )


class TestReplaceedSetting(AppSettingTestCase):

    def test_referencing_old_setting_on_settings_module_raises_warning(self):
        expected_message = (
            "The REPLACED_SETTING_OLD app setting is deprecated in favour of "
            "using REPLACED_SETTING_NEW. You should update your code to "
            "reference this new setting instead. However, we would recommend "
            "looking at the release notes for more information beforehand."
        )
        with self.assertWarns(
            warning_classes.removed_in_following_version_warning,
            msg=expected_message
        ):
            self.assertEqual(
                self.appsettingshelper.REPLACED_SETTING_OLD,
                defaults.REPLACED_SETTING_OLD,
            )

    @override_settings(APPUTILS_TESTS_REPLACED_SETTING_OLD='ooolaalaa')
    def test_user_defined_setting_with_old_name_still_used_when_new_setting_referenced(self):
        expected_message = (
            "The APPUTILS_TESTS_REPLACED_SETTING_OLD setting has been renamed "
            "to APPUTILS_TESTS_REPLACED_SETTING_NEW. Please update your "
            "project's Django settings to use this new name instead, or your "
            "override will fail to work in future versions."
        )
        with self.assertWarns(
            warning_classes.removed_in_following_version_warning,
            msg=expected_message
        ):
            self.assertEqual(
                self.appsettingshelper.REPLACED_SETTING_NEW,
                'ooolaalaa'
            )
