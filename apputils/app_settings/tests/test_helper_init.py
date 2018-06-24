from django.core.exceptions import ImproperlyConfigured
from django.test import TestCase

from apputils.app_settings import BaseAppSettingsHelper, DeprecatedAppSetting


class TestSettingsHelper(BaseAppSettingsHelper):
    defaults_path = 'apputils.tests.conf.defaults'
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
        test_val = 'apputils'
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
