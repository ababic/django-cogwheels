==============================================
Separating ``defaults.py`` and ``settings.py``
==============================================

This is supported. However, you will need to set the ``defaults_path`` attribute on your ``SettingsHelper`` class, so that it knows where to find the default values. For example:

.. code-block:: python

    # yourapp/settings.py

    class MyAppSettingsHelper(BaseAppSettingsHelper):
        defaults_path = 'yourapp.some_other_place.defaults'
