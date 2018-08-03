================
Regular settings
================

Any setting that allows a user to override a simple Python type value is classed as a 'regular' setting. Cogweels doesn't limit the type of values you can use, but it's recommended that your try to stick to well-known types that are easy for your app's users to define when they want to override something.

When you request a value for a 'regular' setting from your app's settings module, it returns a pointer to the exact same value in memory - no copying or further manipulation of the value takes place. For example:

If no override value is found, the default value (added in ``conf/defaults.py``) is returned:

.. code-block:: console

    > from yourproject.conf import settings
    > from yourproject.conf import defaults

    > settings.SETTING_NAME
    'default-value'

    > settings.SETTING_NAME is defaults.SETTING_NAME
    True

If a user overrides the setting by adding a value to their Django settings, that exact value is returned:

.. code-block:: python
    
    # userproject/settings/base.py

    YOURAPP_SETTING_NAME = 'override-value'

.. code-block:: console

    > from yourproject.conf import settings
    > from django.conf import settings as django_settings

    > settings.SETTING_NAME
    'override-value'

    > settings.SETTING_NAME is django_settings.YOURAPP_SETTING_NAME
    True





.. contents:: Contents:
    :local:
    :depth: 1


.. _regular_setting_definition:

Adding an app setting
=====================

Adding a to add it to ``conf/defaults.py`` with your preferred default value. The following 

.. code-block:: python
    :caption: yourapp/conf/defaults.py
    
    ITEM_LABEL = "Item"

    MAX_ITEMS_PER_ORDER = 3

    SEND_DISPATCH_EMAILS = True

    STUFF_ROBOTS_SAY = [
        "Beep",
        "Boop",
        "Bleeeep",
        "Prepare for extermination!",
    ]

    APP_FONTAWESOME_ICONS = {
        'alert': 'fa-bell',
        'celebration': 'fa-cake',
        'fast': 'fa-bolt',
    }

    OPTION_FIELD_CHOICES = (
        ('one', 'Option one'),
        ('two', 'Option two'),
        ('three', 'Option three'),
    )


.. code-block:: python

    # userproject/settings/base.py

    ...

    # ---------------------------------
    # Overrides for ``your-django-app``
    # ---------------------------------

    YOURAPP_MAX_ITEMS_PER_ORDER = 2
    YOURAPP_ORDER_ITEM_MODEL = 'userproject_orders.CustomOrderItem'
    YOURAPP_DISCOUNTS_BACKEND = 'userproject.discounts.custom_discount_backend'
    YOURAPP_ORDER_FORM_CLASS = 'userproject.orders.forms.CustomOrderForm'


.. _regular_setting_access:

Using the setting in your code
==============================

Referencing a setting as a direct attribute of the setting module will return values **exactly** as they are defined in ``defaults.py``, or by the user in their Django settings (no transformation is applied).

.. code-block:: console

    > from yourproject.conf import settings

    > settings.MAX_ITEMS_PER_ORDER
    5

    > type(settings.MAX_ITEMS_PER_ORDER)
    int

    > settings.ORDER_ITEM_MODEL
    'yourproject.SimpleOrderItem'

    > type(settings.ORDER_ITEM_MODEL)
    str

    > settings.DISCOUNTS_BACKEND
    'yourproject.discount_backends.simple'

    > type(settings.DISCOUNTS_BACKEND)
    str

    > settings.ORDER_FORM_CLASS
    'yourproject.forms.OrderForm'

    > type(settings.ORDER_FORM_CLASS)
    str

.. NOTE ::
    ``settings.SETTING_NAME`` is equivalent to doing ``settings.get('SETTING_NAME')``, only the former will raise an ``AttributeError`` if the setting name is invalid, whereas ``get()`` will raise an ``ImproperlyConfigured`` exception.


.. _regular_setting_process:

Behind the scenes
=================

When you request a regular setting value from ``settings`` using:

- ``settings.REGULAR_SETTING_NAME`` or
- ``settings.get('REGULAR_SETTING_NAME')``

Cogwheels does the following:

1.  If the requested setting is deprecated, a helpfully worded ``DeprecationWarning`` is raised to prompt users to review their implementation.
2.  If users of your app have defined an override value in their Django settings using the correct prefix and setting name (e.g. ``YOURAPP_REGULAR_SETTING_NAME``), that value is returned.
3.  If the requested setting is a 'replacement' for a single deprecated setting, Cogwheels also looks in your user's Django settings for override values using the **deprecated** setting name (e.g. ``YOURAPP_DEPRECATED_REGULAR_SETTING_NAME``), and (after raising a helpfully worded ``DeprecationWarning``) returns that if found. 
4.  If no override value was found, the default value that you used in ``defaults.py`` is returned.

The setting value is also cached, so that steps 2-4 can be bypassed the next time the same setting value is requested.
