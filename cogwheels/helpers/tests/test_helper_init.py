from django.core.exceptions import ImproperlyConfigured
from django.test import TestCase

from cogwheels.helpers import BaseAppSettingsHelper, DeprecatedAppSetting


class TestSettingsHelper(BaseAppSettingsHelper):
    defaults_path = 'cogwheels.tests.conf.defaults'
    prefix = 'TEST_'
    deprecations = ()


class TestHelperInit(TestCase):

    def test_providing_prefix_overrides_the_class_attribute_value(self):
        test_val = 'ABRACADABRA_'
        self.assertIs(
            TestSettingsHelper(prefix=test_val)._prefix,
            test_val
        )

    def test_providing_defaults_path_overrides_the_class_attribute_value(self):
        test_val = 'cogwheels'
        self.assertIs(
            TestSettingsHelper(defaults_path=test_val)._defaults_path,
            test_val
        )

    def test_providing_deprecations_overrides_the_class_attribute_value(self):
        test_val = (
            DeprecatedAppSetting('STRING_SETTING'),
        )
        self.assertIs(
            TestSettingsHelper(deprecations=test_val)._deprecations,
            test_val
        )


class TestHelperInitErrors(TestCase):

    def test_errors_if_defaults_path_is_invalid(self):
        with self.assertRaises(ImportError):
            TestSettingsHelper(defaults_path='invalid.module.path')

    def test_errors_if_deprecations_not_list_or_tuple(self):
        message_expected = (
            "'deprecations' must be a list or tuple, not a dict."
        )
        with self.assertRaisesRegex(ImproperlyConfigured, message_expected):
            TestSettingsHelper(deprecations={})

    def test_errors_no_default_value_found_for_a_deprecatedappsetting(self):
        message_expected = (
            "There is an issue with one of your setting deprecation "
            "definitions. 'NON_EXISTENT_SETTING' could not be found in "
            "cogwheels.tests.conf.defaults. Please ensure a default "
            "value remains there until the end of the setting's deprecation "
            "period."
        )
        with self.assertRaisesRegex(ImproperlyConfigured, message_expected):
            TestSettingsHelper(deprecations=(
                DeprecatedAppSetting('NON_EXISTENT_SETTING'),
            ))

    def test_errors_if_invalid_replacement_setting_value_used_for_a_deprecatedappsetting(self):
        message_expected = (
            "There is an issue with one of your settings deprecation "
            "definitions. 'NON_EXISTENT_SETTING' is not a valid replacement "
            "for 'DEPRECATED_SETTING', as no such value can be found in "
            "cogwheels.tests.conf.defaults."
        )
        with self.assertRaisesRegex(ImproperlyConfigured, message_expected):
            TestSettingsHelper(deprecations=(
                DeprecatedAppSetting(
                    'DEPRECATED_SETTING', renamed_to="NON_EXISTENT_SETTING"
                ),
            ))
