=====================
Django model settings
=====================

.. contents:: Contents:
    :local:
    :depth: 2


.. _model_setting_definition:

Adding a new app setting
========================

TBC


.. _model_setting_access:

Using the setting in your code
==============================

For settings that refer to Django models, you can use the settings module's ``models`` attribute to access model classes themselves. For example: 

.. code-block:: console

    > from yourproject.conf import settings

    > settings.models.ORDER_ITEM_MODEL
    yourproject.models.SimpleOrderItem

    > from django.db.models import Model
    > issubclass(settings.models.ORDER_ITEM_MODEL, Model)
    True

.. NOTE ::
    ``settings.models.SETTING_NAME`` is equivalent to doing ``settings.get_model('SETTING_NAME')``, only the former will raise an ``AttributeError`` if the setting name is invalid, whereas ``get()`` will raise Django's ``ImproperlyConfigured`` exception.


.. _model_setting_process:

Behind the scenes
=================

When you request a model setting value from ``settings`` using:

- ``settings.models.MODEL_SETTING_NAME`` or
- ``settings.get_model('MODEL_SETTING_NAME')``

Cogwheels does the following:

1.  If the requested setting is deprecated, a helpfully worded ``DeprecationWarning`` is raised to prompt users to review their implementation.
2.  Cogweels looks for a **raw** (string) setting value that it can use to import the model:

    1.  If users of your app have defined an override value in their Django settings using the correct prefix and setting name (e.g. ``YOURAPP_MODEL_SETTING_NAME``), that value is used.
    2.  If the requested setting is a 'replacement' for a single deprecated setting, Cogwheels also looks in your user's Django settings for override values using the **deprecated** setting name (e.g. ``YOURAPP_DEPRECATED_MODEL_SETTING_NAME``), and (after raising a helpfully worded ``DeprecationWarning``) uses that if found. 
    3.  If no override value was found, the default value that you used in ``defaults.py`` is used.

3. The raw value is then checked to ensure that it is a string. If it is not, a helpfully worded ``OverrideValueTypeInvalid`` or ``DefaultValueTypeInvalid`` error is raised.
4. The string value is checked to ensure it it matches the expected format (e.g. 'app_label.Model'). If it does not, a helpfully worded ``OverrideValueFormatInvalid`` or ``DefaultValueFormatInvalid`` error is raised.
5. Cogwheels attempts to import the model using Django's ``django.apps.apps.get_model()`` method. If the import fails, a helpfully worded ``OverrideValueNotImportable`` or ``DefaultValueNotImportable`` error is raised.

The successfully imported model is cached, so that the steps 2-5 can be bypassed the next time the same setting value is requested.
