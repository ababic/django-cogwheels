=========================================
Example scenario: Renaming an app setting
=========================================

For the sake of this example, imagine your app has a setting called ``ICON_FOR_BLOG_POSTS`` that allows users to override the icon used to represent blog posts in a UI somewhere.

You want to rename this setting to ``BLOG_POSTS_UI_ICON``.

This is a change in **name only**, so all of the following must the same:

- The default setting value or behaviour
- The range or type of override values supported
- The side effects of overriding

In terms of your project's life cycle, we'll pretend that:

-   The latest release version of your app is **1.5**.
-   The next release version of your app will be **1.6**.
-   Your app has a release policy that allows backwards-compatible changes to public APIs between MINOR releases, but only if followed a reasonable deprecation period (where possible). In the Django app space, deprecation periods of two MINOR releases are common, so in this example, we'll be aiming to drop support for the old setting in **1.8**.


Implementing the changes
========================

Because we are having to support a deprecation period spanning multiple releases, we have no choice but to make our changes in stages. This section outlines what changes must be made in each release:

.. contents::
    :local:
    :depth: 3


IN THE UPCOMING RELEASE (1.6)
-----------------------------


.. _rename_step_1:

Adding a setting with the new name
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

All app settings are simply variables added to the ``defaults.py`` module, and this new setting is no exception. Add a variable with the new setting name, with the same value as the existing setting.

.. code-block:: python
    :emphasize-lines: 7

    # yourapp/conf/defaults.py

    ...

    ICON_FOR_BLOG_POSTS = 'fa-newspaper'

    BLOG_POSTS_UI_ICON = 'fa-newspaper'

    ...


.. _rename_step_2:

Marking the old setting as deprecated
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

First, we'll add a comment above the current setting in ``defaults.py``, which will serve as a reminder to ourselves and other app maintainers about the setting's current status. You may find it helpful to keep your regular and deprecated settings separate, by adding a "Deprecated settings" section to the end of the module too, like so:

.. code-block:: python
    :emphasize-lines: 11-12
    
    # yourapp/conf/defaults.py

    ...

    BLOG_POSTS_UI_ICON = 'fa-newspaper'

    # -------------------
    # Deprecated settings
    # -------------------

    # Replaced by BLOG_POSTS_UI_ICON. To be removed in 1.8:
    ICON_FOR_BLOG_POSTS = 'fa-newspaper'

Next, we'll update the app's settings helper definition, so that it knows how to handle requests for both the old and new settings:

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

There are a few things worth noting here:

-   The ``deprecations`` attribute value should always be a tuple, even if it only contains a single ``DeprecatedAppSetting`` definition.
-   For ``DeprecatedAppSetting`` definitions, setting names should be supplied as strings, and you should use non-prefixed setting names here (e.g. ``"ICON_FOR_BLOG_POSTS"`` rather than ``"YOURAPP_ICON_FOR_BLOG_POSTS"``). Prefixes should only be used by your app's users when adding overrides to their Django settings.
-   The ``warning_category`` used above will be passed to Python's ``warnings.warn()`` method when raising deprecation warnings related to this setting. We're using Python's built-in ``PendingDeprecationWarning`` here to indicate that deprecation is not yet imminent, but any sub-class of ``DeprecationWarning`` or ``PendingDeprecationWarning`` is supported (you might like to consider: :doc:`/best-practice/custom-deprecation-warning-classes`).


.. _rename_step_3:

Updating the app code to support both the new and old settings
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Let's pretend the setting is currently being used in the following way by our app's codebase:

.. code-block:: python
    :emphasize-lines: 11

    # yourapp/modeladmin.py

    from wagtail.contrib.modeladmin.options import ModelAdmin

    from yourapp.blog.models import BlogPost
    from yourapp.conf import settings


    class BlogPostModelAdmin(ModelAdmin):
        model = BlogPost
        menu_icon = settings.ICON_FOR_BLOG_POSTS  # The OLD setting name!


Typically, supporting both the new and old app settings here simultaneously would involve having to make some considerable changes. But, because we're using Cogwheels, and our settings helper knows about this deprecation, all we have to do is this:

.. code-block:: python
    :emphasize-lines: 4

    # yourapp/modeladmin.py

    class BlogPostModelAdmin(ModelAdmin):
        menu_icon = settings.BLOG_POSTS_UI_ICON  # The NEW setting name!


The settings helper will automatically do some extra work to support users still using the old setting name:


1.  First, it looks for an override value defined using the new name, e.g.

    .. code-block:: python

        # userproject/settings/base.py

        # ---------------------------------
        # Overrides for ``your-django-app``
        # ---------------------------------

        YOURAPP_BLOG_POSTS_UI_ICON = 'fa-rss'  # I'm cutting edge!

2.  Next, it looks for an override value defined using the old name, e.g.

    .. code-block:: python
        
        # userproject/settings/base.py

        # ---------------------------------
        # Overrides for ``your-django-app``
        # ---------------------------------

        YOURAPP_ICON_FOR_BLOG_POSTS = 'fa-rss'  # I'm old-skool!

3.  If no override setting was found, Cogwheels resorts to using the default value for the new setting.


.. _rename_step_4:

Warn any users still using the old setting
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

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


.. _rename_step_5:

Updating the documentation
~~~~~~~~~~~~~~~~~~~~~~~~~~

How exactly you document your app settings is up to you, but it's highly recommended that you have some kind of reference to help users understand what behaviour they can override in your app and how.

.. seealso:: :doc:`/best-practice/documenting-your-app-settings`

If you do have a settings reference, you should make the following changes:

1. Add an entry for the new setting. If you are using Sphinx to build your documentation, use the :ref:`versionadded directive<versionadded-directive>` directive to indicate when the new setting was added.
2. Update the entry for the existing setting to mark it as deprecated. If you are using Sphinx to build documentation, use the :ref:`deprecated directive<deprecated-directive>` for this.
3. Review any direct references to the existing setting throughout the rest of the documentation, and update them to reference the entry for the new setting instead.


.. _rename_step_6:

Mentioning the deprecation in the release notes
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

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


IN THE NEXT RELEASE (1.7)
-------------------------


.. _rename_step_7:

Use stronger deprecation warnings to indicate that removal is now imminent
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

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


IN THE FOLLOWING RELEASE (1.8)
------------------------------


.. _rename_step_8:

Remove support for the deprecated setting in app code
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    
Because Cogwheels handles so much for you automatically, you shouldn't have to do much in terms of updating your app code now. The changes already made back in :ref:`step 3 <rename_step_3>` should be all that is needed. 


.. _rename_step_9:

Removing the deprecated setting 
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

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


.. _rename_step_10:

Updating the documentation
~~~~~~~~~~~~~~~~~~~~~~~~~~

How exactly you do this is up to you, but to avoid any ambiguity surrounding the new and old setting, it's recommended that you remove the entry for the old setting from your 'Settings reference' where possible, reviewing any references to it in the process.


.. _rename_step_11:

Mentioning the backwards-incompatible change in the release notes
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

This version of your app will now behave differently for any users still using the old setting name to override the icon, and will raise an exception for anyone requesting old setting values from your app's settings helper. So, it's important to let them know about these changes in your release notes. Your addition might look something like this::

    Backwards-incompatible changes
    ==============================

    Following a standard deprecation period a two minor releases, the following functionality has now been removed.


    The ``YOURAPP_ICON_FOR_BLOG_POSTS`` setting
    -------------------------------------------

    If you are using this setting to override the icon used to represent blog posts in the admin area UI, you should update your Django settings to use the new setting name of ``YOURAPP_BLOG_POSTS_UI_ICON`` instead. Failure to do this after upgrading will result in the default icon ("fa-newspaper") being used.

    Similarly, if you are importing ``yourapp.conf.settings`` anywhere within your project, and are requesting the old setting value from it (as an attribute: ``settings.ICON_FOR_BLOG_POSTS``, or using ``get()``: ``settings.get("ICON_FOR_BLOG_POSTS")``), you should update that code to use the new setting name also. Failure to do this after upgrading will result in an ``AttributeError`` or ``ImproperlyConfigured`` error.

    ..seealso::
        :ref:`BLOG_POSTS_UI_ICON`



