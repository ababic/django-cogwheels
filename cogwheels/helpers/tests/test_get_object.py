from unittest.mock import patch

from django.test import override_settings

from cogwheels import exceptions
from cogwheels.tests.conf import settings
from cogwheels.tests.base import AppSettingTestCase
from cogwheels.tests.classes import DefaultClass, ReplacementClass


class TestValidObjectSettingOverride(AppSettingTestCase):
    """
    Tests the effect of overriding ``COGWHEELS_TESTS_VALID_OBJECT``
    """
    def test_returns_default_class_by_default(self):
        self.assertIs(
            self.appsettingshelper.get_object('VALID_OBJECT'), DefaultClass,
        )

    @patch.object(settings, 'import_module')
    def test_returns_from_cache_after_first_import(self, mocked_method):
        settings.clear_caches()
        settings.get_object('VALID_OBJECT')
        settings.get_object('VALID_OBJECT')
        settings.get_object('VALID_OBJECT')
        self.assertEqual(mocked_method.call_count, 1)

    @override_settings(COGWHEELS_TESTS_VALID_OBJECT='cogwheels.tests.classes.ReplacementClass')
    def test_successful_override(self):
        self.assertIs(
            self.appsettingshelper.get_object('VALID_OBJECT'), ReplacementClass
        )

    @override_settings(COGWHEELS_TESTS_VALID_OBJECT=1)
    def test_raises_correct_error_type_when_value_is_not_a_string(self):
        with self.assertRaises(exceptions.InvalidSettingValueType):
            self.appsettingshelper.get_object('VALID_OBJECT')

    @override_settings(COGWHEELS_TESTS_VALID_OBJECT='no_dots_here')
    def test_raises_correct_error_type_when_format_is_invalid(self):
        with self.assertRaises(exceptions.InvalidSettingValueFormat):
            self.appsettingshelper.get_object('VALID_OBJECT')

    @override_settings(COGWHEELS_TESTS_VALID_OBJECT='project.app.module.Class')
    def test_raises_correct_error_type_when_module_not_found(self):
        with self.assertRaises(exceptions.SettingValueNotImportable):
            self.appsettingshelper.get_object('VALID_OBJECT')

    @override_settings(COGWHEELS_TESTS_VALID_OBJECT='cogwheels.tests.classes.NonExistentClass')
    def test_raises_correct_error_type_when_object_not_found(self):
        with self.assertRaises(exceptions.SettingValueNotImportable):
            self.appsettingshelper.get_object('VALID_OBJECT')


class TestInvalidDefaultObjectSettings(AppSettingTestCase):
    """
    Tests what happens when an app setting (which is supposed to be a valid
    python import path) is referenced, but the default value provided by the
    app developer is invalid.
    """

    def test_raises_correct_error_type_when_format_is_invalid(self):
        with self.assertRaises(exceptions.InvalidDefaultValueFormat):
            self.appsettingshelper.get_object('INCORRECT_FORMAT_OBJECT')

    def test_raises_correct_error_type_when_module_not_found(self):
        with self.assertRaises(exceptions.DefaultValueNotImportable):
            self.appsettingshelper.get_object('MODULE_UNAVAILABLE_OBJECT')

    def test_raises_correct_error_type_when_object_not_found(self):
        with self.assertRaises(exceptions.DefaultValueNotImportable):
            self.appsettingshelper.get_object('OBJECT_UNAVAILABLE_OBJECT')
