Utilising the ``conf`` app
==========================

Since you now have a ``conf`` app, it might make sense to move other 'configurational' things into there too.

For example, in the ``conf`` app for wagtailmenus_, there's a ``constants.py`` file for defining some fixed values that are used app-wide, and the ``apps.py`` module that normally resides in an app's root directory has also been moved to the ``conf``.

.. _wagtailmenus: https://github.com/rkhleics/wagtailmenus/tree/master/wagtailmenus
