================================
Using setting values in your app
================================

To use setting values in your app, simply import the settings module wherever it is needed, and reference settings as attributes of the module.

.. contents::
    :local:
    :depth: 2

.. _getting_raw_values:

Getting a 'raw' setting value
=============================

Reference a setting as a direct attribute of the setting module will return values **exactly** as they are defined in ``defaults.py``, or by the user in their Django settings (no transformation is applied).

.. code-block:: console

    >>> from yourproject.conf import settings

    >>> settings.MAX_ITEMS_PER_ORDER
    5
    >>> type(settings.MAX_ITEMS_PER_ORDER)
    int

    >>> settings.ORDER_ITEM_MODEL
    'yourproject.SimpleOrderItem'
    >>> type(settings.ORDER_ITEM_MODEL)
    str

    >>> settings.DISCOUNTS_BACKEND
    'yourproject.discount_backends.simple'
    >>> type(settings.DISCOUNTS_BACKEND)
    str

    >>> settings.ORDER_FORM_CLASS
    'yourproject.forms.OrderForm'
    >>> type(settings.ORDER_FORM_CLASS)
    str


.. _raw_value_process:

Behind the scenes:
------------------

When any setting value is requested (be it directly from the ``settings`` module, or using the one of the ``models``, ``modules`` or ``objects`` helper attributes explained below), Cogwheels takes the following steps to identify the raw value:

1.  If the requested setting has been marked for deprecation, a helpfully worded ``DeprecationWarning`` is raised to help inform developers of the change.
2.  The Django settings module is then checked for a relevant 'override' setting value. If found, this value is returned.
3.  If the requested setting is a 'replacement' for a deprecated setting, the Django settings module is checked again for a relevant 'override' setting value, this time using the **deprecated** setting name. If found, a helpfully worded ``DeprecationWarning`` is raised before the value is returned.
4.  If no 'override' value was found, the default value from your ``defaults`` module will be returned.
5.  The resulting value is cached, so that the above steps can be bypassed the next time a value for this setting is requested.

.. NOTE :: To learn more about how setting deprecation works, see: :doc:`deprecation-handling` 


.. _getting_model_values:

Getting Django models from setting values
=========================================

For settings that refer to Django models, you can use the settings module's ``models`` attribute to access model classes themselves. For example: 

.. code-block:: console

    >>> from yourproject.conf import settings

    >>> settings.models.ORDER_ITEM_MODEL
    yourproject.models.SimpleOrderItem

    >>> from django.db.models import Model
    >>> issubclass(settings.models.ORDER_ITEM_MODEL, Model)
    True


.. _model_value_process:

Behind the scenes:
------------------

When you request an attribute from ``settings.models`` instead of the ``settings`` module directly, Cogwheels takes the following steps to get the value you require:

1. First, an appropriate 'raw' setting value is identified, following the standard process (see: :ref:`raw_value_process`).
2. The raw value is checked to ensure that it is a string. If it is not, a helpfully worded ``OverrideValueTypeInvalid`` or ``DefaultValueTypeInvalid`` error is raised.
3. The string value is checked to ensure it it matches the expected format (e.g. 'app_label.Model'). If it does not, a helpfully worded ``OverrideValueFormatInvalid`` or ``DefaultValueFormatInvalid`` error is raised.
4. Cogwheels attempts to import the model using Django's ``django.apps.apps.get_model()`` method. If the import fails, a helpfully worded ``OverrideValueNotImportable`` or ``DefaultValueNotImportable`` error is raised.
5. The successfully imported model is cached, so that the above steps can be bypassed the next time it is requested.

.. NOTE :: To learn more about the errors raised by Cogwheels, and to see some examples, see: :doc:`error-handling` 


.. _getting_module_values:

Getting Python modules from setting values
==========================================

For settings that refer to Python modules, you can use the settings module's ``modules`` attribute to access the modules themselves. For example:
    
.. code-block:: console

    >>> from yourproject.conf import settings

    >>> settings.modules.DISCOUNTS_BACKEND
    <module 'yourproject.discount_backends.simple' from '/system/path/to/your-django-project/yourproject/discount_backends/simple.py'>

    >>> type(settings.modules.DISCOUNTS_BACKEND)
    module


.. _module_value_process:

Behind the scenes:
------------------

When you request an attribute from ``settings.modules`` instead of the ``settings`` module directly, Cogwheels takes the following steps to get the value you require:

1. First, an appropriate 'raw' setting value is identified, following the standard process (see: :ref:`raw_value_process`).
2. The raw value is checked to ensure that it is a string. If it is not, a helpfully worded ``OverrideValueTypeInvalid`` or ``DefaultValueTypeInvalid`` error is raised.
3. The string value is checked to ensure it it matches the expected format (e.g. 'project.app.module'). If it does not, a helpfully worded ``OverrideValueFormatInvalid`` or ``DefaultValueFormatInvalid`` error is raised.
4. Cogwheels attempts to import the module using Python's ``importlib.import_module()``. If the import fails, a helpfully worded ``OverrideValueNotImportable`` or ``DefaultValueNotImportable`` error is raised.
5. The successfully imported module is cached, so that the above steps can be bypassed the next time it is requested.

.. NOTE :: To learn more about the errors raised by Cogwheels, and to see some examples, see: :doc:`error-handling` 


.. _getting_object_values:

Getting classes, functions and other Python objects from setting values
=======================================================================

For settings that refer to classes, functions, or other importable python objects, you can use the settings module's ``objects`` attribute to access those objects. For example:

.. code-block:: console

    >>> from yourproject.conf import settings

    >>> settings.objects.ORDER_FORM_CLASS
    yourproject.forms.OrderForm

    >>> from django.forms import Form
    >>> issubclass(settings.objects.ORDER_FORM_CLASS, Form)
    True


.. _object_value_process:

Behind the scenes:
------------------

When you request an attribute from ``settings.objects`` instead of the ``settings`` module directly, Cogwheels takes the following steps to get the value you require:

1. First, an appropriate 'raw' setting value is identified, following the standard process (see: :ref:`raw_value_process`).
2. The raw value is checked to ensure that it is a string. If it is not, a helpfully worded ``OverrideValueTypeInvalid`` or ``DefaultValueTypeInvalid`` error is raised.
3. The string value is checked to ensure it it matches the expected format (e.g. 'project.app.module.object'). If it does not, a helpfully worded ``OverrideValueFormatInvalid`` or ``DefaultValueFormatInvalid`` error is raised.
4. Cogwheels attempts to import the module using Python's ``importlib.import_module()``, then uses ``getattr`` to attempt to retrieve the object from the module. If either of these steps fail, a helpfully worded ``OverrideValueNotImportable`` or ``DefaultValueNotImportable`` error is raised.
5. The successfully imported object is cached, so that the above steps can be skipped next time the same object is requested.

.. NOTE :: To learn more about the errors raised by Cogwheels, and to see some examples, see: :doc:`error-handling` 
