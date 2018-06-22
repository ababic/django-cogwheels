from django.core.exceptions import ImproperlyConfigured
from django.test import override_settings

from apputils.tests.base import AppSettingTestCase
from apputils.tests.modules import default_module, replacement_module


class TestValidModuleSettingOverride(AppSettingTestCase):
    """
    Tests the effect of overriding ``TEST_VALID_MODULE``
    """
    def test_returns_default_module_by_default(self):
        # Using 'get_module()' directly
        self.assertIs(
            self.appsettingshelper.get_module('VALID_MODULE'), default_module,
        )

        # Using the 'modules' attribute shortcut
        self.assertIs(
            self.appsettingshelper.modules.VALID_MODULE, default_module,
        )

    @override_settings(TEST_VALID_MODULE='apputils.tests.modules.replacement_module')
    def test_successful_override(self):
        # Using 'get_module()' directly
        self.assertIs(
            self.appsettingshelper.get_module('VALID_MODULE'), replacement_module
        )

        # Using the 'modules' attribute shortcut
        self.assertIs(
            self.appsettingshelper.modules.VALID_MODULE, replacement_module
        )

    @override_settings(TEST_VALID_MODULE='project.app.module')
    def test_raises_error_when_module_does_not_exist(self):
        message_expected = (
            "Your TEST_VALID_MODULE setting value is invalid. No module could "
            "be found with the path 'project.app.module'. Please use a full, "
            "valid import path (e.g. 'project.app.module'), and avoid using "
            "relative paths."
        )

        # Using 'get_module()' directly
        with self.assertRaisesMessage(ImproperlyConfigured, message_expected):
            self.appsettingshelper.get_module('VALID_MODULE')

        # Using the 'modules' attribute shortcut
        with self.assertRaisesMessage(ImproperlyConfigured, message_expected):
            self.appsettingshelper.modules.VALID_MODULE


class TestInvalidDefaultModuleSettings(AppSettingTestCase):
    """
    Tests what happens when an app setting (which is supposed to be a valid
    python import path) is referenced, but the default value provided by the
    app developer is invalid.
    """

    def test_raises_error_when_module_unavailable(self):
        message_expected = (
            "The default value defined by the app developer for the "
            "UNAVAILABLE_MODULE app setting is invalid. No module could be "
            "found with the path 'apputils.tests.modules.imaginary_module'. "
            "Please use a full, valid import path (e.g. 'project.app.module')"
            ", and avoid using relative paths."

        )

        # Using 'get_module()' directly
        with self.assertRaisesMessage(ImproperlyConfigured, message_expected):
            self.appsettingshelper.get_module('UNAVAILABLE_MODULE')

        # Using the 'modules' attribute shortcut
        with self.assertRaisesMessage(ImproperlyConfigured, message_expected):
            self.appsettingshelper.modules.UNAVAILABLE_MODULE
