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


.. _creating_the_conf_app:

Creating a conf app
===================

The ``conf`` app is where you define the available app settings for your app, the default values for those settings, and where you'll import your `settings helper` object from (for retrieving setting values). 

Cogwheels provides a `Django app template <https://github.com/ababic/cogwheels-conf-app/>`_ that you can use for this step, making it quick and easy:

1.  From the console, ``cd`` into your project's root app directory, for example:
    
    .. code-block:: console

        $ cd your-django-app/yourapp/

2.  Use Django's ``startapp`` command to create a ``conf`` app, using the Django app template provided by Cogwheels:

    .. code-block:: console

        $ django-admin.py startapp conf --template=https://github.com/ababic/cogwheels-conf-app/zipball/master

3.  All app settings are simply variables with upper-case names, added to your app's ``conf/defaults.py`` module with a default value. To find out more about how to define and use app setting values, see: :doc:`/usage/index`

.. NOTE ::
    If your app contains multiple sub-apps, you may wish to create multiple ``conf`` apps, within some or all those. Cogwheels fully supports this, and will generate a unique :doc:`setting namespace prefix <changing-the-namespace-prefix>` for each sub-app.


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

