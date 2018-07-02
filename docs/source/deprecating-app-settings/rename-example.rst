==========================
A 'setting rename' example
==========================

.. contents::
    :local:
    :depth: 2


What we're looking to achieve
=============================

Let's pretend that the latest release of your app has two overridable app settings, which appear in the ``defaults.py`` module like so:

.. code-block:: python

    # yourapp/conf/defaults.py

    # -------------------
    # Admin / UI settings
    # -------------------

    FLATMENU_MENU_ICON = 'list-ol'

    FLAT_MENUS_EDITABLE_IN_WAGTAILADMIN = True


The naming convention here is a little inconsistent, so you would like to rename the ``FLATMENU_MENU_ICON`` setting to ``FLAT_MENUS_MENU_ICON``.


Some assumptions
================

In the following example, we're going to assume that:

-   The latest release version of your app was ``1.5``.
-   The next release version of your app will be ``1.6``.
-   You have a deprecation policy that continues to support deprecated behaviour for two 'feature releases' before support is dropped completely. So, in each example, we'll be aiming to remove support completely in version ``1.8``.
-   Rather than using Python's built-in ``DeprecationWarning`` and ``PendingDeprecationWarning`` classes directly, your app defines it's own warning classes to aid with deprecation, which are cycled with each feature release version. The classes have already been updated for version ``1.6``, and so look something like this:

.. code-block:: python

    # yourapp/utils/deprecation.py

    class RemovedInYourApp17Warning(DeprecationWarning):
        pass


    removed_in_next_version_warning = RemovedInYourApp17Warning


    class RemovedInYourApp18Warning(PendingDeprecationWarning):
        pass


    removed_in_following_version_warning = RemovedInYourApp18Warning


Implementing the deprecation
============================


In version ``1.6``
------------------


1. Adding the new setting
~~~~~~~~~~~~~~~~~~~~~~~~~

First, let's add a setting using the new name to ``defaults.py``. We also want to mark the existing setting in some way that will help us remember the state of things. Our updated ``defaults.py`` module should look something like this:


.. code-block:: python

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

    FLATMENU_MENU_ICON = 'list-ol'  # Remove me in v1.8!


2. Declaring the deprecation
~~~~~~~~~~~~~~~~~~~~~~~~~~~~


Next, we'll update the settings helper definition for our app, so that it knows how to handle requests for setting values:


.. code-block:: python

    # yourapp/conf/settings.py

    from cogwheels import BaseAppSettingsHelper, DeprecatedAppSetting
    from yourapp.utils.deprecation import RemovedInYourApp18Warning

    
    class MyAppSettingsHelper(BaseAppSettingsHelper):

        # NOTE: 'deprecations' should always be defined as a tuple, even if you're only 
        # deprecating a single setting 
        deprecations = (
            DeprecatedAppSetting(
                setting_name='FLATMENU_MENU_ICON',
                renamed_to='FLAT_MENUS_MENU_ICON',
                warning_category=RemovedInYourApp18Warning, # use this class when raising deprecation warnings
            ),
        )

    ...


3. Updating the app code
~~~~~~~~~~~~~~~~~~~~~~~~

This takes care of the 'definintion' side of things, but we still have to update our code to use the new setting. Let's imagine that our code currently looks something like this:


.. code-block:: python

    # yourapp/modeladmin.py

    from wagtail.contrib.modeladmin.options import ModelAdmin

    from yourapp.conf import settings


    class FlatMenuAdmin(ModelAdmin):
        menu_icon = settings.FLATMENU_MENU_ICON  # << old setting name
    ...


For a 'setting rename', all you have to do is change any references to the old name to the new one, like so:


.. code-block:: python

    # yourapp/modeladmin.py

    from wagtail.contrib.modeladmin.options import ModelAdmin

    from yourapp.conf import settings


    class FlatMenuAdmin(ModelAdmin):
        menu_icon = settings.FLAT_MENUS_MENU_ICON  # << that's better!
    ...


4. Warning your users
~~~~~~~~~~~~~~~~~~~~~

Because your settings helper knows about the rename, ``settings.FLAT_MENUS_MENU_ICON`` will behave a little differently:

1.  Cogwheels first looks for an override setting using the new name, which is the 'ideal' scenario, and where we want all our users to be eventually. For example:

    .. code-block:: python
        
        # userproject/settings/base.py

        ...

        # ---------------------------------
        # Overrides for ``your-django-app``
        # ---------------------------------

        FLAT_MENUS_MENU_ICON = 'icon-new'


2.  Next, Cogwheels will look for an override setting defined using the old name. For example:

    .. code-block:: python
        
        # userproject/settings/base.py

        ...

        # ---------------------------------
        # Overrides for ``your-django-app``
        # ---------------------------------

        FLATMENU_MENU_ICON = 'icon-old'  # I'm old-skool!

    Now, although we're still happy to support this value for a while longer, we want users to know that this setting has been renamed, and that they should use the new setting name if they wish for their override value to continue working in future versions. So, Cogwheels raises the following warning:

    .. code-block:: console
        
        RemovedInYourApp18Warning(
            The YOURAPP_FLATMENU_MENU_ICON setting has been renamed to YOURAPP_FLAT_MENUS_MENU_ICON. 
            Please update your project's Django settings to use this new name instead, or your
            override will fail to work in future versions.
        )

3. If no override setting was found, Cogwheels resorts to using the default value for the new setting, as you'd expect.


Now, even though the app settings module is intended for private use in your app, there may well be cases where some users are importing it, in order to make use of the setting value, for example:

.. code-block:: python

    # userproject/modeladmin.py

    from wagtail.contrib.modeladmin.options import ModelAdmin

    from yourapp.conf import settings


    class MyCustomFlatMenuAdmin(ModelAdmin):
        menu_icon = settings.FLATMENU_MENU_ICON  # << old setting name


These users also need to be warned about the rename, so that they can make the appropriate changes to their code. So, Cogwheels automatically raises the following warning:

.. code-block:: console
    
    RemovedInYourApp18Warning(
        The FLATMENU_MENU_ICON app setting has been renamed to FLAT_MENUS_MENU_ICON.
        You should update your code to reference this new setting instead.
    )


Taking care of the deprecating in your code is one thing, but you'll also want to update your documentation to reflect the new changes, by:

1.  Mentioning the deprecation in the ``1.6`` release notes
2.  Adding an entry for the new setting to the "Settings reference", and updating any references to the old setting entry to the new one
3.  Updating the entry for the existing setting in the "Settings reference", using Sphinx's `deprecated directive <http://www.sphinx-doc.org/en/stable/markup/para.html#directive-deprecated>`_ to mark the old setting as deprecated, for example::
        .. deprecated:: 1.6
            Use :ref:`YOURAPP_FLAT_MENUS_MENU_ICON` instead.


In version ``1.7``
------------------

Cogwheels assumes that you're already using custom warning classes to manage deprecations within your app, and 'cycling' them regularly with each feature release. Assuming your warning classes have been cycled for this version already, they should now look something like this:

.. code-block:: python

    # yourapp/utils/deprecation.py

    class RemovedInYourApp18Warning(DeprecationWarning):
        pass


    removed_in_next_version_warning = RemovedInYourApp18Warning


    class RemovedInYourApp19Warning(PendingDeprecationWarning):
        pass


    removed_in_following_version_warning = RemovedInYourApp19Warning


With ``RemovedInYourApp18Warning`` subclassing ``DeprecationWarning`` instead of ``PendingDeprecationWarning``, we don't have to make any further changes, because we're already using this warning class in our settings helper definition, remember?

.. code-block:: python

    # yourapp/conf/settings.py

    from cogwheels import BaseAppSettingsHelper, DeprecatedAppSetting
    from yourapp.utils.deprecation import RemovedInYourApp18Warning

    
    class MyAppSettingsHelper(BaseAppSettingsHelper):

        # NOTE: 'deprecations' should always be defined as a tuple, even if you're only 
        # deprecating a single setting 
        deprecations = (
            DeprecatedAppSetting(
                setting_name='FLATMENU_MENU_ICON',
                renamed_to='FLAT_MENUS_MENU_ICON',
                warning_category=RemovedInYourApp18Warning, # No changes needed here!
            ),
        )

    ...


Users will continue to see the exact same warning messages that they did in version ``1.6``, only the warnings will be classed as 'iminent' rather than 'pending', which is exactly what we want.


In version ``1.8``
------------------

We're finally ready to remove support for the old setting (YEY!), so the following steps should be taken:

1.  Remove the default value for the old setting from ``defaults.py`` 
    
    .. code-block:: python

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

    FLATMENU_MENU_ICON = 'list-ol'  # DELETE ME!


2. Remove the deprecation definition from your app's setting helper in ``settings.py``


    .. code-block:: python

    # yourapp/conf/settings.py

    from cogwheels import BaseAppSettingsHelper, DeprecatedAppSetting
    from yourapp.utils.deprecation import RemovedInYourApp18Warning

    
    class MyAppSettingsHelper(BaseAppSettingsHelper):

        # NOTE: 'deprecations' should always be defined as a tuple, even if you're only 
        # deprecating a single setting 
        deprecations = ()  # I'm so empty! 

    ...
    

3. Announce the breaking change in the version ``1.8`` release notes.

4. Remove the entry for the old setting from the "Settings reference" page of the documentation.
