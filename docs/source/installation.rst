==================
Installation guide
==================

.. contents:: Contents
    :local:
    :depth: 2


Prerequisites
=============

To use Cogwheels in your app, all you need are compatible versions of Python and Django, which you likely have already. The current version is tested for compatibility with:

- Python 3.4 to 3.7
- Django 1.11 to 2.1


Getting the code
================

The recommended way to install Cogwheels is via pip_:

.. code-block:: console

    $ pip install django-cogwheels

To test an upcoming release, you can install the in-development version with the following command:

.. code-block:: console

    $ pip install -e git+https://github.com/ababic/django-cogwheels.git#egg=cogwheels

.. _pip: https://pip.pypa.io/


Adding ``django-cogwheels`` as a dependency
===========================================

If your app is in the Python Package Index (PyPi), it's likely that it has a ``setup.py`` file in the root directory. To use ``django-cogwheels`` to manage your app settings, you'll need to ensure ``django-cogwheels`` is added to the ``install_requires`` list that is passed to the ``setup()`` method in that file. For example:

.. code-block:: python

    # your-django-app/setup.py

    from setuptools import setup

    ...
    
    setup(
        name='your-django-project',
        description="An app that does something super useful.",
        classifiers=(
            "Programming Language :: Python",
            "Programming Language :: Python :: 3",
            "Programming Language :: Python :: 3.4",
            "Programming Language :: Python :: 3.5",
            "Programming Language :: Python :: 3.6",
            "Programming Language :: Python :: 3.7",
            "Framework :: Django",
            "Framework :: Django :: 1.11",
            "Framework :: Django :: 2.0",
            ...
        ),
        install_requires=[
            'some-requirement',
            'some-other-requirement',
            'django-cogwheels',  # ADD THIS HERE!
        ],
        ...
    )


.. _defining_settings:

Defining settings for your app
==============================


1.  From the console, ``cd`` into your project's root app directory, for example:
    
    .. code-block:: console

        $ cd your-django-app/yourapp/


2.  Use Django's ``startapp`` command to create a ``conf`` app, using the official cogwheels app template:

    .. code-block:: console

        $ django-admin.py startapp conf --template=https://github.com/ababic/cogwheels-conf-app/zipball/master


3.  Any overridable settings you want to support in your app simply need adding as standard variables to the newly created ``conf/defaults.py`` module. Here is some friendly advice:

    - The variable names for your settings should be in upper case (e.g. ``SOME_SETTING``).
    - There's no need to prefix setting names with ``"YOURAPP_"`` or similar here. Cogwheels will take care of adding this prefix automatically when it is useful. 
    - You can use any native Python type as a value (e.g. string, int, boolean, float, list, tuple, dict, date, time), but try to stick to well-known types that are easy for your app's users to define when they want to override something.
    - It's absolutely fine to use dictionaries to allow overriding of more complicated features, but try not to group together unrelated bits of configuration into large dictionaries, when they would make more sense as separate settings. 

    Your setting definitions should look something like this:

    .. code-block:: python

        # your-django-app/yourapp/conf/defaults.py

        ...

        MAX_ITEMS_PER_ORDER = 5

        SEND_ORDER_CONFIRMATION_EMAILS = True

        # For settings that refer to Django models, the default value should be a string
        # in the format 'app_name.Model', e.g.:

        ORDER_ITEM_MODEL = 'yourproject.SimpleOrderItem'

        # For settings that refer to Python modules, the default value should be an
        # 'import path' string, e.g.:

        DISCOUNTS_BACKEND = 'yourproject.discount_backends.simple'

        # For settings that refer to classes, methods, or other importable Python
        # objects, the default value should be an 'object import path' string, e.g.:

        ORDER_FORM_CLASS = 'yourproject.forms.OrderForm'

.. NOTE::

    Ready to start using setting values in your code? See: :doc:`using-setting-values` 


Optional configuration
======================


Changing the setting namespace prefix
-------------------------------------

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

    >>> from yourproject.conf import settings
    >>> settings.get_prefix()
    'YOURPROJECT_'

You can change this prefix to whatever you like by setting the ``prefix`` attribute on your settings helper class. For example, this:

.. code-block:: python

    # yourapp/conf/settings.py
    
    class MyAppSettingsHelper(BaseAppSettingsHelper):
        prefix = 'CUSTOM'  # No need for a trailing underscore here

Would result in this:

.. code-block:: console

    >>> from yourproject.conf import settings
    >>> settings.get_prefix()
    'CUSTOM_'


Moving more 'configurational' stuff to the ``conf`` app
-------------------------------------------------------

Since you now have a ``conf`` app, it might make sense to move other 'configurational' things into there too.

For example, in the ``conf`` app for wagtailmenus_, there's a ``constants.py`` file for defining some fixed values that are used app-wide, and the ``apps.py`` module that normally resides in an app's root directory has also been moved to the ``conf``.

.. _wagtailmenus: https://github.com/rkhleics/wagtailmenus/tree/master/wagtailmenus


Ditching the ``conf`` app
-------------------------

Everyone has their own preferences for how they structure their projects, and that's all well and good. 

There's no requirement for ``defaults.py`` and ``settings.py`` to be kept inside a ``conf`` app - it is only a recommendation. As long as you keep the two files in the same directory, things should work fine 'out of the box'.


Using different locations for ``defaults.py`` and ``settings.py``
-----------------------------------------------------------------

This is supported. However, you will need to set the ``defaults_path`` attribute on your ``SettingsHelper`` class, so that it knows where to find the default values. For example:

.. code-block:: python

    # yourapp/settings.py

    class MyAppSettingsHelper(BaseAppSettingsHelper):
        defaults_path = 'yourapp.some_other_place.defaults'
