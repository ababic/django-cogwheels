==============================================
Welcome to the django-cogwheels documentation!
==============================================

``django-cogwheels`` is a tool for developers of reusable Django apps, helping them to implement 'overridable app-specific settings' in a simple, standarised way. Once implemented, developers using the app in their projects will be able to override default behaviour by adding alternative values to their Django settings module.


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


Documentation index
===================

.. toctree::
    :maxdepth: 2
    :titlesonly:
