===========
Usage guide
===========

.. contents:: Contents:
    :local:
    :depth: 1


Creating and using app settings
===============================

App settings in Cogwheels all work in a very similar fashion, regardless of what type of value you are using:

1.  App settings are simply variables with upper-case names, added to your app's ``conf/defaults.py`` module with a default value, e.g.
    
    .. code-block:: python

        # yourapp/conf/defaults.py

        SETTING_NAME = "default-value"

2.  Instead of importing variables from the ``defaults`` module directly, you import a `settings helper` object, and query that for your setting values instead, e.g.
    
    .. code-block:: console

        > from yourapp.conf import settings
        
        # Referencing as a direct attribute (recommended)
        > settings.SETTING_NAME   
        "default-value"

        # Using the get() method
        > settings.get('SETTING_NAME') 
        "default-value"
    
3.  When you request a setting value from the helper, it checks your user's Django settings module for an override value using a prefixed version of the setting name (To find out or change the prefix for your app, see :doc:`/installation/changing-the-namespace-prefix`). If found, the override value will be returned instead of the default.

    .. code-block:: python

        # usersdjangoproject/settings/base.py

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
- :doc:`/installation/changing-the-namespace-prefix`


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
    

Deprecation handling for app settings
=====================================

Another major benefit of using Cogwheels is it's built-in support for app setting deprecation. Whether you are renaming or replacing a setting, or simply removing it, Cogwheels helps to take some of the pain out of deprecation by:

- Allowing you to clearly and explicitly express the deprecation status of all your app settings, using common definitions
- Automatically raising sensibly worded deprecation warnings when setting values are requested
- Allowing you to easily access deprecated setting values, so that you can continue to support deprecated behaviour until the end of the deprecation period.

**For more information, see:**

- :doc:`setting-deprecation/index`


Setting implementation guides
=============================

.. toctree::
    :maxdepth: 1

    implementing-a-regular-setting
    implementing-a-django-model-setting
    implementing-a-python-module-setting
    implementing-a-python-object-setting


Other guides
============

.. toctree::
    :maxdepth: 2
    
    setting-deprecation/index







