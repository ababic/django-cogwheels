=========================================
Removing an app setting: Example scenario
=========================================

For the sake of this example, imagine your app has a setting called ``DEFAULT_MENU_DEPTH`` that allows users to override how many levels deep a menu is rendered by a function when no alternative value is specified. 

You've decided that it will be better if, instead of allowing users to change this default value via a setting, the default value should always be ``2``, and user's should specify when calling the function whenever they want the depth to differ.

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
    :emphasize-lines: 9-10
    
    # yourapp/conf/defaults.py

    ...

    # -------------------
    # Deprecated settings
    # -------------------

    # To be removed in 1.8.
    DEFAULT_MENU_DEPTH = 2

Next, we'll update the settings helper definition for our app, to make it aware of the deprecation:

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
                    "specify an alternative value when using the render_menu() "
                    "tag."
                ),
            ),
        )

There are a few things worth noting here:

-   The ``deprecations`` attribute value should always be a tuple, even if it only contains a single ``DeprecatedAppSetting`` definition.
-   For ``DeprecatedAppSetting`` definitions, setting names should be supplied as strings, and you should use non-prefixed setting names here (e.g. ``"DEFAULT_MENU_DEPTH"`` rather than ``"YOURAPP_DEFAULT_MENU_DEPTH"``). Prefixes should only be used by your app's users when adding overrides to their Django settings.
-   The ``warning_category`` used above will be passed to Python's ``warnings.warn()`` method when raising deprecation warnings related to this setting. We're using Python's built-in ``PendingDeprecationWarning`` here to indicate that deprecation is not yet imminent, but any sub-class of ``DeprecationWarning`` or ``PendingDeprecationWarning`` is supported (you might like to consider: :doc:`/best-practice/custom-deprecation-warning-classes`).
-   The ``additional_guidance`` argument can be used to provide additional information to users when raising deprecation warnings related to the setting.

    .. TIP::
       If the change is difficult to summarise succinctly, it's perfectly valid to include a URL to your release notes / documentation in ``additional_guidance``, and explain things in more detail there.


.. _remove_step_2:

2. Updating the code where the setting value is used
----------------------------------------------------

Let's pretend the setting is currently being used in the following way by our app's codebase:

.. code-block:: python
    :emphasize-lines: 7

    # yourapp/templatetags/menu_tags.py

    from yourapp.conf import settings

    def render_menu(root_page, depth=None):
        if depth is None:
            depth = settings.DEFAULT_MENU_DEPTH
        # do stuff     
        ...

Now, we still want to use the settings helper to retrieve the value here, because we still have to support override values for a while longer. However, the line highlighted above will currently raise a deprecation warning, because the setting is deprecated. So, what to do?

Referencing settings as direct attributes of the settings helper is basically a shortcut for calling the helpers ``get()`` method. The default behaviour of ``get()`` is to raise a deprecation warning at this point, but when calling the method directly, the ``warn_only_if_overridden`` argument can be used to change this behaviour.

We want to change the highlighted line from::
    
    depth = settings.DEFAULT_MENU_DEPTH 

To::

    depth = settings.get("DEFAULT_MENU_DEPTH", warn_only_if_overridden=True)


This way, a deprecation warning will only be raised if a user is overriding the setting (and not if the default value is being used), which is what we want.

.. NOTE::
    If you happen to be using the ``models`` attribute shortcut to retrieve a Django model instead of a raw setting value (e.g. ``settings.models.SETTING_NAME``), you can call ``settings.get_model("SETTING_NAME")`` instead, which also accepts the ``warn_only_if_overridden`` argument.

    Similarly, if you are using the ``modules`` or ``objects`` attribute shortcuts, you can use ``get_module()`` or ``get_objects()`` (repectively), both of which accept the ``warn_only_if_overridden`` argument too.


.. _remove_step_3:

3. Warn any users still using the old setting
---------------------------------------------

Assuming you have already made the changes in steps 1 and 2 above, Cogwheels already has you covered here.

When your code requests the setting value, any users are found to be overriding ``DEFAULT_MENU_DEPTH`` using ``YOURAPP_DEFAULT_MENU_DEPTH`` in their Django settings (and with Python configured to surface warnings) will be presented with the following warning:

.. container:: highlight warning-sample

    PendingDeprecationWarning: The YOURAPP_DEFAULT_MENU_DEPTH setting is deprecated. The override value from your project's Django settings will no longer have any affect once support is removed in two versions time. Once removed, the default menu depth will be fixed at 2. Where this is unsuitable, use the 'depth' argument to specify an alternative value when using the render_menu() tag."

There are a few things worth noting here:

-   This warning is intended for your app's core users, who will be using prefixed setting names in their Django settings to override your app's behaviour, so prefixed setting names are used in the warning text also.
-   The second sentence ends with **"removed in two versions time"** because ``PendingDeprecationWarning`` was used as the ``warning_class`` value for the ``DeprecatedAppSetting`` definition in :ref:`step one <remove_step_1>`. Using ``DeprecationWarning`` (or a subclass of it) instead would result in that sentence ending with **"removed in the next version"**.
-   The last couple of sentences come from the ``additional_guidance`` value that was used for the ``DeprecatedAppSetting`` definition in :ref:`step one <remove_step_1>`.

And, just in case there are any users out there using ``settings.DEFAULT_MENU_DEPTH`` or ``settings.get("DEFAULT_MENU_DEPTH")`` in their projects to request the setting value from your settings helper (less likely, but perfectly possible), Cogwheels will present those users with a different (but similar) warning:

.. container:: highlight warning-sample

    PendingDeprecationWarning: The DEFAULT_MENU_DEPTH app setting is deprecated. Please remove any references to it from your project, as continuing to reference it will cause an exception to be raised once support is removed in two versions time. Once removed, the default menu depth will be fixed at 2. Where this is unsuitable, use the 'depth' argument to specify an alternative value when using the render_menu() tag.

There are a few things worth noting here:

-   Because this warning is triggered by users referencing the settings from your app's settings helper using non-prefixed setting names (like you do in your app), non-prefixed setting names are used in this message also.
-   The second sentence ends with **"removed in two versions time"** because ``PendingDeprecationWarning`` was used as the ``warning_class`` value for the ``DeprecatedAppSetting`` definition in :ref:`step one <remove_step_1>`. Using ``DeprecationWarning`` (or a subclass of it) instead would result in that sentence ending with **"removed in the next version"**.
-   The last couple of sentences come from the ``additional_guidance`` value that was used for the ``DeprecatedAppSetting`` definition in :ref:`step one <remove_step_1>`.


.. _remove_step_4:

4. Updating the documentation
-----------------------------

How exactly you document your app settings is up to you, but it's highly recommended that you have some kind of reference to help users understand what behaviour they can override in your app and how.

.. seealso:: :doc:`/best-practice/documenting-your-app-settings`

If you do have a settings reference, you should update the entry for the existing setting to mark it as deprecated. If you are using Sphinx to build documentation, use the :ref:`deprecated directive<deprecated-directive>` for this.


.. _remove_step_5:

5. Mentioning the deprecation in the release notes
--------------------------------------------------

How and where you define the release notes for your app is up to you, but it's highly recommended that you include information about any new deprecations. For this release, you should include a note about the deprecation, detailing how users might update their code, and when support will be removed entirely (e.g. version 1.8 in this example). This might look something like::

    Deprecations
    ============

    The following features have been deprecated in this version. Unless otherwise stated, support for deprecated features is retained for two minor releases, so you have until version **1.8** to make any necessary changes to your implementation.


    The ``YOURAPP_DEFAULT_MENU_DEPTH`` setting has been deprecated
    --------------------------------------------------------------

    Overrides will continue to work until **1.8**, but after this, they will be ignored, and the default depth will be fixed at ``2``. If you are using this setting to override the default ``depth`` value used by the ``render_menu()`` tag, you should update your code to use the ``depth`` argument of ``render_menu()`` instead, like so:

    ..code:: html
        {% render_menu depth=1 %}

    If you are importing ``yourapp.conf.settings`` anywhere within your project, and are requesting ``DEFAULT_MENU_DEPTH`` the setting value from it (as an attribute: ``settings.DEFAULT_MENU_DEPTH``, or using the ``get()``: ``settings.get("DEFAULT_MENU_DEPTH")``), use the value ``2`` instead to silence any deprecation warnings.


In the next release (1.7)
=========================


.. _remove_step_6:

6. Use stronger deprecation warnings to indicate removal is now imminent
------------------------------------------------------------------------

Assuming you followed the example and used ``PendingDeprecationWarning`` (or a custom sub-class of it) as the ``warning_class`` value for the ``DeprecatedAppSetting`` definition in :ref:`step one <remove_step_1>`, all you should need to do here is update that ``DeprecatedAppSetting`` to use ``DeprecationWarning`` (or a custom sub-class of it) as the ``warning_class`` value instead, like so:

.. code-block:: python
    :emphasize-lines: 11

    # yourapp/conf/settings.py

    from cogwheels import BaseAppSettingsHelper, DeprecatedAppSetting

    
    class MyAppSettingsHelper(BaseAppSettingsHelper):

        deprecations = (
            DeprecatedAppSetting(
                setting_name="DEFAULT_MENU_DEPTH",
                warning_category=DeprecationWarning,
                additional_guidance=(
                    "Once removed, the default menu depth will be fixed at 2. "
                    "Where this is unsuitable, use the 'depth' argument to "
                    "specify an alternative value when using the render_menu() "
                    "tag."
                ),
            ),
        )




Doing so should change the both the class used for any deprecation warnings raised in relation to this setting, and the descriptive text used for those warnings to read "in the next version" instead of "in two versions time".


In the following release (1.8)
==============================


.. _remove_step_7:

7. Removing support for the deprecated setting
----------------------------------------------
    
Remember the code we updated in :ref:`step two <remove_step_2>`? Now that we don't have to support override values any longer, we can just hardcode our default value, and don't need to request a value from the settings helper any longer. The modified code might look something like this::

    # yourapp/templatetags/menu_tags.py

    from yourapp.conf import settings

    def render_menu(root_page, depth=None):
        if depth is None:
            depth = 2
        # do stuff 
        ...

Or, better still::

    # yourapp/templatetags/menu_tags.py

    from yourapp.conf import settings

    def render_menu(root_page, depth=2):
        # do stuff
        ...



.. _remove_step_8:

8. Removing the deprecated setting itself
-----------------------------------------

First, we'll update our app's settings helper definition again. This time, to remove the ``DeprecatedAppSetting`` definition that was added back in :ref:`step 1 <remove_step_1>`:

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
                    "specify an alternative value when using the render_menu() "
                    "tag."
                ),
            ),
        )

Next, we'll remove any lines related to the old setting from the ``defaults.py`` module: 

.. code-block:: python
        :emphasize-lines: 9-10

        # yourapp/conf/defaults.py

        ...

        # -------------------
        # Deprecated settings
        # -------------------

        # To be removed in 1.8.
        DEFAULT_MENU_DEPTH = 2


.. _remove_step_9:

9. Updating the documentation
------------------------------

How exactly you do this is up to you, but to avoid any ambiguity, it's recommended that you either remove the entry for the setting from your 'Settings reference' (reviewing any references to it in the process), or, if.


.. _remove_step_10:

10. Mentioning the backwards-incompatible change in the release notes
---------------------------------------------------------------------

This version of your app will now behave differently for any users still relying on the setting to control the default ``depth`` value used by ``render_menu()``, and will raise an exception for anyone requesting the value from your settings helper. Because of this, it's important to let users know about the changes in your release notes. Your addition might look something like this::

    Backwards-incompatible changes
    ==============================

    Following a standard deprecation period a two minor releases, the following functionality has now been removed.


    The ``YOURAPP_DEFAULT_MENU_DEPTH`` setting is no longer supported
    -----------------------------------------------------------------

    The default ``depth`` value used by ``render_menu()`` is now fixed at ``2``. If you wish to render menus of a different depth, you should use the ``depth`` argument of ``render_menu()`` to indicate this, like so:

    ..code:: html
        {% render_menu depth=1 %}

    If you are importing ``yourapp.conf.settings`` anywhere within your project, and are requesting ``DEFAULT_MENU_DEPTH`` the setting value from it (as an attribute: ``settings.DEFAULT_MENU_DEPTH``, or using the ``get()``: ``settings.get("DEFAULT_MENU_DEPTH")``), update your code to use the value ``2`` instead.



