=====================================
Overriding default app setting values
=====================================

Once you have configured Cogwheels for your app and packaged the changes into a new release, users of your app should be able override any of the default values by adding alternative values to their project's Django settings module. For example: 

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


You have probably noticed that the above setting names are all prefixed with `YOURAPP_``, which isn't how they are defined in the ``defaults.py`` module. This namespacing of settings is important, as it helps users of your app to remember which app their settings apply to, and also helps to prevent setting name clashes between apps.

If you're unsure what the prefix is for your app, you can use the settings module's ``get_prefix()`` method to find out. For example:
    
.. code-block:: console

    >>> from yourproject.conf import settings
    >>> settings.get_prefix()
    'YOURPROJECT_'

.. sealso ::

    :ref:`raw_value_process`
