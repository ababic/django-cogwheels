.. image:: https://raw.githubusercontent.com/ababic/django-cogwheels/master/docs/source/_static/django-cogwheels-logo.png
    :alt: Django Cogwheels

.. image:: https://travis-ci.com/ababic/django-cogwheels.svg?branch=master
    :alt: Build Status
    :target: https://travis-ci.com/ababic/django-cogwheels

.. image:: https://codecov.io/gh/ababic/django-cogwheels/branch/master/graph/badge.svg
    :alt: Code coverage
    :target: https://codecov.io/gh/ababic/django-cogwheels

======================
About Django Cogwheels
======================

.. caution:: 
    Cogwheels is still in the early stages of development, and isn't recommended for use in production projects just yet.

A handy API to allow you to more easily offer and maintain 'user overridable settings' in your Django package, framework or reuseable app.

Give your users the flexibility they deserve, and allow them to:

- Override basic python type values such as: strings, integers, booleans, decimals and floats.
- Override structured python type values such as: lists, tuples and dictionaries.
- Use custom Django models in place of the ones you provide.
- Use custom python classes, objects or entire modules in place of you provide.


Goodness for you and other maintainers
======================================

- A stable, documented, standardised approach for implementing overridable app-specific settings.
- Cached imports for speedy access to models, modules and other overridable objects.
- Clearly define and communicate the deprecation status of app settings, giving you the flexibility to rename, replace or flag settings for removal over your project's lifecycle. User overrides defined using old setting names remain available to you, allowing you to continue to support them during the deprecation period.
- Helpful, consistent error messages when default values provided for models, modules or other overridable object settings are invalid.
- Plays nicely with Django's test framework (subscribes to Django's ``setting_changed`` signal, so that cached values are cleared when ``override_settings`` is used).


Goodness for your users
=======================

- Helpful, consistent error messages when their Model, Class, method or module override settings are incorrectly formatted, or cannot be imported.
- Helpful, consistent deprecation warnings when they are overriding a setting that has been renamed, replaced or flagged for removal.


Quick start guide
=================

1.  Install the package using pip: 

    .. code-block:: console

        pip install django-cogwheels

2.  `cd` into your project's root app directory:
    
    .. code-block:: console

        cd your-django-project/yourproject/

3.  Create a ``conf`` app using the cogwheels Django app template:

    .. code-block:: console

        django-admin.py startapp conf --template=https://github.com/ababic/cogwheels-conf-app/zipball/master

4.  Open up ``yourproject/conf/defaults.py``, and add your setting values like so:

    .. code-block:: python

        # You can add settings for any type of value
        MAX_ITEMS_PER_ORDER = 5

        # For settings that refer to models, use a string in the format 'app_name.Model'
        ORDER_ITEM_MODEL = 'yourproject.SimpleOrderItem'

        # For settings that refer to a python module, use an 'import path' string, like so:
        DISCOUNTS_BACKEND = 'yourproject.discount_backends.simple'

        # For settings that refer to classes, methods, or other python objects from a
        # python module, use an 'object import path' string, like so:
        ORDER_FORM_CLASS = 'yourproject.forms.OrderForm'

        
5.  To use setting values in your app, simply import the settings helper, and access them as attributes, like so:

    .. code-block:: console

        >>> from yourproject.conf import settings

        >>> max_items = settings.MAX_ITEMS_PER_ORDER
        5 

        >>> order_item_model_string = settings.ORDER_ITEM_MODEL
        'yourproject.SimpleOrderItem'

        >>> discounts_backend_path = settings.DISCOUNTS_BACKEND
        'yourproject.discount_backends.simple'

        >>> form_class_path = settings.ORDER_FORM_CLASS
        'yourproject.forms.OrderForm'


6.  For settings that refer to Django models, you can use the settings helper's special ``models`` attribute to access model classes themselves, rather than just the string value. For example: 

    .. code-block:: console

        >>> from yourproject.conf import settings

        >>> item_model = settings.models.ORDER_ITEM_MODEL
        yourproject.models.SimpleOrderItem

        >>> obj = item_model(id=1, product='test product', quantity=15)
        >>> obj.save()

        >>> print(item_model.objects.all())
        <QuerySet [<SimpleOrderItem: SimpleOrderItem object (1)>]>

    Behind the scenes, Django's ``django.apps.apps.get_model()`` method is called, and the result is cached so that repeat requests for the same model are handled quickly and efficiently.


7.  For settings that refer to python modules, you can use the settings helper's special ``modules`` attribute to access the modules themselves, instead of an import path string: 
    
    .. code-block:: console

        >>> from yourproject.conf import settings

        >>> discounts_backend = settings.modules.DISCOUNTS_BACKEND
        <module 'yourproject.discount_backends.simple' from '/Users/username/django/projects/your-django-project/yourproject/discount_backends/simple.py'>


    Behind the scenes, python's ``importlib.import_module()`` method is called, and the result is cached so that repeat requests for same module are handled quickly and efficiently.


8.  For settings that refer to classes, functions, or other importable python objects, you can use the settings helper's special ``objects`` attribute to access those objects, instead of an import path string: 

    .. code-block:: console

        >>> from yourproject.conf import settings

        >>> form_class = settings.objects.ORDER_FORM_CLASS
        yourproject.formsOrderForm

        >>> form = form_class(request.POST or None)
        >>> form.is_valid()


    Behind the scenes, python's ``importlib.import_module()`` method is called, and the result is cached so that repeat requests for same object are handled quickly and efficiently.


9.  Users of your app can now override any of the default values by adding alternative values to their project's Django settings module. For example: 

    .. code-block:: python

        # userproject/settings/base.py

        YOURAPP_MAX_ITEMS_PER_ORDER = 2

        YOURAPP_ORDER_ITEM_MODEL = 'userproject_orders.CustomOrderItem'

        YOURAPP_DISCOUNTS_BACKEND = 'userproject.discounts.custom_discount_backend'

        YOURAPP_ORDER_FORM_CLASS = 'userproject.orders.forms.CustomOrderForm'

10. You might may noticed that the above variable names are all prefixed with ``YOURAPP_``. This prefix will differ for your app, depending on the package name. 

    This 'namespacing' of settings is important. Not only does it helps users of your app to remember which app their override settings are for, but it also helps to prevent setting name clashes between apps.

    You can find out what the prefix is for your app by doing:
    
    .. code-block:: console

        >>> from yourproject.conf import settings
        >>> settings.get_prefix()
        'YOURPROJECT_'

    You can change this prefix to whatever you like by setting a ``prefix`` attribute on your settings helper class, like so:

    .. code-block:: python

        # yourapp/conf/settings.py

        ... 

        class MyAppSettingsHelper(BaseAppSettingsHelper):
            prefix = 'CUSTOM'  # No need for a trailing underscore here
        
        ...


    .. code-block:: console

        >>> from yourproject.conf import settings
        >>> settings.get_prefix()
        'CUSTOM_'
        

Compatibility
=============

The current version is tested for compatiblily with the following: 

- Django versions 1.11 to 2.1
- Python versions 3.4 to 3.6
