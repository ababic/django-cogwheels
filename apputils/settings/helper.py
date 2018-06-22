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

    prefix = ''
    defaults_path = None
    deprecations = ()

    def __init__(self, prefix=None, defaults_path=None, deprecations=None):
        from django.conf import settings
        self._prefix = prefix or self.__class__.prefix
        self._defaults_path = defaults_path or self.__class__.defaults_path
        self._defaults = self.load_defaults(self._defaults_path)
        self._django_settings = settings
        self._import_cache = {}
        self._model_cache = {}
        self._deprecations = deprecations or self.__class__.deprecations
        self.perepare_deprecation_data()
        self.modules = HelperMethodAttrWrapper(self, 'get_module')
        self.objects = HelperMethodAttrWrapper(self, 'get_object')
        self.models = HelperMethodAttrWrapper(self, 'get_model')
        setting_changed.connect(self.clear_caches, dispatch_uid=id(self))

    @classmethod
    def load_defaults(cls, module_path):
        try:
            module = import_module(module_path)
            return {
                k: v for k, v in module.__dict__.items() if k.isupper()
            }
        except ImportError:
            raise ImproperlyConfigured(_(
                "The 'defaults_path' value provided for {class_name} is "
                "invalid. '{value}' is not a valid python import path."
            ).format(class_name=cls.__name__, value=module_path))

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
                "'deprecations' must be a list or tuple, not {}."
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
            if item.replacement_name and item.is_renamed:
                self._replacement_settings[item.replacement_name] = item
                if not self.in_defaults(item.replacement_name):
                    raise ImproperlyConfigured(_(
                        "'{replacement_name}' is not a valid replacement "
                        "for {setting_name}. Please ensure {replacement_name} "
                        "has been added to the defaults module."
                    ).format(
                        replacement_name=item.replacement_name,
                        setting_name=item.setting_name,
                    ))

    def clear_caches(self, **kwargs):
        self._import_cache = {}
        self._model_cache = {}

    def in_defaults(self, setting_name):
        return setting_name in self._defaults

    def get_default_value(self, setting_name):
        try:
            return self._defaults[setting_name]
        except KeyError:
            pass
        raise ImproperlyConfigured(_(
            "No default value could be found for '{setting_name}'. Setting "
            "names should always be uppercase, and a default value must "
            "always be added to '{default_module}'."
        ).format(
            setting_name=setting_name, default_module=self._defaults_path
        ))

    def __getattr__(self, name):
        if self.in_defaults(name):
            return self.get(name)
        raise AttributeError("{} object has no attribute '{}'".format(
            self.__class__.__name__, name))

    def get_user_defined_value(self, setting_name):
        attr_name = self._prefix + setting_name
        return getattr(self._django_settings, attr_name)

    def is_overridden(self, setting_name):
        return hasattr(self._django_settings, self._prefix + setting_name)

    def make_invalid_setting_message(self, setting_name, additional_text,
                                     *args, **kwargs):
        if self.is_overridden(setting_name):
            msg = _("Your {} setting value is invalid. ").format(
                self._prefix + setting_name)
        else:
            msg = _(
                "The default value defined by the app developer for the "
                "{} app setting is invalid. "
            ).format(setting_name)
        return msg + additional_text.format(*args, **kwargs)

    def get(self, setting_name):
        """
        Returns the value of the app setting named by ``setting_name``.
        If the setting is unavailable in the Django settings module, then the
        default value from the ``defaults`` dictionary is returned.

        If the setting is deprecated, a suitable deprecation warning will be
        raised, to help inform developers of the change.

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

    def get_module(self, setting_name):
        """
        Returns a python module referenced by an app setting who's value should
        be a string representation of a valid python import path.

        Will not work for relative paths.

        Raises an ``ImproperlyConfigured`` error if the setting value is not
        a valid import path.
        """
        if setting_name in self._import_cache:
            return self._import_cache[setting_name]

        setting_value = getattr(self, setting_name)
        try:
            result = import_module(setting_value)
            self._import_cache[setting_name] = result
            return result
        except ImportError:
            raise ImproperlyConfigured(self.make_invalid_setting_message(
                setting_name,
                "No module could be found with the path '{value}'. Please "
                "use a full, valid import path (e.g. 'project.app.module'), "
                "and avoid using relative paths.",
                value=setting_value
            ))

    def get_object(self, setting_name):
        """
        Returns a python class, method, or other object referenced by
        an app setting who's value should be a string representation of a valid
        python import path.

        Will not work for relative paths.

        Raises an ``ImproperlyConfigured`` error if the setting value is not
        a valid import path, or the object is not found in the imported module.
        """
        if setting_name in self._import_cache:
            return self._import_cache[setting_name]

        setting_value = getattr(self, setting_name)

        try:
            module_path, object_name = setting_value.rsplit(".", 1)
            result = getattr(import_module(module_path), object_name)
            self._import_cache[setting_name] = result
            return result
        except ValueError:
            raise ImproperlyConfigured(self.make_invalid_setting_message(
                setting_name,
                "'{value}' is not a valid object import path. Please use a "
                "full, valid import path with the object name at the "
                "end (e.g. 'project.app.module.object'), and avoid using "
                "relative paths.",
                value=setting_value
            ))
        except ImportError:
            raise ImproperlyConfigured(self.make_invalid_setting_message(
                setting_name,
                "No module could be found with the path '{module_path}'. "
                "Please use a full, valid import path with the object name at "
                "the end (e.g. 'project.app.module.object'), and avoid using "
                "relative paths.",
                module_path=module_path
            ))
        except AttributeError:
            raise ImproperlyConfigured(self.make_invalid_setting_message(
                setting_name,
                "No object could be found in '{module_path}' with the name "
                "'{object_name}'. Could it have been moved or renamed?",
                module_path=module_path,
                object_name=object_name,
            ))

    def get_model(self, setting_name):
        """
        Returns a Django model referenced by an app setting who's value should
        be a 'model string' in the format 'app_label.model_name'.

        Raises an ``ImproperlyConfigured`` error if the setting value is not
        in the correct format, or refers to a model that is not available.
        """
        if setting_name in self._model_cache:
            return self._model_cache[setting_name]

        from django.apps import apps  # delay import until needed
        setting_value = getattr(self, setting_name)

        try:
            result = apps.get_model(setting_value)
            self._model_cache[setting_name] = result
            return result
        except ValueError:
            raise ImproperlyConfigured(self.make_invalid_setting_message(
                setting_name,
                "Model strings must be in the format 'app_label.ModelName', "
                "which '{value}' does not adhere to.",
                value=setting_value
            ))
        except LookupError:
            raise ImproperlyConfigured(self.make_invalid_setting_message(
                setting_name,
                "The model '{value}' does not appear to be installed.",
                value=setting_value,
            ))
