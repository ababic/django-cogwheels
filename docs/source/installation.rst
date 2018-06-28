==================
Installation guide
==================


.. contents::
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


Defining settings for your app
==============================


1.  From the console, ``cd`` into your project's root app directory, for example:
    
    .. code-block:: console

        $ cd your-django-app/yourapp/


2.  Use Django's ``startapp`` command to create a ``conf`` app, using the official cogwheels app template:

    .. code-block:: console

        $ django-admin.py startapp conf --template=https://github.com/ababic/cogwheels-conf-app/zipball/master


3.  Any overridable settings you want to support in your app must to be added to the ``defaults.py`` module in the newly ``conf`` directory.

    **DO:**

    - Use upper-case names for setting names
    - Feel free to use any basic Python type as a value (e.g. string, int, boolean, float, list, tuple, dict)

    **DON'T:**

    - Prefix setting names with ``"YOURAPP_"`` or similar (that is not necessary here)
    - Put all your configuration in one giant dictionary setting (that's just lazy!)
    - Use value types that require import statements to define, unless it's a well-known Python built-in like ``OrderedDict``

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


Using setting values in your app
================================

To use setting values in your app, simply import the settings module wherever it is needed, and reference settings as attributes of the module.


Getting 'raw' setting value
---------------------------

Reference a setting as a direct attribute of the setting module will return values **exactly** as they are defined in ``defaults.py``, or by the user in their Django settings (no transformation is applied).

.. code-block:: console

    >>> from yourproject.conf import settings

    >>> settings.MAX_ITEMS_PER_ORDER
    5
    >>> type(settings.MAX_ITEMS_PER_ORDER)
    int

    >>> settings.ORDER_ITEM_MODEL
    'yourproject.SimpleOrderItem'
    >>> type(settings.ORDER_ITEM_MODEL)
    str

    >>> settings.DISCOUNTS_BACKEND
    'yourproject.discount_backends.simple'
    >>> type(settings.DISCOUNTS_BACKEND)
    str

    >>> settings.ORDER_FORM_CLASS
    'yourproject.forms.OrderForm'
    >>> type(settings.ORDER_FORM_CLASS)
    str


Getting Django models from setting values
-----------------------------------------

For settings that refer to Django models, you can use the settings module's ``models`` attribute to access model classes themselves. For example: 

.. code-block:: console

    >>> from yourproject.conf import settings

    >>> settings.models.ORDER_ITEM_MODEL
    yourproject.models.SimpleOrderItem

    >>> from django.db.models import Model
    >>> issubclass(settings.models.ORDER_ITEM_MODEL, Model)
    True
    
Behind the scenes, Django's ``django.apps.apps.get_model()`` method is called, and the result is cached so that repeat requests for the same model are handled quickly and efficiently.


Getting Python modules from setting values
------------------------------------------

For settings that refer to Python modules, you can use the settings module's ``modules`` attribute to access the modules themselves. For example:
    
.. code-block:: console

    >>> from yourproject.conf import settings

    >>> settings.modules.DISCOUNTS_BACKEND
    <module 'yourproject.discount_backends.simple' from '/system/path/to/your-django-project/yourproject/discount_backends/simple.py'>

    >>> type(settings.modules.DISCOUNTS_BACKEND)
    module

Behind the scenes, Python's ``importlib.import_module()`` method is called, and the result is cached so that repeat requests for same module are handled quickly and efficiently.


Getting classes, functions and other Python objects from setting values
-----------------------------------------------------------------------

For settings that refer to classes, functions, or other importable python objects, you can use the settings module's ``objects`` attribute to access those objects. For example:

.. code-block:: console

    >>> from yourproject.conf import settings

    >>> settings.objects.ORDER_FORM_CLASS
    yourproject.forms.OrderForm

    >>> from django.forms import Form
    >>> issubclass(settings.objects.ORDER_FORM_CLASS, Form)
    True

Behind the scenes, Python's ``importlib.import_module()`` method is called, and the result is cached so that repeat requests for same object are handled quickly and efficiently.


Updating ``setup.py``
=====================

If your app is in the Python Package Index (PyPi), it's likely that it has a ``setup.py`` file somewhere. If you're plan to use ``django-cogwheels``, you'll need to ensure ``django-cogwheels`` is added to the ``install_requires`` list that is passed to the ``setup()`` method in that file. For example:

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


Additional implementation options
=================================


Getting rid of the ``conf`` app
-------------------------------

Everyone has their own preferences for how they structure their projects, and that's all well and good. 

There's no requirement for ``defaults.py`` and ``settings.py`` to be kept inside a ``conf`` app - it is only a recommendation. As long as you keep the two files in the same directory, things should work fine 'out of the box'.


Moving other configurational 'stuff' to the ``conf`` app
--------------------------------------------------------

If you're sticking with the ``conf`` app, it might make sense for you to move other 'configurational' things into there too. For example, in the ``conf`` app for wagtailmenus_, there's a ``constants.py`` file for defining some fixed values that are used app-wide, and the ``apps.py`` module that normally resides in an app's root directory has been moved to the ``conf`` app also.

.. _wagtailmenus: https://github.com/rkhleics/wagtailmenus/tree/master/wagtailmenus


Having ``defaults.py`` and ``settings.py`` in separate directories
------------------------------------------------------------------

This is supported. However, you will need to set the ``defaults_path`` attribute on your ``SettingsHelper`` class, so that it knows where to find the default values. For example:

.. code-block:: python

    # yourapp/settings.py

    class MyAppSettingsHelper(BaseAppSettingsHelper):
        defaults_path = 'yourapp.some_other_place.defaults'
