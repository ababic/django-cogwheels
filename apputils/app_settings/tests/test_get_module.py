from unittest.mock import patch
from django.core.exceptions import ImproperlyConfigured
from django.test import override_settings

from apputils.tests.conf import settings
from apputils.tests.base import AppSettingTestCase
from apputils.tests.modules import default_module, replacement_module


class TestValidModuleSettingOverride(AppSettingTestCase):
    """
    Tests the effect of overriding ``APPUTILS_TESTS_VALID_MODULE``
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

    @override_settings(APPUTILS_TESTS_VALID_MODULE='apputils.tests.modules.replacement_module')
    def test_successful_override(self):
        self.assertIs(
            self.appsettingshelper.get_module('VALID_MODULE'), replacement_module
        )

    @override_settings(APPUTILS_TESTS_VALID_MODULE=1)
    def test_raises_error_when_value_is_not_a_string(self):
        message_expected = (
            "Your APPUTILS_TESTS_VALID_MODULE setting value is invalid. A "
            "value of type 'str' is required, but the current value is of "
            "type 'int'."
        )
        with self.assertRaisesMessage(ImproperlyConfigured, message_expected):
            self.appsettingshelper.get_module('VALID_MODULE')

    @override_settings(APPUTILS_TESTS_VALID_MODULE='project.app.module')
    def test_raises_error_when_module_does_not_exist(self):
        message_expected = (
            "Your APPUTILS_TESTS_VALID_MODULE setting value is invalid. No "
            "module could be found with the path 'project.app.module'. Please "
            "use a full, valid import path (e.g. 'project.app.module'), and "
            "avoid using relative paths."
        )
        with self.assertRaisesMessage(ImproperlyConfigured, message_expected):
            self.appsettingshelper.get_module('VALID_MODULE')


class TestInvalidDefaultModuleSettings(AppSettingTestCase):
    """
    Tests what happens when an app setting (which is supposed to be a valid
    python import path) is referenced, but the default value provided by the
    app developer is invalid.
    """

    def test_raises_error_when_module_unavailable(self):
        message_expected = (
            "The value used for UNAVAILABLE_MODULE in apputils.tests.conf"
            ".defaults is invalid. No module could be found with the path "
            "'apputils.tests.modules.imaginary_module'. Please use a full, "
            "valid import path (e.g. 'project.app.module'), and avoid using "
            "relative paths."
        )
        with self.assertRaisesMessage(ImproperlyConfigured, message_expected):
            self.appsettingshelper.get_module('UNAVAILABLE_MODULE')
