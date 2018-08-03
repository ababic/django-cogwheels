=====================================
Changing the setting namespace prefix
=====================================

Users wanting to override setting values in their project's Django settings will do so using prefixed setting names, rather than using the exact same names you used in ``defaults.py``.  For example:

.. code-block:: python

    # myproject/settings/base.py

    ...

    # ---------------------------------
    # Overrides for ``your-django-app``
    # ---------------------------------

    YOURAPP_MAX_ITEMS_PER_ORDER = 2
    YOURAPP_ORDER_ITEM_MODEL = 'userproject_orders.CustomOrderItem'
    YOURAPP_DISCOUNTS_BACKEND = 'userproject.discounts.custom_discount_backend'
    YOURAPP_ORDER_FORM_CLASS = 'userproject.orders.forms.CustomOrderForm'

This namespacing of settings is important, as not only does it help users of your app to remember which app their settings apply to, but it also helps to prevent setting name clashes between apps.

You can find out the correct prefix for any given settings module by calling it's ``get_prefix()`` method, like so:
    
.. code-block:: console

    > from yourproject.conf import settings
    > settings.get_prefix()
    'YOURPROJECT_'

You can change this prefix to whatever you like by setting the ``prefix`` attribute on your settings helper class. For example, this:

.. code-block:: python

    # yourapp/conf/settings.py
    
    class MyAppSettingsHelper(BaseAppSettingsHelper):
        prefix = 'CUSTOM'  # No need for a trailing underscore here

Would result in this:

.. code-block:: console

    > from yourproject.conf import settings
    > settings.get_prefix()
    'CUSTOM_'
