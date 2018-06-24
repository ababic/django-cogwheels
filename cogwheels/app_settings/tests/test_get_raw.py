from django.core.exceptions import ImproperlyConfigured
from django.test import override_settings

from cogwheels.tests.base import AppSettingTestCase
from cogwheels.tests.conf import defaults


class TestGetValueMethod(AppSettingTestCase):

    def test_raises_error_if_no_default_defined(self):
        with self.assertRaises(ImproperlyConfigured):
            self.appsettingshelper.get_raw('NOT_REAL_SETTING')

    def test_integer_setting_returns_default_value_by_default(self):
        self.assertEqual(
            self.appsettingshelper.get_raw('INTEGER_SETTING'),
            defaults.INTEGER_SETTING
        )

    @override_settings(COGWHEELS_TESTS_INTEGER_SETTING=1234)
    def test_integer_setting_returns_user_defined_value_if_overridden(self):
        result = self.appsettingshelper.get_raw('INTEGER_SETTING')
        self.assertNotEqual(result, defaults.INTEGER_SETTING)
        self.assertEqual(result, 1234)

    def test_boolean_setting_returns_default_value_by_default(self):
        self.assertIs(
            self.appsettingshelper.get_raw('BOOLEAN_SETTING'),
            defaults.BOOLEAN_SETTING
        )

    @override_settings(COGWHEELS_TESTS_BOOLEAN_SETTING=True)
    def test_boolean_setting_returns_user_defined_value_if_overridden(self):
        result = self.appsettingshelper.get_raw('BOOLEAN_SETTING')
        self.assertNotEqual(result, defaults.BOOLEAN_SETTING)
        self.assertIs(result, True)

    def test_string_setting_returns_default_value_by_default(self):
        self.assertIs(
            self.appsettingshelper.get_raw('STRING_SETTING'),
            defaults.STRING_SETTING
        )

    @override_settings(COGWHEELS_TESTS_STRING_SETTING='abc')
    def test_string_setting_returns_user_defined_value_if_overridden(self):
        result = self.appsettingshelper.get_raw('STRING_SETTING')
        self.assertNotEqual(result, defaults.STRING_SETTING)
        self.assertIs(result, 'abc')

    def test_tuples_setting_returns_default_value_by_default(self):
        self.assertIs(
            self.appsettingshelper.get_raw('TUPLES_SETTING'),
            defaults.TUPLES_SETTING
        )

    @override_settings(COGWHEELS_TESTS_TUPLES_SETTING=())
    def test_tuples_setting_returns_user_defined_value_if_overridden(self):
        result = self.appsettingshelper.get_raw('TUPLES_SETTING')
        self.assertNotEqual(result, defaults.TUPLES_SETTING)
        self.assertIs(result, ())
