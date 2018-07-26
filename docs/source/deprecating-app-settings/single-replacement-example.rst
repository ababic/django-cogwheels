======================================
A 'single setting replacement' example
======================================

This guide demonstrates the steps required to introduce a new setting that 'logically replaces' a single existing setting, following a standard 'two release' deprecation process.

If you're looking to add a setting that replaces multiple existing settings, you may find the :doc:`multi-replacement-example` more useful.

.. contents::
    :local:
    :depth: 2


What we're looking to achieve
=============================

Let's pretend your app has a few app setting that allows users to toggle something on or off using a boolean

.. code-block:: python

    # yourapp/conf/defaults.py

    # -------------------
    # Admin / UI settings
    # -------------------

    HIDE_FULL_NAMES_IN_SUMMARY = False
    SHOW_FAILED_PAYMENTS_IN_SUMMARY = True
    SHOW_GRAPHS_ON_DASHBOARD = True

For the sake of consistency, you'd like to rename HIDE_FULL_NAMES_IN_SUMMARY to SHOW_FULL_NAMES_IN_SUMMARY, and give it a value of ``True`` by default.


Some assumptions
================

In the following example, we're going to assume that:

-   The latest release version of your app was ``1.5``.
-   The next release version of your app will be ``1.6``.
-   You have a deprecation policy that continues to support deprecated behaviour for two 'feature releases' before support is dropped completely. So, in each example, we'll be aiming to remove support completely in version ``1.8``.
-   You are defining and using custom deprecation warnings within your app, using the approach outlined in: :doc:`using-custom-warning-classes`.


Implementing the deprecation
============================


In version ``1.6``
------------------


1. Adding the new setting
~~~~~~~~~~~~~~~~~~~~~~~~~

First, we'll add a setting using the new name to ``defaults.py``. We also want to mark the existing settings in ``defaults.py`` in some way, to help us remember that they are deprecated. Our updated ``defaults.py`` module should look something like this:


.. code-block:: python

    # yourapp/conf/defaults.py

    # -------------------
    # Admin / UI settings
    # -------------------

    SHOW_FULL_NAMES_IN_SUMMARY = True  # I'm new!
    SHOW_FAILED_PAYMENTS_IN_SUMMARY = True
    SHOW_GRAPHS_ON_DASHBOARD = True

    # -------------------
    # Deprecated settings
    # -------------------
    # These need to stick around until support is dropped completely

    HIDE_FULL_NAMES_IN_SUMMARY = False  # Remove me in v1.8!


2. Declaring the deprecation
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Next, we'll update the settings helper definition for our app, so that it knows how to handle requests for setting values:


.. code-block:: python

    # yourapp/conf/settings.py

    from cogwheels import BaseAppSettingsHelper, DeprecatedAppSetting
    from yourapp.utils.deprecation import RemovedInYourApp18Warning

    
    class MyAppSettingsHelper(BaseAppSettingsHelper):

        deprecations = (
            DeprecatedAppSetting(
                setting_name='HIDE_FULL_NAMES_IN_SUMMARY',
                replaced_by='SHOW_FULL_NAMES_IN_SUMMARY',
                warning_category=RemovedInYourApp18Warning, # use this class when raising deprecation warnings,
                additional_guidance=(
                    "As the name suggests, the new setting has completely the opposite effect that it did before, "
                    "and the default value is ``True`` rather than ``False``."
                )
            ),
        )

    ...


3. Updating the app code
~~~~~~~~~~~~~~~~~~~~~~~~

The above steps take care of the deprecation definition, but we still have to update our code to use the new setting. Let's imagine that our code currently looks something like this:


.. code-block:: python

    # yourapp/views.py

    from django.views.generic import ListView

    from yourapp.conf import settings


    class TransactionSummaryList(ListView):
        
        def get_context_data(self, **kwargs):
            data = {
                'hide_full_names': settings.HIDE_FULL_NAMES_IN_SUMMARY,
                ...
            }
            data.update(**kwargs)
            return super().get_context_data(**data)
    ...

First, we want to update the view to use the new setting instead:

.. code-block:: python

    # yourapp/views.py

    class TransactionSummaryList(ListView):
        
        def get_context_data(self, **kwargs):
            hide_full_names = not settings.SHOW_FULL_NAMES_IN_SUMMARY
            data = {
                'hide_full_names': hide_full_names,
                ...
            }
            data.update(**kwargs)
            return super().get_context_data(**data)
    ...
