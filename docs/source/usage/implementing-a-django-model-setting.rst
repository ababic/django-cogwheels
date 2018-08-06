=====================
Django model settings
=====================

.. contents:: Contents:
    :local:
    :depth: 1


What is a Django model setting?
===============================

A Django model setting is a setting that allows users to swap out a default Django model for a custom one (or an alternative that including in your app).

Setting values must be defined as `model strings`, in the format "app_label.Model".

When you request the model from your app's settings helper, Cogwheels utilises Django's ``django.apps.apps.get_model()`` method to retrieve the relevant Django model, and caches the import to improve the efficiency of repeat requests for the same model.

.. NOTE ::
    When a model setting is overridden:

    - Cogwheels does not prevent the default model from being created or otherwise interfere with your migration history. 
    - So long as the relevant app remains installed, the default model will remain available, and any existing data will remain untouched in the database.
    - No data is migrated to the custom model automatically. If necessary, this will be down to you or your users to implement.
    - The replacement model must be installed in order to be imported successfully (the relevant app must be added to the user's ``INSTALLED_APPS`` setting).


Adding new app settings
=======================

App settings are simply variables with upper-case names, added to your app's ``conf/defaults.py`` module, and Django model settings are no exception. You just have to ensure the model strings you use as default values are correct, and follow the "app_label.Model" format. For example:

.. code-block:: python

    # yourapp/conf/defaults.py

    DOCUMENT_MODEL = "myapp_documents.Document"

    IMAGE_MODEL = "myapp_images.Image"

    MAIN_MENU_MODEL = "myapp_menus.MainMenu"

Users will override these settings by adding override values to their Django settings, like so:

.. code-block:: python

    # usersdjangoproject/settings/base.py

    ...

    # ---------------------------------
    # Overrides for ``your-django-app``
    # ---------------------------------

    YOURAPP_DOCUMENT_MODEL = "media.CustomDocument"

    YOURAPP_IMAGE_MODEL = "media.CustomImage"

    YOURAPP_MAIN_MENU_MODEL = "core.CustomMainMenu"


.. NOTE::
    The `YOURAPP_` prefix used above will differ for you app, depending on your app's name, and where your settings helper is defined. To find out the prefix for your app, or to change it, see: :doc:`/installation/changing-the-namespace-prefix`.


Retrieving app setting values
=============================

You can use the settings helper's ``models`` attribute shortcut or ``get_model()`` method to retrieve model classes referenced by Django model setting values. For example:

.. code-block:: console

    > from yourapp.conf import settings

    > settings.models.MAIN_MENU_MODEL
    yourapp.models.MainMenu

    > settings.get_model("MAIN_MENU_MODEL")
    yourapp.models.MainMenu


Validation and error handling
=============================

When you use the settings helper's ``models`` attribute shortcut or ``get_model()`` method to retrieve the Django model, Cogwheels applies some basic validation to the setting value to ensure it is in the correct format, and will also raise a custom exception if the model cannot be imported.

If you define an invalid default value for the setting:

- A ``DefaultValueTypeInvalid`` error is raised if the value is not a string.
- A ``DefaultValueFormatInvalid`` error is raised if the string is not in the correct format.
- A ``DefaultValueNotImportable`` error is raised if attempting to import the model results in a ``LookupError``.

If a user uses an invalid value as an override in their Django settings:

- A ``OverrideValueTypeInvalid`` error is raised if the value is not a string.
- A ``OverrideValueFormatInvalid`` error is raised if the string is not in the correct format.
- A ``OverrideValueNotImportable`` error is raised if attempting to import the model results in a ``LookupError``.


Accessing the 'model string' value
----------------------------------

In cases where you only need the string value, instead of the model class itself, you can reference the setting as a direct attribute of the settings helper, or use the ``get()`` method:

.. code-block:: console

    > from yourapp.conf import settings

    > settings.MAIN_MENU_MODEL
    "yourapp.MainMenu"

    > settings.get("MAIN_MENU_MODEL")
    "yourapp.models.MainMenu"

However, doing so **will not invoke the built-in validation and error handling behaviour** provided by the ``models`` shortcut or ``get_model()`` method. 


Behind the scenes
=================

When you request a model setting value from ``settings`` using:

- ``settings.models.MODEL_SETTING_NAME`` or
- ``settings.get_model('MODEL_SETTING_NAME')``

Cogwheels does the following:

1.  If the requested setting is deprecated, a helpfully worded ``DeprecationWarning`` is raised to prompt users to review their implementation.
2.  Cogwheels looks for a **raw** (string) setting value that it can use to import the model:

    1.  If users of your app have defined an override value in their Django settings using the correct prefix and setting name (e.g. ``YOURAPP_MODEL_SETTING_NAME``), that value is used.
    2.  If the requested setting is a 'replacement' for a single deprecated setting, Cogwheels also looks in your user's Django settings for override values using the **deprecated** setting name (e.g. ``YOURAPP_DEPRECATED_MODEL_SETTING_NAME``), and (after raising a helpfully worded ``DeprecationWarning``) uses that if found. 
    3.  If no override value was found, the default value that you used in ``defaults.py`` is used.

3. The raw value is then checked to ensure that it is a string. If it is not, a helpfully worded ``OverrideValueTypeInvalid`` or ``DefaultValueTypeInvalid`` error is raised.
4. The string value is checked to ensure it it matches the expected format (e.g. 'app_label.Model'). If it does not, a helpfully worded ``OverrideValueFormatInvalid`` or ``DefaultValueFormatInvalid`` error is raised.
5. Cogwheels attempts to import the model using Django's ``django.apps.apps.get_model()`` method. If the import fails, a helpfully worded ``OverrideValueNotImportable`` or ``DefaultValueNotImportable`` error is raised.

The successfully imported model is cached, so that the steps 2-5 can be bypassed the next time the same setting value is requested.
