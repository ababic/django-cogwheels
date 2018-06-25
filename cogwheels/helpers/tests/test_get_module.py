from unittest.mock import patch
from django.test import override_settings

from cogwheels import exceptions
from cogwheels.tests.conf import settings
from cogwheels.tests.base import AppSettingTestCase
from cogwheels.tests.modules import default_module, replacement_module


class TestValidModuleSettingOverride(AppSettingTestCase):
    """
    Tests the effect of overriding ``COGWHEELS_TESTS_VALID_MODULE``
    """
    def test_returns_default_module_by_default(self):
        self.assertIs(
            self.appsettingshelper.get_module('VALID_MODULE'), default_module,
        )

    @patch.object(settings, 'import_module')
    def test_returns_from_cache_after_first_import(self, mocked_method):
        settings.clear_caches()
        settings.get_module('VALID_MODULE')
        settings.get_module('VALID_MODULE')
        settings.get_module('VALID_MODULE')
        self.assertEqual(mocked_method.call_count, 1)

    @override_settings(COGWHEELS_TESTS_VALID_MODULE='cogwheels.tests.modules.replacement_module')
    def test_successful_override(self):
        self.assertIs(
            self.appsettingshelper.get_module('VALID_MODULE'), replacement_module
        )

    @override_settings(COGWHEELS_TESTS_VALID_MODULE=1)
    def test_raises_correct_error_type_when_value_is_not_a_string(self):
        with self.assertRaises(exceptions.InvalidSettingValueType):
            self.appsettingshelper.get_module('VALID_MODULE')

    @override_settings(COGWHEELS_TESTS_VALID_MODULE='project.app.module')
    def test_raises_correct_error_type_when_module_not_importable(self):
        with self.assertRaises(exceptions.SettingValueNotImportable):
            self.appsettingshelper.get_module('VALID_MODULE')


class TestInvalidDefaultModuleSettings(AppSettingTestCase):
    """
    Tests what happens when an app setting (which is supposed to be a valid
    python import path) is referenced, but the default value provided by the
    app developer is invalid.
    """

    def test_raises_correct_error_type_when_module_unavailable(self):
        with self.assertRaises(exceptions.DefaultValueNotImportable):
            self.appsettingshelper.get_module('UNAVAILABLE_MODULE')
