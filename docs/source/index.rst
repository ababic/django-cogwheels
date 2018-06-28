=======================================
Welcome to the Cogwheels documentation!
=======================================

Cogwheels is a tool for developers of reusable Django apps, to help them implement 'overridable app-specific settings' in a simple, standardised way. 


A note to fellow app developers
===============================

As an author of reusable Django apps, I understand that adding a new dependency to your project is something you'd rather avoid:

- A dependency can tie you to specific versions of Python or Django, making it difficult to support new versions yourself.
- A dependency's features change over time, and it's another thing you have to keep track of.
- A dependency often has other dependencies of it's own, leading to unnecessarily complicated dependency graphs.

Allow me to offer you a few reassurances:

- The current feature set is stable and unlikely to change substantially, and the code only uses officially supported Python and Django features under the hood. As such, compatibility updates should be trivial, and I plan to keep on top of that (I depend on this app too)!
- Unless it would add be an unreasonable amount of development effort (or is simply not possible), I will always follow a standard deprecation cycle of two 'feature releases' before adding breaking changes to any public APIs. Full details will always be made available in release notes, too.
- Other than requiring a compatible versions of Python and Django, the app currently has no other dependencies, and likely never will.


Compatibility
=============

The current version of Cogwheels is tested for compatibility with:

- Python 3.4 to 3.7
- Django 1.11 to 2.1


Documentation index
===================

.. toctree::
    :maxdepth: 2
    :titlesonly:

    installation
    overriding-settings
    error-handling
    deprecation-handling
    how-to
    example-implementations
    contributing/index
    releases/index
