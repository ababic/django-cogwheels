======================
Python module settings
======================

.. contents:: Contents:
    :local:
    :depth: 2


.. _module_setting_definition:

Adding a new app setting
========================

TBC


.. _module_setting_access:

Using the setting in your code
==============================

For settings that refer to Python modules, you can use the settings module's ``modules`` attribute to access the modules themselves. For example:
    
.. code-block:: console

    > from yourproject.conf import settings

    > settings.modules.DISCOUNTS_BACKEND
    <module 'yourproject.discount_backends.simple' from '/system/path/to/your-django-project/yourproject/discount_backends/simple.py'>

    > type(settings.modules.DISCOUNTS_BACKEND)
    module

.. NOTE ::
    ``settings.modules.SETTING_NAME`` is equivalent to doing ``settings.get_module('SETTING_NAME')``, only the former will raise an ``AttributeError`` if the setting name is invalid, whereas ``get()`` will raise an  ``ImproperlyConfigured`` exception.


.. _module_setting_process:

Behind the scenes
=================

When you request a model setting value from ``settings`` using:

- ``settings.modules.MODULE_SETTING_NAME`` or
- ``settings.get_module('MODULE_SETTING_NAME')``

Cogwheels does the following:

1.  If the requested setting is deprecated, a helpfully worded ``DeprecationWarning`` is raised to prompt users to review their implementation.
2.  Cogweels looks for a **raw** (string) setting value that it can use to import the module:

    1.  If users of your app have defined an override value in their Django settings using the correct prefix and setting name (e.g. ``YOURAPP_MODULE_SETTING_NAME``), that value is used.
    2.  If the requested setting is a 'replacement' for a single deprecated setting, Cogwheels also looks in your user's Django settings for override values using the **deprecated** setting name (e.g. ``YOURAPP_DEPRECATED_MODULE_SETTING_NAME``), and (after raising a helpfully worded ``DeprecationWarning``) uses that if found. 
    3.  If no override value was found, the default value that you used in ``defaults.py`` is used.

3. The raw value is then checked to ensure that it is a string. If it is not, a helpfully worded ``OverrideValueTypeInvalid`` or ``DefaultValueTypeInvalid`` error is raised.
4. Cogwheels attempts to import the module using Python's ``importlib.import_module()``. If the import fails, a helpfully worded ``OverrideValueNotImportable`` or ``DefaultValueNotImportable`` error is raised.

The successfully imported module is cached, so that the steps 2-4 can be bypassed the next time the same setting value is requested.
