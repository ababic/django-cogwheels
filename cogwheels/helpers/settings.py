from importlib import import_module
from django.conf import settings as django_settings
from django.core.signals import setting_changed
from cogwheels import (
    OverrideValueError, OverrideValueTypeInvalid,
    OverrideValueFormatInvalid, OverrideValueNotImportable,
    DefaultValueError, DefaultValueTypeInvalid,
    DefaultValueFormatInvalid, DefaultValueNotImportable,
)
from cogwheels.exceptions.deprecations import (
    ImproperlyConfigured,
    IncorrectDeprecationsValueType, InvalidDeprecationDefinition,
    DuplicateDeprecationError, DuplicateDeprecationReplacementError,
)
from .utils import AttrRefererToMethodHelper


class BaseAppSettingsHelper:

    prefix = None
    defaults_path = None
    deprecations = ()

    def __init__(self, prefix=None, defaults_path=None, deprecations=None):
        self.__module_path_split = self.__class__.__module__.split('.')
        self._set_prefix(prefix)

        # Load values from defaults module
        self._set_defaults_module_path(defaults_path)
        self._load_defaults()

        # Load deprecation data
        if deprecations is not None:
            self._deprecations = deprecations
        else:
            self._deprecations = self.__class__.deprecations
        self._perepare_deprecation_data()

        self._raw_cache = {}

        # Define 'models' reference shortcut and cache
        self.models = AttrRefererToMethodHelper(self, 'get_model')
        self._models_cache = {}

        # Define 'modules' reference shortcut and cache
        self.modules = AttrRefererToMethodHelper(self, 'get_module')
        self._modules_cache = {}

        # Define 'object' reference shortcut and cache
        self.objects = AttrRefererToMethodHelper(self, 'get_object')
        self._objects_cache = {}

        setting_changed.connect(self.clear_caches, dispatch_uid=id(self))

    def __getattr__(self, name):
        """
        If the requested attribute wasn't found, it's assumed that the caller
        wants the value of a setting matching 'name'. So, if 'name' looks like
        a valid setting name, refer the request to 'self.get_raw()', otherwise
        raise an ``AttributeError``, so that the caller knows the request is
        invalid.
        """
        if not self.in_defaults(name):
            raise AttributeError("{} object has no attribute '{}'".format(
                self.__class__.__name__, name))
        return self.get_raw(name)

    def _set_prefix(self, init_supplied_val):
        """
        Sets this object's ``_prefix`` attribute to a sensible value. If no
        value was provided to __init__(), and no value has been set using the
        ``prefix`` class attribute, a default value will be used, based on
        where the helper class is defined.

        For example:

        If the class is defined in ``myapp/conf/settings.py`` or
        ``myapp/settings.py``, the value ``"MYAPP"`` would be used.

        If the class is defined in ``myapp/subapp/conf/settings.py`` or
        ``myapp/subapps/settings.py`` the value ``"MYAPP_SUBAPP"`` would be
        used.
        """
        if init_supplied_val is not None:
            value = init_supplied_val.rstrip('_')
        elif self.__class__.prefix is not None:
            value = self.__class__.prefix.rstrip('_')
        else:
            module_path_parts = self.__module_path_split[:-1]
            try:
                module_path_parts.remove('conf')
            except ValueError:
                pass
            value = '_'.join(module_path_parts).upper()
        self._prefix = value

    def _set_defaults_module_path(self, init_supplied_val):
        """
        Sets this object's ``_defaults_module_path`` attribute to a sensible
        value. If no value was provided to __init__(), and no value has been
        set using the ``defaults_path`` class attribute, a default value will
        be used, based on where the helper class is defined.

        It is assumed that the defaults module is defined in the same directory
        as the settings helper. For example:

        If the settings helper is defined in ``myapp/config/settings.py``, the
        defaults module is assumed to be at ``myapp/config/defaults.py``.

        If the settings helper is defined in ``myapp/some_other_directory/settings.py``,
        the defaults module is assumed to be at ``myapp/some_other_directory/defaults.py``.
        """
        if init_supplied_val is not None:
            value = init_supplied_val
        elif self.__class__.defaults_path is not None:
            value = self.__class__.defaults_path
        else:
            value = '.'.join(self.__module_path_split[:-1]) + ".defaults"
        self._defaults_module_path = value

    @staticmethod
    def _do_import(module_path):
        """A simple wrapper for importlib.import_module()."""
        return import_module(module_path)

    def _load_defaults(self):
        """
        Sets the object's ``_defaults`` attibute value to a dictionary for
        optimal lookup performance. Items are loaded from the relevant
        ``defaults.py`` module on initialisation.
        """
        module = self._do_import(self._defaults_module_path)
        self._defaults = {
            k: v for k, v in module.__dict__.items()
            if k.isupper()  # ignore anything that doesn't look like a setting
        }

    def _perepare_deprecation_data(self):
        """
        Cycles through the list of AppSettingDeprecation instances set on
        ``self._deprecations`` and propulates two new dictionary attributes:

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
            raise IncorrectDeprecationsValueType(
                "'deprecations' must be a list or tuple, not a {}."
                .format(type(self._deprecations).__name__)
            )

        self._deprecated_settings = {}
        self._replacement_settings = {}

        for item in self._deprecations:
            item.prefix = self._prefix

            if not self.in_defaults(item.setting_name):
                raise InvalidDeprecationDefinition(
                    "There is an issue with one of your setting deprecation "
                    "definitions. '{setting_name}' could not be found in "
                    "{defaults_module_path}. Please ensure a default value "
                    "remains there until the end of the setting's deprecation "
                    "period."
                    .format(
                        setting_name=item.setting_name,
                        defaults_module_path=self._defaults_module_path,
                    )
                )

            if item.setting_name in self._deprecated_settings:
                raise DuplicateDeprecationError(
                    "The setting name for each deprecation definition "
                    "must be unique, but '{setting_name}' has been used more "
                    "than once for {helper_class}. "
                    .format(
                        setting_name=item.setting_name,
                        helper_class=self.__class__.__name__,
                    )
                )

            self._deprecated_settings[item.setting_name] = item

            if item.replacement_name:

                if item.replacement_name in self._replacement_settings:
                    raise DuplicateDeprecationReplacementError(
                        "The replacement setting name for each deprecation "
                        "definition must be unique, but '{setting_name}' has "
                        "been used more than once for {helper_class}."
                        .format(
                            setting_name=item.replacement_name,
                            helper_class=self.__class__.__name__,
                        )
                    )

                if not self.in_defaults(item.replacement_name):
                    raise InvalidDeprecationDefinition(
                        "There is an issue with one of your settings "
                        "deprecation definitions. '{replacement_name}' is not "
                        "a valid replacement for '{setting_name}', as no such "
                        "value can be found in {defaults_module_path}."
                        .format(
                            replacement_name=item.replacement_name,
                            setting_name=item.setting_name,
                            defaults_module_path=self._defaults_module_path,
                        )
                    )

                self._replacement_settings[item.replacement_name] = item

    def clear_caches(self, **kwargs):
        self._raw_cache = {}
        self._models_cache = {}
        self._modules_cache = {}
        self._objects_cache = {}

    def in_defaults(self, setting_name):
        return setting_name in self._defaults

    def get_default_value(self, setting_name):
        try:
            return self._defaults[setting_name]
        except KeyError:
            pass
        raise ImproperlyConfigured(
            "No default value could be found in {default_module} with the "
            "name '{setting_name}'."
            .format(
                setting_name=setting_name,
                default_module=self._defaults_module_path,
            )
        )

    def get_prefix(self):
        return self._prefix + '_'

    def get_prefixed_setting_name(self, setting_name):
        return self.get_prefix() + setting_name

    def get_user_defined_value(self, setting_name):
        attr_name = self.get_prefixed_setting_name(setting_name)
        return getattr(django_settings, attr_name)

    def is_overridden(self, setting_name):
        attr_name = self.get_prefixed_setting_name(setting_name)
        return hasattr(django_settings, attr_name)

    def raise_setting_error(
        self, setting_name, additional_text,
        user_value_error_class=None, default_value_error_class=None,
        **text_format_kwargs
    ):
        if self.is_overridden(setting_name):
            error_class = user_value_error_class or OverrideValueError
            message = (
                "There is an issue with the value specified for "
                "{setting_name} in your project's Django settings."
            ).format(setting_name=self.get_prefixed_setting_name(setting_name))
        else:
            error_class = default_value_error_class or DefaultValueError
            message = (
                "There is an issue with the default value specified for "
                "{setting_name} in {defaults_module}."
            ).format(
                setting_name=setting_name,
                defaults_module=self._defaults_module_path,
            )

        message += ' ' + additional_text.format(**text_format_kwargs)
        raise error_class(message)

    def _get_raw_setting_value(self, setting_name):
        """
        Returns the value of the app setting named by ``setting_name``,
        exactly as it has been defined in the defaults modul or a user's
        Django settings.

        If the requested setting is deprecated, a suitable deprecation
        warning is raised to help inform developers of the change.

        If the requested setting replaces a deprecated setting, and no user
        defined setting name is defined using the new name, the method will
        look for a user defined setting value using the deprecated setting
        name, and return that if found. A deprecation warning will also be
        raised.

        If no override value was found in the Django setting, then the
        relevant value from the defaults module is returned.
        """
        if setting_name in self._deprecated_settings:
            depr = self._deprecated_settings[setting_name]
            depr.warn_if_setting_attribute_referenced()

        if self.is_overridden(setting_name):
            return self.get_user_defined_value(setting_name)

        if setting_name in self._replacement_settings:
            depr = self._replacement_settings[setting_name]
            if self.is_overridden(depr.setting_name):
                depr.warn_if_user_using_old_setting_name()
                return self.get_user_defined_value(depr.setting_name)

        return self.get_default_value(setting_name)

    def is_value_from_deprecated_setting(self, setting_name):
        """
        Returns a boolean to help developers determine where a setting value
        came from when dealing settings that replace deprecated settings.
        Returns ``True`` when:

        -   The setting named by ``setting_name`` is a replacement for a
            deprecated setting.
        -   The value returned by self.get_raw() for the setting comes from a
            user-defined Django setting that uses the deprecated setting name
        """
        if not self.in_defaults(setting_name):
            raise ValueError('%s is not a valid setting name' % setting_name)
        if(
            not self.is_overridden(setting_name) and
            setting_name in self._replacement_settings
        ):
            depr = self._replacement_settings[setting_name]
            return self.is_overridden(depr.setting_name)
        return False

    def get_raw(self, setting_name, enforce_type=None):
        """
        A wrapper for self.get_raw_value(), that caches the raw setting value
        for faster future access, and, optionally checks that the
        raw value type matches the supplied ``enforce_type`` value type (or
        tuple of value types).
        """
        if setting_name in self._raw_cache:
            return self._raw_cache[setting_name]

        result = self._get_raw_setting_value(setting_name)
        if enforce_type and not isinstance(result, enforce_type):
            if isinstance(enforce_type, tuple):
                msg = (
                    "The value is expected to be one of the following types, "
                    "but a value of type '{current_type}' was found: "
                    "{required_types}."
                )
                text_format_kwargs = dict(
                    current_type=type(result).__name__,
                    required_types=enforce_type,
                )
            else:
                msg = (
                    "The value is expected to be a '{required_type}', but a "
                    "value of type '{current_type}' was found."
                )
                text_format_kwargs = dict(
                    current_type=type(result).__name__,
                    required_type=enforce_type.__name__,
                )
            self.raise_setting_error(
                setting_name=setting_name,
                user_value_error_class=OverrideValueTypeInvalid,
                default_value_error_class=DefaultValueTypeInvalid,
                additional_text=msg,
                **text_format_kwargs
            )
        self._raw_cache[setting_name] = result
        return result

    def get_model(self, setting_name):
        """
        Returns a Django model referenced by an app setting who's value should
        be a 'model string' in the format 'app_label.model_name'.

        Raises an ``ImproperlyConfigured`` error if the setting value is not
        in the correct format, or refers to a model that is not available.
        """
        if setting_name in self._models_cache:
            return self._models_cache[setting_name]

        raw_value = self.get_raw(setting_name, enforce_type=str)

        try:
            from django.apps import apps  # delay import until needed
            result = apps.get_model(raw_value)
            self._models_cache[setting_name] = result
            return result
        except ValueError:
            self.raise_setting_error(
                setting_name=setting_name,
                user_value_error_class=OverrideValueFormatInvalid,
                default_value_error_class=DefaultValueFormatInvalid,
                additional_text=(
                    "Model strings should match the format 'app_label.Model', "
                    "which '{value}' does not adhere to."
                ),
                value=raw_value,
            )
        except LookupError:
            self.raise_setting_error(
                setting_name=setting_name,
                user_value_error_class=OverrideValueNotImportable,
                default_value_error_class=DefaultValueNotImportable,
                additional_text=(
                    "The model '{value}' does not appear to be installed."
                ),
                value=raw_value
            )

    def get_module(self, setting_name):
        """
        Returns a python module referenced by an app setting who's value should
        be a valid python import path, defined as a string.

        Will not work for relative paths.

        Raises an ``ImproperlyConfigured`` error if the setting value is not
        a valid import path.
        """
        if setting_name in self._modules_cache:
            return self._modules_cache[setting_name]

        raw_value = self.get_raw(setting_name, enforce_type=str)

        try:
            result = self._do_import(raw_value)
            self._modules_cache[setting_name] = result
            return result
        except ImportError:
            self.raise_setting_error(
                setting_name=setting_name,
                user_value_error_class=OverrideValueNotImportable,
                default_value_error_class=DefaultValueNotImportable,
                additional_text=(
                    "No module could be found matching the path '{value}'. "
                    "Please use a full (not relative) import path in the "
                    "format: 'project.app.module'."
                ),
                value=raw_value
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
        if setting_name in self._objects_cache:
            return self._objects_cache[setting_name]

        raw_value = self.get_raw(setting_name, enforce_type=str)

        try:
            module_path, object_name = raw_value.rsplit(".", 1)
        except ValueError:
            self.raise_setting_error(
                setting_name=setting_name,
                user_value_error_class=OverrideValueFormatInvalid,
                default_value_error_class=DefaultValueFormatInvalid,
                additional_text=(
                    "'{value}' is not a valid object import path. Please use "
                    "a full (not relative) import path with the object name "
                    "at the end, for example: 'project.app.module.object'."
                ),
                value=raw_value
            )
        try:
            result = getattr(self._do_import(module_path), object_name)
            self._objects_cache[setting_name] = result
            return result
        except ImportError:
            self.raise_setting_error(
                setting_name=setting_name,
                user_value_error_class=OverrideValueNotImportable,
                default_value_error_class=DefaultValueNotImportable,
                additional_text=(
                    "No module could be found matching the path "
                    "'{module_path}'. Please use a full (not relative) import "
                    "path with the object name at the end, for example: "
                    "'project.app.module.object'."
                ),
                module_path=module_path,
            )
        except AttributeError:
            self.raise_setting_error(
                setting_name=setting_name,
                user_value_error_class=OverrideValueNotImportable,
                default_value_error_class=DefaultValueNotImportable,
                additional_text=(
                    "No object could be found in {module_path} matching the "
                    "name '{object_name}'."
                ),
                module_path=module_path,
                object_name=object_name,
            )
