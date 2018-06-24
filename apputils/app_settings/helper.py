from importlib import import_module
from django.core.exceptions import ImproperlyConfigured
from django.core.signals import setting_changed
from django.utils.translation import ugettext_lazy as _


class HelperMethodAttrWrapper:
    """
    ``BaseAppSettingsHelper`` creates several instances of this class on
    initialisation to allow developers to neatly reference settings to get a
    value cast as a certain type of object. Behind the scenes, attribute
    requests on ``HelperMethodAttrWrapper`` instance are forwarded on to
    one of the helper instance's 'get_x()' methods.

    For example, if you want the actual python module referenced by a setting,
    instead of doing this:

    ``appsettingshelper.get_module('MODULE_SETTING_NAME')``

    The 'modules' ``HelperMethodAttrWrapper`` instance (set as an attribute
    on every setting helper) allows you to do this:

    ``appsettingshelper.modules.MODULE_SETTING_NAME``

    An 'objects' attribute also allows you to neatly access python objects from
    setting values too, like:

    ``appsettingshelper.objects.OBJECT_SETTING_NAME``

    And 'models' allows you to access Django models, like:

    ``appsettingshelper.models.MODEL_SETTING_NAME``

    """
    def __init__(self, settings_helper, getter_method_name):
        self.settings_helper = settings_helper
        self.getter_method_name = getter_method_name

    def __getattr__(self, name):
        if self.settings_helper.in_defaults(name):
            return self.get_value_via_helper_method(name)
        raise AttributeError("{} object has no attribute '{}'".format(
            self.settings_helper.__class__.__name__, name))

    def get_value_via_helper_method(self, setting_name):
        method = getattr(self.settings_helper, self.getter_method_name)
        return method(setting_name)


class BaseAppSettingsHelper:

    prefix = None
    defaults_path = None
    deprecations = ()

    def __init__(self, prefix=None, defaults_path=None, deprecations=None):
        from django.conf import settings

        self._prefix = self.get_prefix_value(prefix)
        self._defaults_path = self.get_defaults_module_path(defaults_path)
        if deprecations is not None:
            self._deprecations = deprecations
        else:
            self._deprecations = self.__class__.deprecations
        self._defaults = self.load_defaults(self._defaults_path)
        self._django_settings = settings
        self._import_cache = {}
        self.perepare_deprecation_data()
        self.modules = HelperMethodAttrWrapper(self, 'get_module')
        self.objects = HelperMethodAttrWrapper(self, 'get_object')
        self.models = HelperMethodAttrWrapper(self, 'get_model')
        setting_changed.connect(self.clear_caches, dispatch_uid=id(self))

    @property
    def module_path_split(self):
        return self.__class__.__module__.split('.')

    def get_prefix_value(self, init_supplied_val):
        """
        Return a value to use for this object's ``_prefix`` attribute. If no
        value was provided to __init__(), and no value has been set on the
        class using the ``prefix`` attribute, a default value is returned,
        based on where the helper class is defined. For example:

        - If the class is defined in ``myapp.conf.settings``, the value would
          be "MYAPP_".
        - If the class is defined in ``myapp.subapp.conf.settings``, the value
          would be "MYAPP_SUBAPP_".
        """
        if init_supplied_val is not None:
            return init_supplied_val
        if self.__class__.prefix is not None:
            return self.__class__.prefix
        return '_'.join(self.module_path_split[:-2]).upper() + '_'

    def get_defaults_module_path(self, init_supplied_val):
        """
        Return a value to use for this object's ``_defaults_path`` attribute.
        If no value was provided to __init__(), and no value has been
        set as on the class using the ``defaults_path`` attribute, a default
        value is returned, based on where the helper class is defined.
        For example:

        - If the class is defined in ``myapp.conf.settings``, the return value
          would be "myapp.conf.defaults".
        - If the class is defined in ``myapp.subapp.conf.settings``, the return
          value would be "myapp.conf.subapp.defaults".
        """
        if init_supplied_val is not None:
            return init_supplied_val
        if self.__class__.defaults_path is not None:
            return self.__class__.defaults_path
        return '.'.join(self.module_path_split[:-1]) + ".defaults"

    @classmethod
    def load_defaults(cls, module_path):
        module = cls.import_module(module_path)
        return {
            k: v for k, v in module.__dict__.items() if k.isupper()
        }

    @staticmethod
    def import_module(module_path):
        """A simple wrapper for importlib.import_module(). Added to allow
        unittest.mock.patch to be used in tests."""
        return import_module(module_path)

    def perepare_deprecation_data(self):
        """
        Cycles through the list of AppSettingDeprecation instances set on
        ``self._deprecations`` and creates two new dictionaries on it:

        ``self._deprecated_settings``:
            Uses the deprecated setting names as keys, and will be
            used to identify if a requested setting value if for a deprecated
            setting.

        ``self._renamed_settings``:
            Uses the 'replacement setting' names as keys (if supplied), and
            allows us to temporarily support user-defined settings using the
            old name when the new setting is requested.
        """
        if not isinstance(self._deprecations, (list, tuple)):
            raise ImproperlyConfigured(_(
                "'deprecations' must be a list or tuple, not a {}."
            ).format(type(self._deprecations).__name__))

        self._deprecated_settings = {}
        self._replacement_settings = {}

        for item in self._deprecations:
            item.prefix = self._prefix
            self._deprecated_settings[item.setting_name] = item
            if not self.in_defaults(item.setting_name):
                raise ImproperlyConfigured(_(
                    "'{setting_name}' cannot be found in the defaults module. "
                    "A value should remain present there until the end of the "
                    "setting's deprecation period."
                ).format(setting_name=item.setting_name))
            if item.replacement_name:
                self._replacement_settings[item.replacement_name] = item
                if not self.in_defaults(item.replacement_name):
                    raise ImproperlyConfigured(_(
                        "'{replacement_name}' is not a valid replacement "
                        "for {setting_name}. Please ensure {replacement_name} "
                        "has been added to {defaults_module_path}."
                    ).format(
                        replacement_name=item.replacement_name,
                        setting_name=item.setting_name,
                        defaults_module_path=self._defaults_path,
                    ))

    def clear_caches(self, **kwargs):
        self._import_cache = {}

    def in_defaults(self, setting_name):
        return setting_name in self._defaults

    def get_default_value(self, setting_name):
        try:
            return self._defaults[setting_name]
        except KeyError:
            pass
        raise ImproperlyConfigured(_(
            "No default value could be found in {default_module} with the "
            "name '{setting_name}'."
        ).format(
            setting_name=setting_name,
            default_module=self._defaults_path,
        ))

    def __getattr__(self, name):
        if self.in_defaults(name):
            return self.get_raw(name)
        raise AttributeError("{} object has no attribute '{}'".format(
            self.__class__.__name__, name))

    def get_user_defined_value(self, setting_name):
        attr_name = self._prefix + setting_name
        return getattr(self._django_settings, attr_name)

    def is_overridden(self, setting_name):
        return hasattr(self._django_settings, self._prefix + setting_name)

    def raise_invalid_setting_value_error(
        self, setting_name, additional_text, *args, **kwargs
    ):
        if self.is_overridden(setting_name):
            message = _(
                "Your {} setting value is invalid."
            ).format(self._prefix + setting_name)
        else:
            message = _(
                "The value used for {setting_name} in {defaults_module} is "
                "invalid."
            ).format(
                setting_name=setting_name,
                defaults_module=self._defaults_path,
            )
        message += ' ' + additional_text.format(*args, **kwargs)
        raise ImproperlyConfigured(message)

    def get_raw(self, setting_name):
        """
        Returns the value of the app setting named by ``setting_name``.
        If the setting is unavailable in the Django settings module, then the
        default value from the ``defaults`` module is returned.

        If the setting is deprecated, a suitable deprecation warning will be
        raised to help inform developers of the change.

        If the named setting replaces a deprecated setting, and no user defined
        setting name is defined using the new name, the method will look for a
        user defined setting using the old name, and return that if found. A
        deprecation warning will also be raised.
        """
        if setting_name in self._deprecated_settings:
            depr = self._deprecated_settings[setting_name]
            depr.warn_if_referenced_directly()

        if self.is_overridden(setting_name):
            return self.get_user_defined_value(setting_name)

        if setting_name in self._replacement_settings:
            depr = self._replacement_settings[setting_name]
            if self.is_overridden(depr.setting_name):
                depr.warn_if_deprecated_value_used_by_replacement()
                return self.get_user_defined_value(depr.setting_name)

        return self.get_default_value(setting_name)

    def get_and_enforce_type(self, setting_name, required_type):
        setting_value = getattr(self, setting_name)
        if not isinstance(setting_value, required_type):
            self.raise_invalid_setting_value_error(
                setting_name, _(
                    "A value of type '{required_type}' is required, but the "
                    "current value is of type '{current_type}'."
                ),
                required_type=required_type.__name__,
                current_type=type(setting_value).__name__,
            )
        return setting_value

    def get_module(self, setting_name):
        """
        Returns a python module referenced by an app setting who's value should
        be a valid python import path, defined as a string.

        Will not work for relative paths.

        Raises an ``ImproperlyConfigured`` error if the setting value is not
        a valid import path.
        """
        if setting_name in self._import_cache:
            return self._import_cache[setting_name]

        setting_value = self.get_and_enforce_type(setting_name, str)

        try:
            result = self.import_module(setting_value)
            self._import_cache[setting_name] = result
            return result
        except ImportError:
            self.raise_invalid_setting_value_error(
                setting_name, _(
                    "No module could be found with the path '{value}'. Please "
                    "use a full, valid import path (e.g. 'project.app.module')"
                    ", and avoid using relative paths."
                ),
                value=setting_value
            )

    def get_object(self, setting_name):
        """
        Returns a python class, method, or other object referenced by
        an app setting who's value should be a valid python import path,
        defined as a string.

        Will not work for relative paths.

        Raises an ``ImproperlyConfigured`` error if the setting value is not
        a valid import path, or the object cannot be found in the specified
        module.
        """
        if setting_name in self._import_cache:
            return self._import_cache[setting_name]

        setting_value = self.get_and_enforce_type(setting_name, str)

        try:
            module_path, object_name = setting_value.rsplit(".", 1)
        except ValueError:
            self.raise_invalid_setting_value_error(
                setting_name, _(
                    "'{value}' is not a valid object import path. Please use "
                    "a full, valid import path with the object name at the "
                    "end (e.g. 'project.app.module.object'), and avoid using "
                    "relative paths."
                ),
                value=setting_value
            )
        try:
            result = getattr(self.import_module(module_path), object_name)
            self._import_cache[setting_name] = result
            return result
        except ImportError:
            self.raise_invalid_setting_value_error(
                setting_name, _(
                    "No module could be found with the path '{module_path}'. "
                    "Please use a full, valid import path with the object "
                    "name at the end (e.g. 'project.app.module.object'), and "
                    "avoid using relative paths."
                ),
                module_path=module_path
            )
        except AttributeError:
            self.raise_invalid_setting_value_error(
                setting_name, _(
                    "No object could be found in '{module_path}' with the "
                    "name '{object_name}'. Could it have been moved or "
                    "renamed?"
                ),
                module_path=module_path,
                object_name=object_name,
            )

    def get_model(self, setting_name):
        """
        Returns a Django model referenced by an app setting who's value should
        be a 'model string' in the format 'app_label.model_name'.

        Raises an ``ImproperlyConfigured`` error if the setting value is not
        in the correct format, or refers to a model that is not available.
        """
        if setting_name in self._import_cache:
            return self._import_cache[setting_name]

        setting_value = self.get_and_enforce_type(setting_name, str)

        try:
            from django.apps import apps  # delay import until needed
            result = apps.get_model(setting_value)
            self._import_cache[setting_name] = result
            return result
        except ValueError:
            self.raise_invalid_setting_value_error(
                setting_name, _(
                    "Model strings must be in the format 'app_label.Model', "
                    "which '{value}' does not adhere to."
                ),
                value=setting_value
            )
        except LookupError:
            self.raise_invalid_setting_value_error(
                setting_name, _(
                    "The model '{value}' does not appear to be installed."
                ),
                value=setting_value
            )
