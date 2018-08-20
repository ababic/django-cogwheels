=========================================
Removing an app setting: Example scenario
=========================================

For the sake of this example, imagine your app has a setting called ``DEFAULT_MENU_DEPTH`` that allows users to override how many levels deep a menu is rendered by a function when no alternative value is specified. 

You've decided that, instead of allowing users to change this default value via a setting, they should always specify a value when generating each menu, as this will make their code more verbose.

In terms of your project's life cycle, we'll pretend that:

-   The latest release version of your app is **1.5**.
-   The next release version of your app will be **1.6**.
-   Your app has a release policy that allows backwards-compatible changes to public APIs between MINOR releases, but only if followed a reasonable deprecation period (where possible). In the Django app space, deprecation periods of two MINOR releases are common, so in this example, we'll be aiming to drop support for the old setting in **1.8**.

Because we are having to support a deprecation period spanning multiple releases, we have no choice but to make our changes in stages:

.. contents::
    :local:
    :depth: 3


In the upcoming release (1.6)
=============================


.. _remove_step_1:

1. Marking the old setting as deprecated
----------------------------------------

First, we'll add a comment above the setting in ``defaults.py``, which will serve as a reminder to ourselves and other app maintainers about the setting's current status. You may find it helpful to keep your regular and deprecated settings separate, by adding a "Deprecated settings" section to the end of the module too, like so:

.. code-block:: python
    :emphasize-lines: 11-12
    
    # yourapp/conf/defaults.py

    ...

    # -------------------
    # Deprecated settings
    # -------------------

    # To be removed in 1.8.
    DEFAULT_MENU_DEPTH = 2

Next, we'll update the app's settings helper definition, so that it knows how to handle requests this settings:

.. code-block:: python
    :emphasize-lines: 9-18

    # yourapp/conf/settings.py

    from cogwheels import BaseAppSettingsHelper, DeprecatedAppSetting

    
    class MyAppSettingsHelper(BaseAppSettingsHelper):

        deprecations = (
            DeprecatedAppSetting(
                setting_name="DEFAULT_MENU_DEPTH",
                warning_category=PendingDeprecationWarning,
                additional_guidance=(
                    "Once removed, the default menu depth will be fixed at 2. "
                    "Where this is unsuitable, use the 'depth' argument to "
                    "specify an alternative value when calling the "
                    "generate_menu() method."
                ),
            ),
        )

There are a few things worth noting here:

-   The ``deprecations`` attribute value should always be a tuple, even if it only contains a single ``DeprecatedAppSetting`` definition.
-   For ``DeprecatedAppSetting`` definitions, setting names should be supplied as strings, and you should use non-prefixed setting names here (e.g. ``"DEFAULT_MENU_DEPTH"`` rather than ``"YOURAPP_DEFAULT_MENU_DEPTH"``). Prefixes should only be used by your app's users when adding overrides to their Django settings.
-   The ``warning_category`` used above will be passed to Python's ``warnings.warn()`` method when raising deprecation warnings related to this setting. We're using Python's built-in ``PendingDeprecationWarning`` here to indicate that deprecation is not yet imminent, but any sub-class of ``DeprecationWarning`` or ``PendingDeprecationWarning`` is supported (you might like to consider: :doc:`/best-practice/custom-deprecation-warning-classes`).
-   The ``additional_guidance`` argument can be used to provide additional information to users when raising deprecation warnings related to the setting.


.. _remove_step_2:


.. _remove_step_4:

4. Warn any users still using the old setting
---------------------------------------------

Assuming you have already made the changes in steps 2 and 3 above, Cogwheels already has you covered here.

When your code requests a value for the new setting from the settings helper using ``settings.BLOG_POSTS_UI_ICON`` or ``settings.get("BLOG_POSTS_UI_ICON")``, any users found to be using the old setting name (and with Python configured to surface deprecation warnings) will be presented with the following warning:

.. container:: highlight warning-sample

    PendingDeprecationWarning: The YOURAPP_ICON_FOR_BLOG_POSTS setting has been renamed to YOURAPP_BLOG_POSTS_UI_ICON. Please update your Django settings to use the new setting, otherwise the app will revert to it's default behaviour once support for YOURAPP_ICON_FOR_BLOG_POSTS is removed in two versions time.

There are a couple of things worth noting here:

-   This warning is intended for your app's core users, who will be using prefixed setting names in their Django settings to override your app's behaviour, so prefixed setting names are used in the warning text also.
-   The message ends with **"removed in two versions time"** because ``PendingDeprecationWarning`` was used as the ``warning_class`` value for the ``DeprecatedAppSetting`` definition in :ref:`step two <rename_step_2>`. Using ``DeprecationWarning`` (or a subclass of it) instead would result in the message ending with **"removed in the next version"**.

And, just in case there are any users out there using ``settings.ICON_FOR_BLOG_POSTS`` or ``settings.get("ICON_FOR_BLOG_POSTS")`` in their projects to request the old setting value from your settings helper (less likely, but perfectly possible), Cogwheels will present those users with a different (but similar) warning:

.. container:: highlight warning-sample

    PendingDeprecationWarning: The ICON_FOR_BLOG_POSTS app setting has been renamed to BLOG_POSTS_UI_ICON. Please update your code to reference the new setting, as continuing to reference ICON_FOR_BLOG_POSTS will cause an exception to be raised once support is removed in two versions time.

There are a couple of things worth noting here:

-   Because this warning is triggered by users referencing the settings from your app's settings helper using non-prefixed setting names (like you do in your app), non-prefixed setting names are used in this message also.
-   The message ends with **"removed in two versions time"** because ``PendingDeprecationWarning`` was used as the ``warning_class`` value for the ``DeprecatedAppSetting`` definition in :ref:`step two <rename_step_2>`. Using ``DeprecationWarning`` (or a subclass of it) instead would result in the message ending with **"removed in the next version"**.


.. _remove_step_5:

5. Updating the documentation
-----------------------------

How exactly you document your app settings is up to you, but it's highly recommended that you have some kind of reference to help users understand what behaviour they can override in your app and how.

.. seealso:: :doc:`/best-practice/documenting-your-app-settings`

If you do have a settings reference, you should make the following changes:

1. Add an entry for the new setting. If you are using Sphinx to build your documentation, use the :ref:`versionadded directive<versionadded-directive>` directive to indicate when the new setting was added.
2. Update the entry for the existing setting to mark it as deprecated. If you are using Sphinx to build documentation, use the :ref:`deprecated directive<deprecated-directive>` for this.
3. Review any direct references to the existing setting throughout the rest of the documentation, and update them to reference the entry for the new setting instead.


.. _remove_step_6:

6. Mentioning the deprecation in the release notes
--------------------------------------------------

How and where you define the release notes for your app is up to you, but it's highly recommended that you include information about any new deprecations for each version. For this release, you should include something about the old setting being deprecated, including details about how they can update their code, and when support for old setting will be removed entirely (e.g. version 1.8 in this example). This might look something like::

    Deprecations
    ============

    The following features have been deprecated in this version. Unless otherwise stated, support for deprecated features is retained for two minor releases, so you have until version **1.8** to make any necessary changes to your implementation.


    The ``YOURAPP_ICON_FOR_BLOG_POSTS`` setting has been renamed
    ------------------------------------------------------------

    If you are using this setting to override the icon used to represent blog posts in the admin area UI, you should update your Django settings to use the new setting name of ``YOURAPP_BLOG_POSTS_UI_ICON`` instead. Failure to do this by version ``1.8`` will resort in the default icon ("fa-newspaper") being used.

    Similarly, if you are importing ``yourapp.conf.settings`` anywhere within your project, and are requesting the old setting value from it (as an attribute: ``settings.ICON_FOR_BLOG_POSTS``, or using the ``get()``: ``settings.get("ICON_FOR_BLOG_POSTS")``), you should update that code to use the new setting name also.

    ..seealso::
        :ref:`BLOG_POSTS_UI_ICON`


In the next release (1.7)
=========================


.. _remove_step_7:

7. Use stronger deprecation warnings to indicate removal is now imminent
------------------------------------------------------------------------

Assuming you followed the example and used ``PendingDeprecationWarning`` (or a custom sub-class of it) as the ``warning_class`` value for the ``DeprecatedAppSetting`` definition in :ref:`step two <rename_step_2>`, all you should need to do here is update that ``DeprecatedAppSetting`` to use ``DeprecationWarning`` (or a custom sub-class of it) as the ``warning_class`` value instead, like so:

.. code-block:: python
    :emphasize-lines: 12

    # yourapp/conf/settings.py

    from cogwheels import BaseAppSettingsHelper, DeprecatedAppSetting

    
    class MyAppSettingsHelper(BaseAppSettingsHelper):

        deprecations = (
            DeprecatedAppSetting(
                setting_name="ICON_FOR_BLOG_POSTS",
                renamed_to="BLOG_POSTS_UI_ICON",
                warning_category=DeprecationWarning,
            ),
        )


Doing so should change the both the class used for any deprecation warnings raised in relation to this setting, and the descriptive text used for those warnings to read "in the next version" instead of "in two versions time".


In the following release (1.8)
==============================


.. _remove_step_8:

8. Removing support for the deprecated setting
----------------------------------------------
    
Because Cogwheels handles so much for you automatically, you shouldn't have to do much in terms of updating your app code now. The changes already made back in :ref:`step 3 <rename_step_3>` should be all that is needed. 


.. _remove_step_9:

9. Removing the deprecated setting itself
-----------------------------------------

First, we'll update our app's settings helper definition again. This time, to remove the ``DeprecatedAppSetting`` definition that was added back in :ref:`step 2 <rename_step_2>`:

.. code-block:: python
    :emphasize-lines: 9-13

    # yourapp/conf/settings.py

    from cogwheels import BaseAppSettingsHelper, DeprecatedAppSetting

    
    class MyAppSettingsHelper(BaseAppSettingsHelper):

        deprecations = (
            DeprecatedAppSetting(
                setting_name="ICON_FOR_BLOG_POSTS",
                renamed_to="BLOG_POSTS_UI_ICON",
                warning_category=PendingDeprecationWarning,
            ),
        )

Next, we'll remove any lines related to the old setting from the ``defaults.py`` module: 

.. code-block:: python
        :emphasize-lines: 12-13

        # yourapp/conf/defaults.py

        ...

        BLOG_POSTS_UI_ICON = 'fa-newspaper'

        # -------------------
        # Deprecated settings
        # -------------------
        # These need to stick around until support is dropped completely

        # Replaced by BLOG_POSTS_UI_ICON. To be removed in 1.8:
        ICON_FOR_BLOG_POSTS = 'fa-newspaper'


.. _remove_step_10:

10. Updating the documentation
------------------------------

How exactly you do this is up to you, but to avoid any ambiguity surrounding the new and old setting, it's recommended that you remove the entry for the old setting from your 'Settings reference' where possible, reviewing any references to it in the process.


.. _remove_step_11:

11. Mentioning the backwards-incompatible change in the release notes
---------------------------------------------------------------------

This version of your app will now behave differently for any users still using the old setting name to override the icon, and will raise an exception for anyone requesting old setting values from your settings helper. Because of this, it's important to let users know about the changes in your release notes. Your addition might look something like this::

    Backwards-incompatible changes
    ==============================

    Following a standard deprecation period a two minor releases, the following functionality has now been removed.


    The ``YOURAPP_ICON_FOR_BLOG_POSTS`` setting
    -------------------------------------------

    If you are using this setting to override the icon used to represent blog posts in the admin area UI, you should update your Django settings to use the new setting name of ``YOURAPP_BLOG_POSTS_UI_ICON`` instead. Failure to do this after upgrading will result in the default icon ("fa-newspaper") being used.

    Similarly, if you are importing ``yourapp.conf.settings`` anywhere within your project, and are requesting the old setting value from it (as an attribute: ``settings.ICON_FOR_BLOG_POSTS``, or using ``get()``: ``settings.get("ICON_FOR_BLOG_POSTS")``), you should update that code to use the new setting name also. Failure to do this after upgrading will result in an ``AttributeError`` or ``ImproperlyConfigured`` error.

    ..seealso::
        :ref:`BLOG_POSTS_UI_ICON`



