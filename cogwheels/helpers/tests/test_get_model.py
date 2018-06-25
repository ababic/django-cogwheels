from unittest.mock import patch
from django.test import override_settings

from cogwheels import exceptions
from cogwheels.tests.conf import settings
from cogwheels.tests.base import AppSettingTestCase
from cogwheels.tests.models import DefaultModel, ReplacementModel


class TestValidModelSettingOverride(AppSettingTestCase):
    """
    Tests the effect of overriding ``COGWHEELS_TESTS_VALID_MODEL``
    """
    def test_returns_default_model_by_default(self):
        self.assertIs(
            self.appsettingshelper.get_model('VALID_MODEL'), DefaultModel,
        )

    @patch('django.apps.apps.get_model')
    def test_returns_from_cache_after_first_import(self, mocked_method):
        settings.clear_caches()
        settings.get_model('VALID_MODEL')
        settings.get_model('VALID_MODEL')
        settings.get_model('VALID_MODEL')
        self.assertEqual(mocked_method.call_count, 1)

    @override_settings(COGWHEELS_TESTS_VALID_MODEL='tests.ReplacementModel')
    def test_successful_override(self):
        self.assertIs(
            self.appsettingshelper.get_model('VALID_MODEL'), ReplacementModel
        )

    @override_settings(COGWHEELS_TESTS_VALID_MODEL=1)
    def test_raises_correct_error_type_when_user_defined_value_is_not_a_string(self):
        with self.assertRaises(exceptions.InvalidSettingValueType):
            self.appsettingshelper.get_model('VALID_MODEL')

    @override_settings(COGWHEELS_TESTS_VALID_MODEL='no_dots_here')
    def test_raises_correct_error_type_when_format_is_invalid(self):
        with self.assertRaises(exceptions.InvalidSettingValueFormat):
            self.appsettingshelper.get_model('VALID_MODEL')

    @override_settings(COGWHEELS_TESTS_VALID_MODEL='tests.NonExistentModel')
    def test_raises_correct_error_type_when_model_not_importable(self):
        with self.assertRaises(exceptions.SettingValueNotImportable):
            self.appsettingshelper.get_model('VALID_MODEL')


class TestInvalidDefaultModelSettings(AppSettingTestCase):
    """
    Tests what happens when an app setting (which is supposed to be a valid
    'model import string') is referenced, but the default value provided by the
    app developer is invalid.
    """

    def test_raises_correct_error_type_when_format_is_invalid(self):
        with self.assertRaises(exceptions.InvalidDefaultValueFormat):
            self.appsettingshelper.get_model('INCORRECT_FORMAT_MODEL')

    def test_raises_correct_error_type_when_model_not_importable(self):
        with self.assertRaises(exceptions.DefaultValueNotImportable):
            self.appsettingshelper.get_model('UNAVAILABLE_MODEL')
