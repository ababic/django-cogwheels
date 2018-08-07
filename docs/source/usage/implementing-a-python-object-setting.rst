======================
Python object settings
======================

A Python object setting is a setting that allows users to swap out a default class, function or other Python object for a custom one (or an alternative that is available within your app).

Setting values must be defined as Python import path strings (e.g. "project.app.module.object").

When you request the object from your app's settings helper, Cogwheels utilises Python's ``importlib.import_module()`` to import the module and fetch you with the relevant object, caching the result to improve the efficiency of repeat requests for the same object.


Adding a new app setting
========================

App settings are simply variables with upper-case names, added to your app's ``conf/defaults.py`` module, and Python object settings are no exception. You just have to ensure the import path strings you use as default values are correct. For example:

.. code-block:: python

    # yourapp/conf/defaults.py

    # ---------------------
    # FUNCTION SUBSTITUTION
    # ---------------------

    USERNAME_VALIDATOR = "yourapp.accounts.validators.username_default"

    # ------------------
    # CLASS SUBSTITUTION
    # ------------------

    MAIN_MENU_ADD_FORM = "yourapp.menus.forms.MainMenuAddForm"

    CATEGORY_OPTIONS_FORM_WIDGET = 'django.forms.RadioSelect'

Users will override these settings by adding override values to their Django settings, like so:

.. code-block:: python

    # userdjangoproject/settings/base.py

    ...

    # ---------------------------------
    # Overrides for ``your-django-app``
    # ---------------------------------

    # Use the built-in validator to ensure usernames are valid emails
    YOURAPP_USERNAME_VALIDATOR = 'yourapp.accounts.validators.email_address'

    # Use our custom form when adding menus
    YOURAPP_MAIN_MENU_ADD_FORM = 'core.forms.menus.CustomMainMenuAddForm'

.. NOTE::
    Users define overrides using *prefixed* setting names. The prefix used in the example above is **YOURAPP_** because of where the ``conf`` app is defined in the example, but this will differ for your app. For more information see: :ref:`finding-the-namespace-prefix`.


Retrieving the app setting value
================================

You can use the settings helper's ``objects`` attribute shortcut or ``get_object()`` method to retrieve the Python objects referenced by setting values.

.. code-block:: console

    > from yourapp.conf import settings
    
    > settings.objects.MAIN_MENU_ADD_FORM
    core.forms.menus.CustomMainMenuAddForm

    > settings.get_object("MAIN_MENU_ADD_FORM")
    core.forms.menus.CustomMainMenuAddForm

    > settings.objects.USERNAME_VALIDATOR
    <function yourapp.accounts.validators.username.default(username, obj)>

    > settings.get_object("USERNAME_VALIDATOR")
    <function yourapp.accounts.validators.username.default(username, obj)>


Validation and error handling
=============================

When you use the settings helper's ``objects`` attribute shortcut or ``get_object()`` method to retrieve the relevant object, Cogwheels applies some basic validation to the setting value to ensure it is in the correct format, and will also raise a custom exception if the object cannot be imported.

If you define an invalid default value for the setting:

- A ``DefaultValueTypeInvalid`` error is raised if the value is not a string.
- A ``DefaultValueFormatInvalid`` error is raised if the string is not in the correct format.
- A ``DefaultValueNotImportable`` error is raised if attempting to import the module raises an ``ImporError``.
- A ``DefaultValueNotImportable`` with slightly different messaging is raised if attempting to retrieve the object from the module results in an ``AttributeError``.

If a user uses an invalid value as an override in their Django settings:

- A ``OverrideValueTypeInvalid`` error is raised if the value is not a string.
- A ``OverrideValueFormatInvalid`` error is raised if the string is not in the correct format.
- A ``OverrideValueNotImportable`` error is raised if attempting to import the model raises a ``LookupError``.
- A ``OverrideValueNotImportable`` with slightly different messaging is raised if attempting to retrieve the object from the module results in an ``AttributeError``.


Behind the scenes
=================

When you request a model setting value from ``settings`` using:

- ``settings.objects.OBJECT_SETTING_NAME`` or
- ``settings.get_object('OBJECT_SETTING_NAME')``

Cogwheels does the following:

1.  If the requested setting is deprecated, a deprecation warning is raised to prompt users to review their implementation.
2.  Cogwheels looks for a **raw** (string) setting value that it can use to import the object:

    1.  If users of your app have defined an override value in their Django settings using the correct prefix and setting name (e.g. ``YOURAPP_OBJECT_SETTING_NAME``), that value is used.
    2.  If the requested setting is a 'replacement' for a single deprecated setting, Cogwheels also looks in your user's Django settings for override values using the **deprecated** setting name (e.g. ``YOURAPP_DEPRECATED_OBJECT_SETTING_NAME``), and (after raising a helpfully worded deprecation warning) uses that if found. 
    3.  If no override value was found, the default value that you used in ``defaults.py`` is used.

3. The raw value is then checked to ensure that it is a string. If it is not, a helpfully worded ``OverrideValueTypeInvalid`` or ``DefaultValueTypeInvalid`` error is raised.
4. The string value is checked to ensure it matches the expected format (e.g. 'project.app.module.object'). If it does not, a helpfully worded ``OverrideValueFormatInvalid`` or ``DefaultValueFormatInvalid`` error is raised.
5. Cogwheels attempts to import the module using Python's ``importlib.import_module()``, then uses ``getattr`` to attempt to retrieve the object from the module. If either of these steps fail, a helpfully worded ``OverrideValueNotImportable`` or ``DefaultValueNotImportable`` error is raised.

The successfully imported object is cached, so that the steps 2-5 can be bypassed the next time the same setting value is requested.

