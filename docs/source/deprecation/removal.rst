=======================
Removing an app setting
=======================

.. warning ::
    This examples assumes you are using custom deprecation warnings classes to help manage deprecations for your app. If you are not, you may find it tricky to follow in parts. It isn't a requirement that you use custom deprecation warning classes for app setting deprecations, but it will make your life (and following this example) easier. Check out the following guide: :doc:`/best-practice/custom-deprecation-warning-classes`.

This guide demonstrates the steps required to remove support a setting, following a standard 'two release' deprecation process.


What we're looking to achieve
=============================

Let's pretend that your app currently has an overridable setting that allows users to modify the cache timeout used by a specific feature. Like all your app settings, the default value appears in ``defaults.py`` like so:

.. code-block:: python
    
    # yourapp/conf/defaults.py

    # ---------------------
    # Product data settings
    # ---------------------

    PRODUCT_LIST_CACHE_TIMEOUT = 3000

You have since decided that it will be better for your app to not use a timeout at all, and cache product data for the maximum time supported by the cache.

Your app should continue to respect override values defined using ``YOURAPP_PRODUCT_LIST_CACHE_TIMEOUT`` in user's Django settings for another two versions, but any users who are using it should be warned that the behaviour is changing, and the override will no longer have any affect once the deprecation period has ended. You also want to include some additional guidance to warning messages, prompting users to check that they are using a cache solution that supports a ``TIMEOUT`` value of ``None``.


A few assumptions
-----------------

In the following example, we're going to assume that:

-   The latest release version of your app was **1.5**.
-   The next release version of your app will be **1.6**.
-   You have a deprecation policy that continues to support deprecated behaviour for two 'feature releases' before support is dropped completely. So, in each example, we'll be aiming to remove support completely in version **1.8**.


Changes required for the upcoming release (1.6)
===============================================


1. Updating ``conf/defaults.py``
--------------------------------

You may find it helpful to mark the deprecated setting here in some way, to remind you and other app maintainers that it has been deprecated.

.. code-block:: python
    :emphasize-lines: 8

    # yourapp/conf/defaults.py

    # -------------------
    # Deprecated settings
    # -------------------
    # These need to stick around until support is dropped completely

    PRODUCT_LIST_CACHE_TIMEOUT = None  # Remove in v1.8


2. Updating ``conf/settings.py``
--------------------------------

Next, you'll need to update your app's settings helper, so that it knows how to handle requests for setting values. For example:

.. code-block:: python

    # yourapp/conf/settings.py

    from cogwheels import BaseAppSettingsHelper, DeprecatedAppSetting
    from yourapp.utils.deprecation import RemovedInYourApp18Warning

    
    class MyAppSettingsHelper(BaseAppSettingsHelper):

        deprecations = (
            DeprecatedAppSetting(
                setting_name="PRODUCT_LIST_CACHE_TIMEOUT",
                warning_category=RemovedInYourApp18Warning,
                additional_guidance=(
                    "Product data is now cached indefinitely by default, "
                    "and invalidated automatically when a product is updated. "
                    "This approach will be used unconditionally once support "
                    "for the setting is removed. Please ensure the cache "
                    "implementation you are using supports None timeout "
                    "values. If needed, you can use the "
                    "YOURAPP_PRODUCT_DATA_CACHE setting to change the cache "
                    "used for product data."
            ),
        )

There are a few things worth noting here:

- When defining ``deprecations`` on your ``SettingsHelper`` class, the value must be a tuple, even if it only contains a single ``DeprecatedAppSetting`` definition.
- In the ``DeprecatedAppSetting`` definition, setting names should be provided as strings.
- The ``warning_category`` used in the ``DeprecatedAppSetting`` definition above will be passed to Python's ``warnings.warn()`` method when raising deprecation warnings related to this setting. It should be a subclass of ``DeprecationWarning`` or ``PendingDeprecationWarning``.


3. Updating your app code
-------------------------

In progress


4. Updating your documentation
------------------------------

In progress


Changes required for the next release (1.7)
===========================================

Provided you are defining and using custom deprecation warnings within your app (using the approach outlined in: :doc:`/best-practice/custom-deprecation-warning-classes`), and cycle those warnings for this release, no further changes should be needed in regards to this specific deprecation. The message text for any warnings raised in relation to this setting should change automatically to read 'in the next version' instead of 'in two versions time'.


Changes required for the following release (1.8)
================================================

We're finally ready to remove support for the old setting, so the following steps should be taken:

1.  Remove the default value for the setting from ``defaults.py`` 
    
    .. code-block:: python
        :emphasize-lines: 16

        # yourapp/conf/defaults.py

        # -------------------
        # Admin / UI settings
        # -------------------

        FLAT_MENUS_MENU_ICON = 'list-ol'

        FLAT_MENUS_EDITABLE_IN_WAGTAILADMIN = True

        # -------------------
        # Deprecated settings
        # -------------------
        # These need to stick around until support is dropped completely

        FLATMENU_MENU_ICON = 'list-ol'  # REMOVE THIS LINE!

2.  Remove the deprecation definition from your app's setting helper in ``settings.py``

    .. code-block:: python
        :emphasize-lines: 7

        # yourapp/conf/settings.py
        
        from cogwheels import BaseAppSettingsHelper, DeprecatedAppSetting
        from yourapp.utils.deprecation import RemovedInYourApp18Warning

        class MyAppSettingsHelper(BaseAppSettingsHelper):
            deprecations = ()
    
3. Announce the breaking change in the version **1.8** release notes.

4. Remove the entry for the old setting from the "Settings reference" page of the documentation.
