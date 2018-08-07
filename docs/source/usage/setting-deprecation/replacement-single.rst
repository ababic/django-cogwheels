==============================
Setting replacement (singular)
==============================

This guide demonstrates the steps required to introduce a new setting that 'logically replaces' a single existing setting, following a standard 'two release' deprecation process.

If you're looking to add a setting that replaces multiple existing settings, you may find the :doc:`replacement-multiple` more useful.

.. contents:: Contents
    :local:
    :depth: 2


What we're looking to achieve
=============================

Let's pretend your app has a few app setting that allows users to toggle something on or off using a boolean

.. code-block:: python
    :caption: yourapp/conf/defaults.py

    # -------------------
    # Admin / UI settings
    # -------------------

    HIDE_FULL_NAMES_IN_SUMMARY = False
    SHOW_FAILED_PAYMENTS_IN_SUMMARY = True
    SHOW_GRAPHS_ON_DASHBOARD = True

For the sake of consistency, you'd like to rename HIDE_FULL_NAMES_IN_SUMMARY to SHOW_FULL_NAMES_IN_SUMMARY, and give it a value of ``True`` by default.


A few assumptions
-----------------

In the following example, we're going to assume that:

-   The latest release version of your app was **1.5**.
-   The next release version of your app will be **1.6**.
-   You have a deprecation policy that continues to support deprecated behaviour for two 'feature releases' before support is dropped completely. So, in each example, we'll be aiming to remove support completely in version **1.8**.
-   You are defining and using custom deprecation warnings within your app, using the approach outlined in: :doc:`/best-practice/custom-deprecation-warning-classes`.


Implementing the deprecation
============================


In version **1.6**
------------------


1. Updating ``conf/defaults.py``
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

First, we'll add a setting using the new name to ``defaults.py``. We also want to mark the existing settings in ``defaults.py`` in some way, to help us remember that they are deprecated. Our updated ``defaults.py`` module should look something like this:

.. code-block:: python
    :caption: yourapp/conf/defaults.py
    :emphasize-lines: 5,20

    # -------------------
    # Admin / UI settings
    # -------------------

    SHOW_FULL_NAMES_IN_SUMMARY = True  # I'm new!
    SHOW_FAILED_PAYMENTS_IN_SUMMARY = True
    SHOW_GRAPHS_ON_DASHBOARD = True

    # --------------
    # Other settings
    # --------------

    ...

    # -------------------
    # Deprecated settings
    # -------------------
    # These need to stick around until support is dropped completely

    HIDE_FULL_NAMES_IN_SUMMARY = False  # Remove me in v1.8!


2. Updating ``conf/settings.py``
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Next, you'll need to update your app's settings helper, so that it knows how to handle requests for setting values. For example:

.. code-block:: python
    :caption: yourapp/conf/settings.py

    from cogwheels import BaseAppSettingsHelper, DeprecatedAppSetting
    from yourapp.utils.deprecation import RemovedInYourApp18Warning

    
    class MyAppSettingsHelper(BaseAppSettingsHelper):

        deprecations = (
            DeprecatedAppSetting(
                setting_name='HIDE_FULL_NAMES_IN_SUMMARY',
                replaced_by='SHOW_FULL_NAMES_IN_SUMMARY',
                warning_category=RemovedInYourApp18Warning,
                additional_guidance=(
                    "As the name suggests, the new setting has the opposite affect, "
                    "and the default value is now True instead of False."
                )
            ),
        )

There are a few things worth noting here:

-   If you need to define ``deprecations`` on your settings helper class, it must be a ``tuple``, even if you only need a single ``DeprecatedAppSetting`` definition.
-   In the ``DeprecatedAppSetting`` definition, setting names are supplied as strings, and we're still using internal/non-prefixed setting names (e.g. ``"FLATMENU_MENU_ICON"`` rather than ``"YOURAPP_FLATMENU_MENU_ICON"``).
-   The ``warning_category`` used in the ``DeprecatedAppSetting`` definition here will be passed to Python's ```warnings.warn()`` method when raising deprecation warnings related to this setting. It should be a subclass of ``DeprecationWarning``.
-   The ``additional_guidance`` argument is optional. But, if supplied, this string will be appended to any of the deprecation warnings raised in relation to this setting. The automatically generated warnings text is quite thorough, so you only really need to explain about nuances between the two settings (if there are any), which is something  Cogwheels cannot realistically infer.
    
    .. NOTE::
        If the issue is particularly difficult to summarise succinctly, it's perfectly valid to include a URL to your release notes / documentation in ``additional_guidance``, and explain things in more thoroughly there.


3. Updating your app code
~~~~~~~~~~~~~~~~~~~~~~~~~

The above steps take care of the deprecation definition, but we still have to update our code to use the new setting. Let's imagine that our code currently looks something like this:

.. code-block:: python
    :caption: yourapp/views.py
    :emphasize-lines: 8

    from django.views.generic import ListView
    from yourapp.conf import settings


    class TransactionSummaryList(ListView):
        
        def get_context_data(self, **kwargs):
            show_full_names = not settings.HIDE_FULL_NAMES_IN_SUMMARY
            data = {
                'show_full_names': show_full_names,
            }
            data.update(**kwargs)
            return super().get_context_data(**data)

        ...


This line highlighted above will now cause the following deprecation warning to be raised:

.. code-block:: console
    
    RemovedInYourApp18Warning: The HIDE_FULL_NAMES_IN_SUMMARY app setting is
    deprecated in favour of using SHOW_FULL_NAMES_IN_SUMMARY. Please update 
    your code to reference the new setting, as continuing to reference 
    HIDE_FULL_NAMES_IN_SUMMARY will cause an exception to be raised once
    support is removed in two versions time. As the name suggests, the new
    setting has the opposite affect, and the default value is now True instead
    of False.

.. NOTE:: If users of your app are referencing ``settings.HIDE_FULL_NAMES_IN_SUMMARY`` or calling ``settings.get('HIDE_FULL_NAMES_IN_SUMMARY')`` for any reason, this warning will be raised by their code also.

First, we want to update the view to use the new setting instead, because the above will now raise a deprecation warning, and that's not what we want:

.. code-block:: python
    :caption: yourapp/views.py
    :emphasize-lines: 4

    class TransactionSummaryList(ListView):
        
        def get_context_data(self, **kwargs):
            show_full_names = settings.SHOW_FULL_NAMES_IN_SUMMARY
            data = {
                'hide_full_names': hide_full_names,
            }
            data.update(**kwargs)
            return super().get_context_data(**data)

        ...

Because your settings helper knows all it needs to about the replacement, ``settings.SHOW_FULL_NAMES_IN_SUMMARY`` will do some extra work to support users still using the old setting name:

1.  It first looks for an override setting using the new name (which is the 'ideal' scenario) and where we want all our users to be eventually. For example:

    .. code-block:: python
        :caption: userproject/settings/base.py

        # ---------------------------------
        # Overrides for ``your-django-app``
        # ---------------------------------

        YOURAPP_SHOW_FULL_NAMES_IN_SUMMARY = False  # I'm cutting edge!

2.  Next, Cogwheels will look for an override setting defined using the old name. For example:

    .. code-block:: python
        :caption: userproject/settings/base.py

        # ---------------------------------
        # Overrides for ``your-django-app``
        # ---------------------------------

        YOURAPP_HIDE_FULL_NAMES_IN_SUMMARY = True  # I'm old-skool!

3.  If no override setting was found, Cogwheels resorts to using the default value for the new setting, as you'd expect.

Although we’re still happy to the deprecated setting for a couple more versions, we want to make users aware that the setting has been replaced. So, Cogwheels will raise the following warning:

.. code-block:: console
    
    RemovedInYourApp18Warning: The YOURAPP_FLATMENU_MENU_ICON setting has been 
    renamed to YOURAPP_FLAT_MENUS_MENU_ICON. Please update your Django settings
    to use the new setting, otherwise the app will revert to it's default
    behavior once support for YOURAPP_FLATMENU_MENU_ICON it removed in two 
    versions time.

In some scenarios, would be all that is required, but obviously more must be done in our case, because the old and new settings have completely different meanings. We need to know where the settings module got it's value from, so that we can modify our app's behaviour accordingly.

The settings helper's ``is_value_from_deprecated_setting()`` method can help us here:

.. code-block:: python
    :caption: yourapp/views.py
    :emphasize-lines: 6-12

    class TransactionSummaryList(ListView):
        
        def get_context_data(self, **kwargs):
            show_full_names = settings.SHOW_FULL_NAMES_IN_SUMMARY
            
            # TODO: Remove in v1.8
            if settings.is_value_from_deprecated_setting(
                'SHOW_FULL_NAMES_IN_SUMMARY', 'HIDE_FULL_NAMES_IN_SUMMARY'
            ):
                # The old setting meant the opposite, so...
                show_full_names = not show_full_names
            
            data = {
                'hide_full_names': hide_full_names,
            }
            data.update(**kwargs)
            return super().get_context_data(**data)

        ...

Now our code is catering for all users, whether they are overriding the deprecated setting, the replacement, both or neither.


4. Updating your documentation
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Raising a deprecation warning with Python is certainly helpful, but you'll also want to update your documentation to reflect the new changes, by:

1.  Mentioning the deprecation in the **1.6** release notes.
2.  Adding an entry for the new setting to the "Settings reference", and updating any references to the old setting entry to the new one.
3.  Updating the entry for the existing setting in the "Settings reference", using Sphinx's `deprecated directive <http://www.sphinx-doc.org/en/stable/markup/para.html#directive-deprecated>`_ to mark the old setting as deprecated. For example::

        .. deprecated:: 1.6
            Use :ref:`YOURAPP_HIDE_FULL_NAMES_IN_SUMMARY` instead.


In version **1.7**
------------------

Provided you are defining and using custom deprecation warnings within your app (using the approach outlined in: :doc:`/best-practice/custom-deprecation-warning-classes`), and cycle those warnings for this release, no further changes should be needed in regards to this specific deprecation. The message text for any warnings raised in relation to this setting should change automatically to read 'in the next version' instead of 'in two versions time'.


In version **1.8**
------------------

We're finally ready to remove support for the old setting (YEY!), so the following steps should be taken:

1.  Remove the default value for the old setting from ``defaults.py`` 
    
    .. code-block:: python
        :caption: yourapp/conf/defaults.py
        :emphasize-lines: 20

        # -------------------
        # Admin / UI settings
        # -------------------

        SHOW_FULL_NAMES_IN_SUMMARY = True  # I'm new!
        SHOW_FAILED_PAYMENTS_IN_SUMMARY = True
        SHOW_GRAPHS_ON_DASHBOARD = True

        # --------------
        # Other settings
        # --------------

        ...

        # -------------------
        # Deprecated settings
        # -------------------
        # These need to stick around until support is dropped completely

        HIDE_FULL_NAMES_IN_SUMMARY = False  # REMOVE THIS LINE!

2.  Remove the deprecation definition from your setting helper class in ``settings.py``

    .. code-block:: python
        :caption: yourapp/conf/settings.py
        :emphasize-lines: 5
        
        from cogwheels import BaseAppSettingsHelper, DeprecatedAppSetting
        from yourapp.utils.deprecation import RemovedInYourApp18Warning

        class MyAppSettingsHelper(BaseAppSettingsHelper):
            deprecations = ()

3. Remove any special-case code that was added in **1.6** to support the old setting during it's deprecation period.
    
4. Announce the breaking change in the version **1.8** release notes.

5. Remove the entry for the old setting from the "Settings reference" page of the documentation.
