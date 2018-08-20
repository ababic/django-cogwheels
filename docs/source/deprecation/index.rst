========================
Deprecating app settings
========================

Deprecation is an inevitable part of managing any reusable app over time, and this applies especially to overridable app settings, which your users likely depend on to make your app function in a way that fits their requirements.

Cogwheels was designed with this in mind, and has features built-in to help you manage app setting deprecation in an standardised, effective way. You will still have to do some work, but Cogwheels should certainly make your life easier.

There are currently four deprecation scenarios that Cogwheels helps to cater for:

Removing an app setting
    You wish to remove a setting, and are not planning to replace it with another setting.

Renaming an app setting
    There are no changes in functionality, but you wish to rename the setting to improve consistency or to make the name more descriptive / accurate.

Replacing a single setting with a new one
    You wish to add a new setting that logically replaces an existing one, but there are some functional differences between the two.

Replacing multiple settings with a new one
    You wish to add add a new setting that logically replaces several existing ones.


Example scenarios
=================

The best way to show how Cogwheels helps with app setting deprecation is with some examples. The following example scenarios explain how to implement each type of deprecation, starting with the current release, right through to removing the deprecated setting two releases later.

.. toctree::
    :maxdepth: 1

    removal
    rename
    replacement-single
    replacement-multiple
    


