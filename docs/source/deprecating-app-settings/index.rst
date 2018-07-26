========================
Deprecating app settings
========================

Deprecation is an inevitable part of managing any reusable app over time, and this applies especially to overridable app settings, which your users likely depend on to make your app function in a way that is most useful to them. 

Cogwheels was designed with this in mind, and has features built-in to help you manage app setting deprecation in an standardised, effective way.

There are currently three deprecation scenarios that are Cogwheels helps to cater for:

A setting removal
    
    You're simply planning to remove support for a setting.

    You're willing to support the setting for couple more feature releases, but would like to prompt any users using it, to make them aware that support will be removed soon, and that they should review their implementation.

    For more information, see: :doc:`removal-example`

A setting rename

    You're changing the name of a setting. There aren't any changes to the type or range of supported override values, or to the way override values affect your app's behaviour.

    You're willing to support override values defined using the previous setting name for a couple more feature releases, but would like to prompt those users to update their Django settings to use the new setting name.

    For more information, see: :doc:`rename-example`

A single setting replacement

    You're adding a new setting that allows users to override behaviour in a way that makes a single existing setting redundant. Although it is a clear logical successor for the existing setting, there may be differences in how override values affect your app's behaviour, and possibly changes to the type or range of override values that are supported.

    You're willing to support override values defined using the previous setting for a couple more feature releases, but would like to prompt those users to find out more about how the new setting works, and start using it instead of the existing one.

    For more information, see: :doc:`single-replacement-example`

A multiple setting replacement

    As above, but the new setting is replacing several existing settings, instead of just one.

    For more information, see: :doc:`multi-replacement-example`


Example deprecation scenarios
=============================

.. toctree::
    :maxdepth: 2
    :titlesonly:

    removal-example
    rename-example
    single-replacement-example
    multi-replacement-example
    using-custom-warning-classes


