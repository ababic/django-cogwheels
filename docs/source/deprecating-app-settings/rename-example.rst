==========================
A 'setting rename' example
==========================

This guide demonstrates the steps required to rename a setting, following a standard 'two release' deprecation process. 

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
-   You are defining and using custom deprecation warnings within your app, using the approach outlined in: :doc:`using-custom-warning-classes`.


Implementing the deprecation
============================


In version ``1.6``
------------------


1. Adding the new setting
~~~~~~~~~~~~~~~~~~~~~~~~~

First, we'll add a setting using the new name to ``defaults.py``. We also want to mark the existing setting in ``defaults.py`` in some way, to help us remember that it’s deprecated. Our updated ``defaults.py`` module should look something like this:


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

The above steps take care of the deprecation definition, but we still have to update our code to use the new setting. Let's imagine that our code currently looks something like this:


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

    Now, although we’re still happy to support this value for a while longer, we want users to know that this setting has been renamed, and that they should use the new setting name if they wish for their override value to continue working in future versions. So, Cogwheels raises the following warning:

    .. code-block:: console
        
        RemovedInYourApp18Warning(
            The YOURAPP_FLATMENU_MENU_ICON setting has been renamed to YOURAPP_FLAT_MENUS_MENU_ICON. Please update your Django settings to use the new setting, otherwise the app will revert to its default behavior in two versions time (when support for YOURAPP_FLATMENU_MENU_ICON will be removed entirely). 
        )

3. If no override setting was found, Cogwheels resorts to using the default value for the new setting, as you'd expect.


Even though the app settings module might not be intended for public use, there may well be cases where user of your app are importing it in order to make use of setting values, for example:

.. code-block:: python

    # userproject/modeladmin.py

    from wagtail.contrib.modeladmin.options import ModelAdmin

    from yourapp.conf import settings


    class MyCustomFlatMenuAdmin(ModelAdmin):
        menu_icon = settings.FLATMENU_MENU_ICON  # << old setting name


These users also need to be warned about the rename, so that they can make the appropriate changes to their code. So, Cogwheels automatically raises the following warning:

.. code-block:: console
    
    RemovedInYourApp18Warning(
        The FLATMENU_MENU_ICON app setting has been renamed to FLAT_MENUS_MENU_ICON. Please update your code to use 'settings.FLAT_MENUS_MENU_ICON' instead, as continuing to reference 'settings.FLATMENU_MENU_ICON' will raise an AttributeError when support is removed in two versions time.",
    )


Raising a deprecating in your code is one thing, but you'll also want to update your documentation to reflect the new changes, by:

1.  Mentioning the deprecation in the ``1.6`` release notes
2.  Adding an entry for the new setting to the "Settings reference", and updating any references to the old setting entry to the new one
3.  Updating the entry for the existing setting in the "Settings reference", using Sphinx's `deprecated directive <http://www.sphinx-doc.org/en/stable/markup/para.html#directive-deprecated>`_ to mark the old setting as deprecated, for example::

        .. deprecated:: 1.6
            Use :ref:`YOURAPP_FLAT_MENUS_MENU_ICON` instead.


In version ``1.7``
------------------

If you are defining and using custom deprecation warnings within your app (using the approach outlined in: :doc:`using-custom-warning-classes`), and cycle those warnings for this release, no further changes should be needed in this release in regards to this specific deprecation. The message text for any warnings raised in relation to this setting should change automatically to read 'in the next version' instead of 'in two versions time'.


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

        from cogwheels import BaseAppSettingsHelper

        
        class MyAppSettingsHelper(BaseAppSettingsHelper):

            # NOTE: 'deprecations' should always be defined as a tuple, even if you're only 
            # deprecating a single setting 
            deprecations = ()  # I'm so empty! 

        ...
    

3. Announce the breaking change in the version ``1.8`` release notes.

4. Remove the entry for the old setting from the "Settings reference" page of the documentation.
