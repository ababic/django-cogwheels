=====
Usage
=====

.. contents:: Contents:
    :local:
    :depth: 1


App settings: The basics
========================

App settings in Cogwheels all work in a similar way, regardless of what type of value you are using:

1.  App settings are simply variables with upper-case names, added to your app's ``conf/defaults.py`` module with a default value, e.g.
    
    .. code-block:: python

        # yourapp/conf/defaults.py

        SETTING_NAME = "default-value"

2.  Within your project, rather than importing variables from ``defaults``, you import a `settings helper` object, and query that for your setting values instead, e.g.
    
    .. code-block:: console

        > from yourapp.conf import settings
        
        # Referencing as a direct attribute (recommended)
        > settings.SETTING_NAME   
        "default-value"

        # Using the get() method
        > settings.get('SETTING_NAME') 
        "default-value"
    
3.  When you request a setting value from the helper, it checks your user's Django settings modules for override values, and if found, uses those values instead of the default.

    .. NOTE::
        Users define overrides using *prefixed* setting names. The prefix used in the example below is **YOURAPP_** because of where the ``conf`` app is defined in the example, but this will differ for your app. For more information see: :ref:`finding-the-namespace-prefix`.

    .. code-block:: python

        # userdjangoproject/settings/base.py

        YOURAPP_SETTING_NAME = "custom-value"

    .. code-block:: console

        > from yourapp.conf import settings

        # Referencing as a direct attribute (recommended)
        > settings.SETTING_NAME
        "custom-value"

        # Using the get() method
        > settings.get('SETTING_NAME')
        "custom-value"

**For more information, see:**

- :doc:`implementing-a-regular-setting`


Retrieving Django models and other Python objects from setting values
=====================================================================

Sometimes settings refer to Python objects such as Django models, classes, functions or modules, so the settings helper has built-in functionality to help you retrieve those objects (complete with validation / error reporting, and caching to improve efficiency of repeat requests). e.g.

.. code-block:: python

    # yourapp/conf/defaults.py

    # The Django model to use for main menus
    MAIN_MENU_MODEL = "yourapp.MainMenu"

    # A Python module that provides a generic API for working with an underlying
    # search engine (e.g. Whoosh, Elasticsearch, PostgreSQL)
    PAGE_SEARCH_BACKEND = "yourapp.search.backends.whoosh"

    # The Django form to use in the "Add main menu" interface
    MAIN_MENU_ADD_FORM = "yourapp.menus.forms.MainMenuAddForm"

    # A Python method that validates a username
    USERNAME_VALIDATOR = "yourapp.accounts.validators.username_default"

You can use the helper's ``models`` attribute shortcut or ``get_model()`` method to retrieve Django models: 

.. code-block:: console

    > from yourapp.conf import settings

    > settings.models.MAIN_MENU_MODEL
    yourapp.models.MainMenu

    > settings.get_model("MAIN_MENU_MODEL")
    yourapp.models.MainMenu

You can use the helper's ``modules`` attribute shortcut or ``get_module()`` method to retrieve Python modules:

.. code-block:: console

    > from yourapp.conf import settings

    > settings.modules.PAGE_SEARCH_BACKEND
    <module 'yourapp.search.backends.whoosh' from '/system/path/to/your-app/yourapp/search/backends.whoosh.py'>

    > settings.get_module("PAGE_SEARCH_BACKEND")
    <module 'yourapp.search.backends.whoosh' from '/system/path/to/your-app/yourapp/search/backends.whoosh.py'>

And, you can use the helper's ``objects`` attribute shortcut or ``get_object()`` method to retrieve other Python objects, such as classes or functions:

.. code-block:: console

    > from yourapp.conf import settings
    
    > settings.objects.MAIN_MENU_ADD_FORM
    yourapp.forms.MainMenuAddForm

    > settings.get_object("MAIN_MENU_ADD_FORM")
    yourapp.forms.MainMenuAddForm

    > settings.objects.USERNAME_VALIDATOR
    <function yourapp.accounts.validators.username.default(username, obj)>

    > settings.get_object("USERNAME_VALIDATOR")
    <function yourapp.accounts.validators.username.default(username, obj)>


**For more information, see:**

- :doc:`implementing-a-django-model-setting`
- :doc:`implementing-a-python-object-setting`
- :doc:`implementing-a-python-module-setting`
    

.. _finding-the-namespace-prefix:

Finding the settings namespace prefix for your app
==================================================

In order to override app settings, your users will add override values to their project's Django settings using **prefixed** setting names.

This namespacing of settings is important, as it helps users of your app to remember which app their settings apply to, and also helps to prevent setting name clashes between apps.

Coghwheels uses the Python path of your ``conf`` app to generate a unique prefix for each settings helper. You can find out what this prefix is by calling the settings helper's ``get_prefix()`` method, like so:

.. code-block:: console

    > from yourapp.conf import settings

    > settings.get_prefix()
    "YOURAPP_"

So, to override settings for this particular app, users must prefix their setting names with **YOURAPP_**, like so:

.. code-block:: python

    # userdjangoproject/settings/base.py

    ...

    # ---------------------------------
    # Overrides for ``your-django-app``
    # ---------------------------------

    # Overrides: yourapp.conf.settings.ADMIN_UI_PROJECT_NAME
    YOURAPP_ADMIN_UI_PROJECT_NAME = "The Best Project Ever!"

    # Overrides: yourapp.conf.settings.SEND_EMAILS_ON_DISPATCH
    YOURAPP_SEND_EMAILS_ON_DISPATCH = False

    # Overrides: yourapp.conf.settings.MAIN_MENU_MAX_DEPTH
    YOURAPP_MAIN_MENU_MAX_DEPTH = 1


If you are unhappy with default prefix chosen by Cogwheels, you can easily specficy your own by adding a ``prefix`` attribute to your settings helper class. e.g.

.. code-block:: python

    # yourapp/conf/settings.py
    
    class MyAppSettingsHelper(BaseAppSettingsHelper):
        prefix = 'custom'


Coghweels will automatically translate this string into upper-case if a lower or mixed case string is provided, and will also add the underscore when necessary, so you don't have to include it yourself. 

With the above changes applied, ``get_prefix()`` will now return the following:

.. code-block:: console

    > from yourapp.conf import settings
    > settings.get_prefix()
    'CUSTOM_'


Deprecation handling for app settings
=====================================

Another major benefit of using Cogwheels is it's built-in support for app setting deprecation. Whether you are renaming or replacing a setting, or simply removing it, Cogwheels helps to take some of the pain out of deprecation by:

- Allowing you to clearly and explicitly express the deprecation status of all your app settings, using common definitions
- Automatically raising sensibly worded deprecation warnings when setting values are requested
- Allowing you to easily access deprecated setting values, so that you can continue to support deprecated behaviour until the end of the deprecation period.

**For more information, see:**

- :doc:`setting-deprecation/index`


Step-by-step guides
===================

.. toctree::
    :maxdepth: 1

    implementing-a-regular-setting
    implementing-a-django-model-setting
    implementing-a-python-module-setting
    implementing-a-python-object-setting
    setting-deprecation/index



