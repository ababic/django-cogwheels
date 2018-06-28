==================
Installation guide
==================


A note to app authors
=====================

As a fellow author of reusable Django apps, I understand that adding new dependencies to your project is probably the last thing you want to do:

- Dependencies can tie you to specific version of Python or Django, making it more difficult to support new versions yourself.
- Dependencies may change over time, and it's another thing you have to keep track of.
- Dependencies very often have dependencies of their own, leading to unnecessarily complicated dependency graphs.

Let me try to offer you a few reassurances:

- **Small and simple**: The current feature-set is stable, and unlikely to grow substantially. And, the app will only ever use officially supported Python and Django features under the hood. As such, compatibility updates should be trivial, and I plan to keep on top of that (I depend on it too)!
- **Deprecation policy**: Unless it would add unreasonable amounts of complexity (or is simply not possible), I will always follow a standard deprecation cycle of two 'feature releases' before adding breaking changes to any documented/public APIs, and full details will always be made available in release notes.
- **No additional dependencies**: Other than requiring a compatible versions of Python and Django, the app currently has no other dependencies, and likely never will.

.. contents::
    :local:
    :depth: 2


Perequisites
============

To use django-cogwheels in your app, all you need is compatible version of Python and Django, which you likely already have. The current version is tested for compatibility with:

- Python 3.4 to 3.7
- Django 1.11 to 2.1


If your app has been added the Python Package Index (PyPi), it's likely that it has a ``setup.py`` file in the root folder. If you plan to use ``django-cogwheels``, you'll need to ensure ``django-cogwheels`` is added to the ``install_requires`` list that is passed to the ``setup()`` method in that file. For example:

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
            'django-cogwheels',  # ADD ME!
        ],
        ...
    )


Getting the code
================

The recommended way to install django-cogwheels is via pip_::

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
    - Feel free to use any built-in basic python type as a value (e.g. string, int, boolean, float, list, tuple, dict)

    **DON'T:**

    - Prefix setting names with 'YOURAPP_' or similar (that isn't necessary here)
    - Put all your configuration in one giant dictionary setting (that's just lazy!)
    - Use value types that require imports statements in order to define (unless it's a well-known Python built-in like ``OrderedDict``)

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

Reference a setting as a direct attribute of the module to access setting values **exactly** as they are defined in ``defaults.py``, or by the user in their Django settings. No tranformation or other magic is applied.

.. code-block:: console

    $ from yourproject.conf import settings

    $ settings.MAX_ITEMS_PER_ORDER
    5
    $ type(settings.MAX_ITEMS_PER_ORDER)
    int

    $ settings.ORDER_ITEM_MODEL
    'yourproject.SimpleOrderItem'
    $ type(settings.ORDER_ITEM_MODEL)
    str

    $ settings.DISCOUNTS_BACKEND
    'yourproject.discount_backends.simple'
    $ type(settings.DISCOUNTS_BACKEND)
    str

    $ settings.ORDER_FORM_CLASS
    'yourproject.forms.OrderForm'
    $ type(settings.ORDER_FORM_CLASS)
    str


Getting Django models from setting values
-----------------------------------------

For settings that refer to Django models, you can use the settings module's ``models`` attribute to access model classes themselves. For example: 

.. code-block:: console

    $ from yourproject.conf import settings

    $ model = settings.models.ORDER_ITEM_MODEL
    yourproject.models.SimpleOrderItem

    $ object = model(id=1, product='test product', quantity=15)
    $ object.save()

    $ print(model.objects.all())
    <QuerySet [<SimpleOrderItem: SimpleOrderItem object (1)>]>
    
Behind the scenes, Django's ``django.apps.apps.get_model()`` method is called, and the result is cached so that repeat requests for the same model are handled quickly and efficiently.


Getting Python modules from setting values
------------------------------------------

For settings that refer to Python modules, you can use the settings module's ``modules`` attribute to access the modules themselves. For example:
    
.. code-block:: console

    $ from yourproject.conf import settings

    $ module = settings.modules.DISCOUNTS_BACKEND
    <module 'yourproject.discount_backends.simple' from '/system/path/to/your-django-project/yourproject/discount_backends/simple.py'>

Behind the scenes, Python's ``importlib.import_module()`` method is called, and the result is cached so that repeat requests for same module are handled quickly and efficiently.


Getting classes, functions and other Python objects from setting values
-----------------------------------------------------------------------

For settings that refer to classes, functions, or other importable python objects, you can use the settings module's ``objects`` attribute to access those objects. For example:

.. code-block:: console

    $ from yourproject.conf import settings

    $ form_class = settings.objects.ORDER_FORM_CLASS
    yourproject.formsOrderForm

    $ form = form_class(data={})
    $ form.is_valid()
    False

Behind the scenes, Python's ``importlib.import_module()`` method is called, and the result is cached so that repeat requests for same object are handled quickly and efficiently.


Frequently asked questions
==========================


Do ``defaults.py`` and ``settings.py`` have to live in a ``conf`` app?
----------------------------------------------------------------------

No. This is just a recommendation. Everyone has their own preferences for how they structure their projects, and that's all well and good. As long as you keep ``defaults.py`` and ``settings.py`` in the same directory, things should work just fine out of the box. 

If you want ``defaults.py`` and ``settings.py`` to live in separate places, ``django-cogwheels`` supports that too. But, you'll have to set the ``defaults_path`` attribute on your settings helper class, so that it knows where to find the default values. For example:

.. code-block:: python

    # yourapp/some_directory/settings.py

    class MyAppSettingsHelper(BaseAppSettingsHelper):
        defaults_path = 'yourapp.some_other_place.defaults'


Are there any example implmentations that I can look at?
--------------------------------------------------------

Sure thing.

You should check out the ``tests`` app within cogwheels itself, which includes lots of examples:
https://github.com/ababic/django-cogwheels/tree/master/cogwheels/tests

``wagtailmenus`` also uses cogwheels to manage it's app settings. See:
https://github.com/rkhleics/wagtailmenus/tree/master/wagtailmenus
