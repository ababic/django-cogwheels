from django.core.exceptions import ImproperlyConfigured
from django.test import override_settings

from apputils.tests.base import AppSettingTestCase
from apputils.tests.classes import DefaultClass, ReplacementClass


class TestValidObjectSettingOverride(AppSettingTestCase):
    """
    Tests the effect of overriding ``TEST_VALID_OBJECT``
    """
    def test_returns_default_class_by_default(self):
        self.assertEqual(
            self.appsettingshelper.get_object('VALID_OBJECT'), DefaultClass,
        )

    @override_settings(TEST_VALID_OBJECT='apputils.tests.classes.ReplacementClass')
    def test_successful_override(self):
        self.assertEqual(
            self.appsettingshelper.get_object('VALID_OBJECT'), ReplacementClass
        )

    @override_settings(TEST_VALID_OBJECT=1)
    def test_raises_error_when_value_is_not_a_string(self):
        message_expected = (
            "Your TEST_VALID_OBJECT setting value is invalid. A value of type "
            "'str' is required, but the current value is of type 'int'."
        )
        with self.assertRaisesMessage(ImproperlyConfigured, message_expected):
            self.appsettingshelper.get_object('VALID_OBJECT')

    @override_settings(TEST_VALID_OBJECT='no_dots_here')
    def test_raises_error_when_format_is_invalid(self):
        message_expected = (
            "Your TEST_VALID_OBJECT setting value is invalid. 'no_dots_here' "
            "is not a valid object import path. Please use a full, valid "
            "import path with the object name at the end (e.g. "
            "'project.app.module.object'), and avoid using relative paths."
        )
        with self.assertRaisesMessage(ImproperlyConfigured, message_expected):
            self.appsettingshelper.get_object('VALID_OBJECT')

    @override_settings(TEST_VALID_OBJECT='project.app.module.Class')
    def test_raises_error_when_module_does_not_exist(self):
        message_expected = (
            "Your TEST_VALID_OBJECT setting value is invalid. No module could "
            "be found with the path 'project.app.module'. Please use a full, "
            "valid import path with the object name at the end (e.g. "
            "'project.app.module.object'), and avoid using relative paths."
        )
        with self.assertRaisesMessage(ImproperlyConfigured, message_expected):
            self.appsettingshelper.get_object('VALID_OBJECT')

    @override_settings(TEST_VALID_OBJECT='apputils.tests.classes.NonExistentClass')
    def test_raises_error_object_not_found_in_module(self):
        message_expected = (
            "Your TEST_VALID_OBJECT setting value is invalid. No object could "
            "be found in 'apputils.tests.classes' with the name "
            "'NonExistentClass'. Could it have been moved or renamed?"
        )
        with self.assertRaisesMessage(ImproperlyConfigured, message_expected):
            self.appsettingshelper.get_object('VALID_OBJECT')


class TestInvalidDefaultObjectSettings(AppSettingTestCase):
    """
    Tests what happens when an app setting (which is supposed to be a valid
    python import path) is referenced, but the default value provided by the
    app developer is invalid.
    """

    def test_raises_error_when_format_is_invalid(self):
        message_expected = (
            "The default value defined for the "
            "INCORRECT_FORMAT_OBJECT app setting is invalid. 'DefaultClass' "
            "is not a valid object import path. Please use a full, valid "
            "import path with the object name at the end (e.g. "
            "'project.app.module.object'), and avoid using relative paths."
        )
        with self.assertRaisesMessage(ImproperlyConfigured, message_expected):
            self.appsettingshelper.get_object('INCORRECT_FORMAT_OBJECT')

    def test_raises_error_when_module_unavailable(self):
        message_expected = (
            "The default value defined for the MODULE_UNAVAILABLE_OBJECT app "
            "setting is invalid. No module could be found with the path "
            "'apputils.imaginary_module'. Please use a full, valid import "
            "path with the object name at the end (e.g. "
            "'project.app.module.object'), and avoid using relative paths."
        )
        with self.assertRaisesMessage(ImproperlyConfigured, message_expected):
            self.appsettingshelper.get_object('MODULE_UNAVAILABLE_OBJECT')

    def test_raises_error_when_object_unavailable(self):
        message_expected = (
            "The default value defined for the OBJECT_UNAVAILABLE_OBJECT app "
            "setting is invalid. No object could be found in "
            "'apputils.tests.classes' with the name 'NonExistent'. Could it "
            "have been moved or renamed?"
        )
        with self.assertRaisesMessage(ImproperlyConfigured, message_expected):
            self.appsettingshelper.get_object('OBJECT_UNAVAILABLE_OBJECT')
