=============================
Documenting your app settings
=============================

In order for users to know what they can override (and how), you'll need to document the settings somewhere.

If you don't have one already, it's highly recommended that you add a "Settings reference" page to your documentation, similar to the one in the one in the `wagtailmenus documentation
<https://wagtailmenus.readthedocs.io/en/latest/settings_reference.html>`_.

You should clearly explain what each setting does, what type of value is expected (if not obvious), and any acceptability criteria that apply to the value (such as maximum length, upper/lower boundaries, or whether the options are limited to a specific set of values).


Some handy Sphinx directives
============================

If you're writing your documentation in `reStructuredText <http://docutils.sourceforge.net/rst.html>`_ and using `Sphinx <http://www.sphinx-doc.org/en/master/>`_, there are a couple of directives available that come in very handy when documenting app settings.


.. _versionadded-directive:

`versionadded <http://www.sphinx-doc.org/en/master/usage/restructuredtext/directives.html#directive-versionadded>`_
-------------------------------------------------------------------------------------------------------------------

Use this when documenting new app settings so that your users know when the setting was added. This will help users viewing the documentation to understand whether or not they can use the feature in their project, since they may well be using an earlier version.

Use directly after the heading for the relevant app setting, like so:: 

    .. _NEW_APP_SETTING:

    ``YOURAPP_NEW_APP_SETTING``
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~

    .. versionadded:: 1.6
        Replaces :ref:`OLD_APP_SETTING`

Adding an explanation is entirely optional. However, if you do add one, note that there must be no blank line between the directive head and the explanation.


.. _deprecated-directive:

`deprecated <http://www.sphinx-doc.org/en/master/usage/restructuredtext/directives.html#directive-deprecated>`_
---------------------------------------------------------------------------------------------------------------

This directive is designed specifically to help you mark specific features as deprecated, and so comes in useful when deprecating, renaming or replacing app settings.

Use directly after the heading for the relevant app setting, like so:: 

    .. _OLD_APP_SETTING:

    ``YOURAPP_OLD_APP_SETTING``
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~
    
    .. deprecated:: 1.6
        Use :ref:`NEW_APP_SETTING` instead

Adding an explanation is entirely optional. However, if you do add one, note that there must be no blank line between the directive head and the explanation.


.. _versionchanged-directive:

`versionchanged <http://www.sphinx-doc.org/en/master/usage/restructuredtext/directives.html#directive-versionchanged>`_
-----------------------------------------------------------------------------------------------------------------------

If you make changes to the way an app setting works (e.g. a change to the type or range of accepted values, or to the side effects), then use this directive to explain when it changed and how. This will help users viewing the documentation to understand whether or not they can use the feature in a particular way in their project, since they may well be using an earlier version.

Use directly after the heading for the relevant app setting, like so::

    .. _SOME_APP_SETTING:

    ``YOURAPP_SOME_APP_SETTING``
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~

    .. versionchanged:: 1.6
        The value must be a list (tuples are no longer supported)

Unlike the other directives mentioned above, the explanation is required for ``versionchanged``. Note that there must be no blank line between the directive head and the explanation.
