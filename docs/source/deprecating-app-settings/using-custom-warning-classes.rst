====================================================
Using custom deprecation warning classes in your app
====================================================

All of the deprecation examples in the Cogwheels documentation assume that you're defining and using custom deprecation warning classes for your app, and that you 'cycle' those warnings before start work on features for each new release. 

For developers unfamiliar with this approach, this guide outlines the benefits of this approach, and provides examples of how to adopt it yourself. 

.. contents::
    :local:
    :depth: 1


What are the benefits?
======================

The main arguments for defining and using custom deprecation warnings within your app are:

- Developers typically see the name of the warning class when a warning is raised, so it’s a convenient way to provide them with more information. For example, from the warning class ``RemovedInWagtail21Warning``, you can easily ascertain that:   
    - ``Wagtail`` is the app that raised the warning.
    - Support for the deprecated functionality will be removed in ``2.1``.
- As a maintainer, cycling deprecation warnings (ensuring that warnings raised using ``PendingDeprecationWarning`` in the previous version are raised with ``DeprecationWarning`` in the new one) is easier, because:
    - You do not have to update quite as much code each time.
    - Anywhere using the warning class being removed will raise an ``ImportError``, which (If your test suite is even half-decent) should help you identify all of the places in your code where support for deprecated behaviour should be removed.
- Developers only interested in specific classes of warning can more easily identify warnings from your app if they need to.


An example implementation
=========================

The following example assumes that:

-   The latest release version of your app is ``1.5``.
-   The next release version of your app will be ``1.6``.
-   The latest version was just released, so deprecation warnings have not yet been cycled.

If you were to add custom deprecation warning classes for your app now, they would look something like this:

.. code-block:: python

    # yourapp/utils/deprecation.py

    class RemovedInYourApp17Warning(DeprecationWarning):
        pass


    removed_in_next_version_warning = RemovedInYourApp17Warning


    class RemovedInYourApp18Warning(PendingDeprecationWarning):
        pass


    removed_in_following_version_warning = RemovedInYourApp18Warning


Because we're starting work on a new release, any code using the ``DeprecationWarning`` class to raise warnings has now reached the end of it's deprecation period, so support for the deprecated functionality can be removed, and the warning should no needs to be raised.

Any warnings raised using the ``PendingDeprecationWarning`` class must be updated to reflect the fact that deprecation is now `imminent` rather than `pending`, which you'll do using the new ``RemovedInYourApp17Warning`` class instead.

For example, this: 

.. code-block:: python

    import warnings

    ...

    warnings.warn(
        "Deprecation warning message here",
        category=PendingDeprecationWarning
    )

Would be updated to: 

.. code-block:: python

    import warnings
    from yourapp.utils.deprecation import RemovedInYourApp17Warning

    ...

    warnings.warn(
        "Deprecation warning message here",
        category=RemovedInYourApp17Warning
    )

Any functionality deprecated between now and the release of version ``1.6`` should use the ``RemovedInYourApp18Warning``, as the functionality won't be removed for another two versions.


Cycling the warnings for future releases
----------------------------------------

Following on from the example above, let's pretend that:

-   You have just released version ``1.6`` of your app.
-   The next release version of your app is now ``1.7``.

Any code currently using the ``RemovedInYourApp17Warning`` warning class has now reached the end of it's deprecation period, so support for the deprecated functionality can be removed, and the warnings should no longer be raised.

Any code currently using the ``RemovedInYourApp18Warning`` should continue to use the same warning class name, but the warning class itself must be updated to subclass ``DeprecationWarning`` instead of ``PendingDeprecationWarning``, to indicate those deprecations are now `imminent` rather than `pending`.

So, your custom deprecation classes should be updated like so:

.. code-block:: python

    # yourapp/utils/deprecation.py

    # RemovedInYourApp17Warning is no longer needed, so has been removed

    class RemovedInYourApp18Warning(DeprecationWarning):
        # This previously subclassed ``PendingDeprecationWarning`` instead
        pass


    removed_in_next_version_warning = RemovedInYourApp18Warning


    class RemovedInYourApp19Warning(PendingDeprecationWarning):
        # Newly deprecated functionality should use this class
        pass


    removed_in_following_version_warning = RemovedInYourApp19Warning
