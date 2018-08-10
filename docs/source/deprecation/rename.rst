=======================
Renaming an app setting
=======================

.. warning ::
    This examples assumes you are using custom deprecation warnings classes to help manage deprecations for your app. If you are not, you may find it tricky to follow in parts. It isn't a requirement that you use custom deprecation warning classes for app setting deprecations, but it will make your life (and following this example) easier. Check out the following guide: :doc:`/best-practice/custom-deprecation-warning-classes`.

For the sake of this example, we're going to pretend that:

-   The latest release version of your app is **1.5**.
-   The next release version of your app will be **1.6**.
-   You have a deprecation policy that continues to support deprecated behaviour for two 'feature releases' before support is dropped completely. So, we'll be looking to do that in version **1.8**.

What we want to acheive
=======================

Let's pretend that we have currently have a ``ICON_FOR_MAIN_MENUS`` settings, which appears in the ``conf/defaults.py`` module like so:

.. code-block:: python
    
    # yourapp/conf/defaults.py

    ICON_FOR_MAIN_MENUS = 'list-ol'

We've decided that we want to rename the setting to ``MAIN_MENUS_ADMIN_UI_ICON`` to make it more descriptive, and to get rid of the redundant 'FOR' from the setting name.


How we'll achieve it
====================

As with any deprecation process, the change will span several releases, so we'll have to do things in stages. Let's take a while and plan what we'll need to do and when:

For our upcoming release (1.6), we'll want to:
    - Add a new setting with the new name
    - Mark the old setting as 'pending deprecation'
    - Update our code to simultaneously respect override values using the new OR old setting name.
    - Warn anyone using the old setting name the old setting is 'pending deprecation', and encourage them to use the new setting instead.
    - Update the documentation

In the next release (1.7) we'll want to:
    - Warn anyone still using the old setting name that the old setting is now offically deprecated, and encourage them to use the new setting instead.

In the following release (1.8) we'll want to:
    - Update our code to only support override values defined using the new setting name
    - Stop warning


Changes required for the upcoming release (1.6)
===============================================


1. Updating ``conf/defaults.py``
--------------------------------

First, you'll want to add a setting using the new name to ``defaults.py``. You may find it helpful to mark the deprecated setting here in some way, to remind you and other app maintainers that it has been deprecated.

.. code-block:: python
    :emphasize-lines: 7,22

    # yourapp/conf/defaults.py

    # -------------------
    # Admin / UI settings
    # -------------------

    FLAT_MENUS_MENU_ICON = 'list-ol'

    FLAT_MENUS_EDITABLE_IN_WAGTAILADMIN = True

    # -------------------
    # Other settings
    # -------------------

    ...

    # -------------------
    # Deprecated settings
    # -------------------
    # These need to stick around until support is dropped completely

    FLATMENU_MENU_ICON = 'list-ol'  # Replaced by FLAT_MENUS_MENU_ICON. Remove in v1.8


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
                setting_name="FLATMENU_MENU_ICON",
                renamed_to="FLAT_MENUS_MENU_ICON",
                warning_category=RemovedInYourApp18Warning,
            ),
        )

There are a few things worth noting here:

- If you need to define ``deprecations`` on your ``SettingsHelper`` class, it needs to be a tuple, even if you only need a single ``DeprecatedAppSetting`` definition.
- In the ``DeprecatedAppSetting`` definition, setting names are supplied as strings, and we're still using internal/non-prefixed setting names (e.g. ``"FLATMENU_MENU_ICON"`` rather than ``"YOURAPP_FLATMENU_MENU_ICON"``).
- The ``warning_category`` used in the ``DeprecatedAppSetting`` definition here will be passed to Python's ``warnings.warn()`` method when raising deprecation warnings related to this setting. It should be a subclass of ``DeprecationWarning`` or ``PendingDeprecationWarning``.


3. Updating your app code
-------------------------

The above steps take care of the deprecation definition, but we still have to update our code to use the new setting. Let's imagine our code currently looks something like this:

.. code-block:: python
    :emphasize-lines: 9

    # yourapp/modeladmin.py

    from wagtail.contrib.modeladmin.options import ModelAdmin

    from yourapp.conf import settings


    class FlatMenuAdmin(ModelAdmin):
        menu_icon = settings.FLATMENU_MENU_ICON

This code will now raise the following deprecation warning:

.. code-block:: console
    
    RemovedInYourApp18Warning: The FLATMENU_MENU_ICON app setting has been
    renamed to FLAT_MENUS_MENU_ICON. Please update your code to reference the
    new setting, as continuing to reference FLATMENU_MENU_ICON will cause an
    exception to be raised once support is removed in two versions time.

.. NOTE:: If users of your app are referencing ``settings.FLATMENU_MENU_ICON`` or calling ``settings.get('FLATMENU_MENU_ICON')`` for any reason, this warning will be raised by their code also.

To resolve this for a 'setting rename', all you have to do is change any references to the old name to the new one, like so:

.. code-block:: python
    :emphasize-lines: 9

    # yourapp/modeladmin.py

    from wagtail.contrib.modeladmin.options import ModelAdmin

    from yourapp.conf import settings


    class FlatMenuAdmin(ModelAdmin):
        menu_icon = settings.FLAT_MENUS_MENU_ICON

Because your settings helper knows all it needs to about the rename, ``settings.FLAT_MENUS_MENU_ICON`` will do some extra work to support users still using the old setting name:

1.  It first looks for an override setting using the new name (which is the 'ideal' scenario), and where we want all our users to be eventually. For example:

    .. code-block:: python

        # userproject/settings/base.py

        # ---------------------------------
        # Overrides for ``your-django-app``
        # ---------------------------------

        YOURAPP_FLAT_MENUS_MENU_ICON = 'icon-new'  # I'm cutting edge!

2.  Next, Cogwheels will look for an override setting defined using the old name. For example:

    .. code-block:: python
        
        # userproject/settings/base.py

        # ---------------------------------
        # Overrides for ``your-django-app``
        # ---------------------------------

        YOURAPP_FLATMENU_MENU_ICON = 'icon-old'  # I'm old-skool!

3.  If no override setting was found, Cogwheels resorts to using the default value for the new setting, as you'd expect.

Although we’re still happy to the deprecated setting for a couple more versions, we want to make users aware that the setting has been replaced. So, Cogwheels will raise the following warning:

.. code-block:: console
    
    RemovedInYourApp18Warning: The YOURAPP_FLATMENU_MENU_ICON setting has been 
    renamed to YOURAPP_FLAT_MENUS_MENU_ICON. Please update your Django settings
    to use the new setting, otherwise the app will revert to it's default
    behaviour once support for YOURAPP_FLATMENU_MENU_ICON is removed in two
    versions time.


4. Updating your documentation
------------------------------

Raising a deprecation warning with Python is certainly helpful, but you'll also want to update your documentation to reflect the new changes, by:

1.  Mentioning the deprecation in the **1.6** release notes
2.  Adding an entry for the new setting to the "Settings reference", and updating any references to the old setting entry to the new one, for example::

        .. _FLAT_MENUS_MENU_ICON:

        ``YOURAPP_FLAT_MENUS_MENU_ICON``
        -------------------------------------------

        .. versionadded:: 1.6
            Replaces :ref:`FLATMENU_MENU_ICON`.

        Value type expected:
            ``string``
        Default value:
            ``"list-ol"``

        Use this setting to change the icon used to represent 'Flat menus' in the admin UI. 

        Any icon class name from _`Font Awesome V4 <https://fontawesome.com/icons/>` is supported.

3.  Updating the entry for the existing setting in the "Settings reference", using Sphinx's `deprecated directive <http://www.sphinx-doc.org/en/stable/markup/para.html#directive-deprecated>`_ to mark the old setting as deprecated, for example::

        .. deprecated:: 1.6
            Use :ref:`FLAT_MENUS_MENU_ICON` instead.


Changes required for the next release (1.7)
===========================================

Provided you are defining and using custom deprecation warnings within your app (using the approach outlined in: :doc:`/best-practice/custom-deprecation-warning-classes`), and cycle those warnings for this release, no further changes should be needed in regards to this specific deprecation. The message text for any warnings raised in relation to this setting should change automatically to read 'in the next version' instead of 'in two versions time'.


Changes required for the following release (1.8)
================================================

We're finally ready to remove support for the old setting (YEY!), so the following steps should be taken:

1.  Remove the default value for the old setting from ``defaults.py`` 
    
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
