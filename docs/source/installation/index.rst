============
Installation
============

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


Adding Cogwheels as a dependency
================================

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

        ORDER_ITEM_MODEL = 'yourapp.SimpleOrderItem'

        # For settings that refer to Python modules, the default value should be an
        # 'import path' string, e.g.:

        DISCOUNTS_BACKEND = 'yourapp.discount_backends.simple'

        # For settings that refer to classes, methods, or other importable Python
        # objects, the default value should be an 'object import path' string, e.g.:

        ORDER_FORM_CLASS = 'yourapp.forms.OrderForm'


Advanced configuration
======================

.. toctree::
    :maxdepth: 1

    changing-the-namespace-prefix
    utilising-the-conf-app
    removing-the-conf-app
    separating-defaults-and-settings


Other things to consider
========================

.. toctree::
    :maxdepth: 1

    documenting-your-app-settings
    custom-deprecation-warning-classes

