======================
Python module settings
======================

A Python module setting is a setting that allows users to swap out an entire Python module for a custom one (or an alternative that is available within your app).

Setting values must be defined as Python import path strings (e.g. "project.app.module").

When you request the module from your app's settings helper, Cogwheels utilises Python's ``importlib.import_module()`` to import the module, and caches the result to improve the efficiency of repeat requests for the same module.


Adding a new app setting
========================

App settings are simply variables with upper-case names, added to your app's ``conf/defaults.py`` module, and Python module settings are no exception. You just have to ensure the import path strings you use as default values are correct. For example:

.. code-block:: python

    # yourapp/conf/defaults.py

    # A Python module that provides a generic API for working with an underlying
    # search engine (e.g. Whoosh, Elasticsearch, PostgreSQL)
    PAGE_SEARCH_BACKEND = "yourapp.search.backends.whoosh"

Users will override this setting by adding override values to their Django settings, like so:

.. code-block:: python

    # userdjangoproject/settings/base.py

    ...
    
    # ---------------------------------
    # Overrides for ``your-django-app``
    # ---------------------------------

    # We like PostgreSQL, so we'll use the built-in postgres backend 
    YOURAPP_PAGE_SEARCH_BACKEND = 'yourapp.search.backends.postgres'

.. NOTE::
    Users define overrides using *prefixed* setting names. The prefix used in the example above is **YOURAPP_** because of where the ``conf`` app is defined in the example, but this will differ for your app. For more information see: :ref:`finding-the-namespace-prefix`.


Retrieving the app setting value
================================

You can use the settings helper's ``modules`` attribute shortcut or ``get_module()`` method to retrieve the Python module referenced by setting values. For example:
    
.. code-block:: console

    > from yourapp.conf import settings

    > settings.modules.DISCOUNTS_BACKEND
    <module 'yourapp.discount_backends.simple' from '/system/path/to/your-django-project/yourapp/discount_backends/simple.py'>

    > settings.get_module("DISCOUNTS_BACKEND")
    <module 'yourapp.discount_backends.simple' from '/system/path/to/your-django-project/yourapp/discount_backends/simple.py'>


Validation and error handling
=============================

When you use the settings helper's ``modules`` attribute shortcut or ``get_module()`` method to retrieve the Python module, Cogwheels applies some basic validation to the setting value to ensure it is a string, and will also raise a custom exception if the object cannot be imported.

If you define an invalid default value for the setting:

- A ``DefaultValueTypeInvalid`` error is raised if the value is not a string.
- A ``DefaultValueNotImportable`` error is raised if attempting to import the module results in an ``ImportError``.

If a user uses an invalid value as an override in their Django settings:

- A ``OverrideValueTypeInvalid`` error is raised if the value is not a string.
- A ``OverrideValueNotImportable`` error is raised if attempting to import the module results in an ``ImportError``.


Behind the scenes
=================

When you request a model setting value from ``settings`` using:

- ``settings.modules.MODULE_SETTING_NAME`` or
- ``settings.get_module('MODULE_SETTING_NAME')``

Cogwheels does the following:

1.  If the requested setting is deprecated, a helpfully worded ``DeprecationWarning`` is raised to prompt users to review their implementation.
2.  Cogwheels looks for a **raw** (string) setting value that it can use to import the module:

    1.  If users of your app have defined an override value in their Django settings using the correct prefix and setting name (e.g. ``YOURAPP_MODULE_SETTING_NAME``), that value is used.
    2.  If the requested setting is a 'replacement' for a single deprecated setting, Cogwheels also looks in your user's Django settings for override values using the **deprecated** setting name (e.g. ``YOURAPP_DEPRECATED_MODULE_SETTING_NAME``), and (after raising a helpfully worded ``DeprecationWarning``) uses that if found. 
    3.  If no override value was found, the default value that you used in ``defaults.py`` is used.

3. The raw value is then checked to ensure that it is a string. If it is not, a helpfully worded ``OverrideValueTypeInvalid`` or ``DefaultValueTypeInvalid`` error is raised.
4. Cogwheels attempts to import the module using Python's ``importlib.import_module()``. If the import fails, a helpfully worded ``OverrideValueNotImportable`` or ``DefaultValueNotImportable`` error is raised.

The successfully imported module is cached, so that the steps 2-4 can be bypassed the next time the same setting value is requested.
