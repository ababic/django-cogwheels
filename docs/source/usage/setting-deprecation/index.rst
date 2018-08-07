=============================
App setting deprecation guide
=============================

Deprecation is an inevitable part of managing any reusable app over time, and this applies especially to overridable app settings, which your users likely depend on to make your app function in a way that is most useful to them. 

Cogwheels was designed with this in mind, and has features built-in to help you manage app setting deprecation in an standardised, effective way. You'll still have to do some work, but Cogwheels should certainly make your life easier.

All of the examples in this section assume that you are using custom deprecation warnings classes within your app to help manage deprecations, so it might be best for you to start by reading :doc:`/best-practice/custom-deprecation-warning-classes`.

There are currently four deprecation scenarios that are Cogwheels helps to cater for:

Setting removal
    You are simply planning to remove a setting.

    You are willing to support the setting for couple more feature releases, but would like to prompt any users using it, to make them aware that support will be removed soon, and that they should review their implementation.

    See: :doc:`removal`

Setting renaming
    You are changing the name of a setting. There aren't any changes to the type or range of supported override values, or to the way override values affect your app's behaviour.

    You are willing to support override values defined using the previous setting name for a couple more feature releases, but would like to prompt those users to update their Django settings to use the new setting name.

    See: :doc:`rename`

Setting replacement (single)
    You are adding a new setting that allows users to override behaviour in a way that makes a single existing setting redundant. Although it is a clear logical successor for the existing setting, there may be differences in how override values affect your app's behaviour, and possibly changes to the type or range of override values that are supported.

    You are willing to support override values defined using the previous setting for a couple more feature releases, but would like to prompt those users to find out more about how the new setting works, and start using it instead of the existing one.

    See: :doc:`replacement-single`

Setting replacement (multiple)
    As above, but the new setting is replacing several existing settings, instead of just one.

    See: :doc:`replacement-multiple`


.. toctree::
    :hidden:
    :maxdepth: 2

    removal
    rename
    replacement-single
    replacement-multiple
    


