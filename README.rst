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

Cogwheels provides you with:

- A stable, documented, well tested, standardised approach for implementing overridable settings.
- A way to clearly define and communicate the deprecation status of overridable settings, giving you the flexibility to rename, replace or flag settings for removal over your project's lifecycle. User overrides defined using old setting names remain available to you, allowing you to continue support them during the deprecation period.
- Helpful error messages when default values provided for Model, Class, method or modules are invalid.

Goodness for your users
=======================

Cogwheels gives them:

- Helpful, consistent error messages when their Model, Class, method or module override settings are incorrectly formatted, or cannot be imported.
- Helpful, consistent deprecation warnings when they are overriding a setting that has been renamed, replaced or flagged for removal.


Installation instructions
=========================

Documentation coming soon.


Usage Guide
===========

Documentation coming soon.


Compatibility
=============

The current version is tested for compatiblily with the following: 

- Django versions 1.11 to 2.0
- Python versions 3.4 to 3.6
