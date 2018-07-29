import warnings
from unittest.mock import patch

from django.test import override_settings

from cogwheels.helpers import BaseAppSettingsHelper
from cogwheels.tests.base import AppSettingTestCase
from cogwheels.tests.conf import defaults


class TestDeprecatedSetting(AppSettingTestCase):

    def test_referencing_attribute_on_settings_helper_raises_warning(self):
        with self.assertWarns(DeprecationWarning) as cm:
            self.assertEqual(
                self.appsettingshelper.DEPRECATED_SETTING,
                defaults.DEPRECATED_SETTING,
            )
        self.assertEqual(
            "The DEPRECATED_SETTING settings helper attribute is deprecated. Please remove any "
            "references to 'settings.DEPRECATED_SETTING' from your project, as this will raise an "
            "AttributeError after support is removed in the next version.",
            str(cm.warning)
        )


class TestRenamedSetting(AppSettingTestCase):

    def test_referencing_old_setting_on_settings_module_raises_warning(self):
        with self.assertWarns(DeprecationWarning) as cm:
            self.assertEqual(
                self.appsettingshelper.RENAMED_SETTING_OLD,
                defaults.RENAMED_SETTING_OLD,
            )
        self.assertEqual(
            "The RENAMED_SETTING_OLD settings helper attribute has been renamed to "
            "RENAMED_SETTING_NEW. Please update your code to reference "
            "'settings.RENAMED_SETTING_NEW' instead, as continuing to reference "
            "'settings.RENAMED_SETTING_OLD' will raise an AttributeError after support is removed "
            "in the next version.",
            str(cm.warning)
        )

    @override_settings(COGWHEELS_TESTS_RENAMED_SETTING_OLD='ooolaalaa')
    def test_user_defined_setting_with_old_name_still_used_when_new_setting_referenced(self):
        with self.assertWarns(DeprecationWarning) as cm:
            self.assertEqual(
                self.appsettingshelper.RENAMED_SETTING_NEW,
                'ooolaalaa'
            )
        self.assertEqual(
            "The COGWHEELS_TESTS_RENAMED_SETTING_OLD setting has been renamed to "
            "COGWHEELS_TESTS_RENAMED_SETTING_NEW. Please update your Django settings to use the "
            "new setting, otherwise the app will revert to its default behaviour in the next "
            "version (when support for COGWHEELS_TESTS_RENAMED_SETTING_OLD will be removed "
            "entirely).",
            str(cm.warning)
        )


class TestReplacedSetting(AppSettingTestCase):

    def test_referencing_old_setting_on_settings_module_raises_warning(self):
        with self.assertWarns(PendingDeprecationWarning) as cm:
            self.assertEqual(
                self.appsettingshelper.REPLACED_SETTING_OLD,
                defaults.REPLACED_SETTING_OLD,
            )
        message = str(cm.warning)
        self.assertIn(
            "The REPLACED_SETTING_OLD settings helper attribute is deprecated in favour of using "
            "REPLACED_SETTING_NEW. Please update your code to reference "
            "'settings.REPLACED_SETTING_NEW' instead, as continuing to reference "
            "'settings.REPLACED_SETTING_OLD' will raise an AttributeError after support is removed "
            "in two versions time.",
            message
        )
        self.assertIn(
            self.appsettingshelper.deprecations[2].additional_guidance,
            message
        )

    @override_settings(COGWHEELS_TESTS_REPLACED_SETTING_OLD='ooolaalaa')
    def test_user_defined_setting_with_old_name_still_used_when_new_setting_referenced(self):
        with self.assertWarns(PendingDeprecationWarning) as cm:
            self.assertEqual(
                self.appsettingshelper.REPLACED_SETTING_NEW,
                'ooolaalaa'
            )
        message = str(cm.warning)
        self.assertIn(
            "The COGWHEELS_TESTS_REPLACED_SETTING_OLD setting is deprecated in favour of using "
            "COGWHEELS_TESTS_REPLACED_SETTING_NEW. Please update your Django settings to use the "
            "new setting, otherwise the app will revert to its default behaviour in two versions "
            "time (when support for COGWHEELS_TESTS_REPLACED_SETTING_OLD will be removed "
            "entirely)",
            message
        )
        self.assertIn(
            self.appsettingshelper.deprecations[2].additional_guidance,
            message
        )


@override_settings(
    COGWHEELS_TESTS_REPLACED_SETTING_ONE='overridden-one',
    COGWHEELS_TESTS_REPLACED_SETTING_TWO='overridden-two',
)
class TestMultipleReplacementSetting(AppSettingTestCase):

    def test_referencing_each_old_setting_on_settings_module_raises_warning(self):
        for deprecated_setting_name in (
            'REPLACED_SETTING_ONE', 'REPLACED_SETTING_TWO', 'REPLACED_SETTING_THREE'
        ):
            with self.assertWarns(DeprecationWarning):
                getattr(self.appsettingshelper, deprecated_setting_name)

    def test_user_defined_setting_with_old_name_is_only_used_if_its_name_matches_accept_deprecated(self):
        # REPLACES_MULTIPLE should return the value from defaults, because a user could be overriding
        # any one of the deprecated settings being replaced, and because we have no idea which to
        # prioritize over the other, picking one could yield unpredictable results.
        self.assertIs(
            self.appsettingshelper.get('REPLACES_MULTIPLE'), defaults.REPLACES_MULTIPLE
        )
        # Instead, developers can specify which deprecated setting in particular they are willing to
        # use a value from, and override values for those settings will be returned.
        with self.assertWarns(DeprecationWarning):
            self.assertEqual(
                self.appsettingshelper.get('REPLACES_MULTIPLE', accept_deprecated='REPLACED_SETTING_ONE'),
                'overridden-one'
            )

        with self.assertWarns(DeprecationWarning):
            self.assertEqual(
                self.appsettingshelper.get('REPLACES_MULTIPLE', accept_deprecated='REPLACED_SETTING_TWO'),
                'overridden-two'
            )
        # But the the default value will still be returned if the specified deprecated setting has
        # not been overridden
        self.assertIs(
            self.appsettingshelper.get('REPLACES_MULTIPLE', accept_deprecated='REPLACED_SETTING_THREE'),
            defaults.REPLACES_MULTIPLE
        )


@override_settings(COGWHEELS_TESTS_REPLACED_SETTING_OLD='somevalue')
class TestSuppressWarnings(AppSettingTestCase):

    def test_warning_raised_by_default(self):
        with warnings.catch_warnings(record=True) as w:
            warnings.simplefilter("always")
            self.appsettingshelper._get_raw_value('REPLACED_SETTING_OLD')
            self.assertEqual(len(w), 1)
            self.appsettingshelper._get_raw_value('REPLACED_SETTING_NEW')
            self.assertEqual(len(w), 2)

    def test_no_warnings_raised_by_get_raw_value_when_suppress_warnings_is_true(self):
        with warnings.catch_warnings(record=True) as w:
            warnings.simplefilter("always")
            self.appsettingshelper._get_raw_value('REPLACED_SETTING_OLD', suppress_warnings=True)
            self.appsettingshelper._get_raw_value('REPLACED_SETTING_NEW', suppress_warnings=True)
            self.assertEqual(len(w), 0)

    @patch.object(BaseAppSettingsHelper, '_get_raw_value', return_value="")
    def test_suppress_warnings_is_passed_on_to_get_raw_value_by_get(self, mocked_method):
        self.appsettingshelper.get('DEPRECATED_SETTING', suppress_warnings=True)
        self.assertIs(mocked_method.call_args[1]['suppress_warnings'], True)

    @patch.object(BaseAppSettingsHelper, '_get_raw_value', return_value=defaults.VALID_MODEL)
    def test_suppress_warnings_is_passed_on_to_get_raw_value_by_get_model(self, mocked_method):
        self.appsettingshelper.get_model('DEPRECATED_SETTING', suppress_warnings=True)
        self.assertIs(mocked_method.call_args[1]['suppress_warnings'], True)

    @patch.object(BaseAppSettingsHelper, '_get_raw_value', return_value=defaults.VALID_MODULE)
    def test_suppress_warnings_is_passed_on_to_get_raw_value_by_get_module(self, mocked_method):
        self.appsettingshelper.get_module('DEPRECATED_SETTING', suppress_warnings=True)
        self.assertIs(mocked_method.call_args[1]['suppress_warnings'], True)

    @patch.object(BaseAppSettingsHelper, '_get_raw_value', return_value=defaults.VALID_OBJECT)
    def test_suppress_warnings_is_passed_on_to_get_raw_value_by_get_object(self, mocked_method):
        self.appsettingshelper.get_object('DEPRECATED_SETTING', suppress_warnings=True)
        self.assertIs(mocked_method.call_args[1]['suppress_warnings'], True)
