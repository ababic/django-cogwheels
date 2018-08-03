======================
Python object settings
======================

.. contents:: Contents:
    :local:
    :depth: 2


.. _object_setting_definition:

Adding a new app setting
========================

TBC


.. _object_setting_access:

Using the setting in your code
==============================

For settings that refer to classes, functions, or other importable python objects, you can use the settings module's ``objects`` attribute to access those objects. For example:

.. code-block:: console

    > from yourproject.conf import settings

    > settings.objects.ORDER_FORM_CLASS
    yourproject.forms.OrderForm

    > from django.forms import Form
    > issubclass(settings.objects.ORDER_FORM_CLASS, Form)
    True

.. NOTE ::
    ``settings.objects.SETTING_NAME`` is equivalent to doing ``settings.get_object('SETTING_NAME')``, only the former will raise an ``AttributeError`` if the setting name is invalid, whereas ``get()`` will raise an ``ImproperlyConfigured`` exception.


.. _object_setting_process:

Behind the scenes
=================

When you request a model setting value from ``settings`` using:

- ``settings.objects.OBJECT_SETTING_NAME`` or
- ``settings.get_object('OBJECT_SETTING_NAME')``

Cogwheels does the following:

1.  If the requested setting is deprecated, a deprecation warning is raised to prompt users to review their implementation.
2.  Cogweels looks for a **raw** (string) setting value that it can use to import the object:

    1.  If users of your app have defined an override value in their Django settings using the correct prefix and setting name (e.g. ``YOURAPP_OBJECT_SETTING_NAME``), that value is used.
    2.  If the requested setting is a 'replacement' for a single deprecated setting, Cogwheels also looks in your user's Django settings for override values using the **deprecated** setting name (e.g. ``YOURAPP_DEPRECATED_OBJECT_SETTING_NAME``), and (after raising a helpfully worded deprecation warning) uses that if found. 
    3.  If no override value was found, the default value that you used in ``defaults.py`` is used.

3. The raw value is then checked to ensure that it is a string. If it is not, a helpfully worded ``OverrideValueTypeInvalid`` or ``DefaultValueTypeInvalid`` error is raised.
4. The string value is checked to ensure it matches the expected format (e.g. 'project.app.module.object'). If it does not, a helpfully worded ``OverrideValueFormatInvalid`` or ``DefaultValueFormatInvalid`` error is raised.
5. Cogwheels attempts to import the module using Python's ``importlib.import_module()``, then uses ``getattr`` to attempt to retrieve the object from the module. If either of these steps fail, a helpfully worded ``OverrideValueNotImportable`` or ``DefaultValueNotImportable`` error is raised.

The successfully imported object is cached, so that the steps 2-5 can be bypassed the next time the same setting value is requested.

