==============
How to install
==============

1.  If your app's repository has a ``setup.py`` file, add ``django-cogwheels`` to the ``install_requires`` list that is passed to the ``setuptools``' ``setup()`` method:

    .. code-block:: python

    # your-django-app/setup.py

    from setuptools import setup

    ...
    
    setup(
        name='your-django-project',
        description="An app that does something super useful.",
        classifiers=(
            "Programming Language :: Python",
            "Programming Language :: Python :: 3",
            "Programming Language :: Python :: 3.4",
            "Programming Language :: Python :: 3.5",
            "Programming Language :: Python :: 3.6",
            "Framework :: Django",
            "Framework :: Django :: 1.11",
            "Framework :: Django :: 2.0",
            ...
        ),
        install_requires=[
            'django-cogwheels',
            ...
        ],
        ...
    )

2.  Install the package using pip: 

    .. code-block:: console

        pip install django-cogwheels
    

3.  ``cd`` into your project's root app directory:
    
    .. code-block:: console

        cd your-django-app/yourapp/


4.  Create a ``conf`` app using the cogwheels Django app template:

    .. code-block:: console

        django-admin.py startapp conf --template=https://github.com/ababic/cogwheels-conf-app/zipball/master


5.  Add the settings you want to support, along with any default values, to the newly created ``defaults.py``. For example:

    .. code-block:: python

        # your-django-app/yourapp/conf/defaults.py

        """
        Any setting you wish to support in your app must be defined here
        with a sensible default value.

        DO:

        - Use upper case names for settings
        - Feel free to use values of any built-in python type

        DON'T:

        - Prefix setting names with 'YOURAPP_' or similar (that isn't necessary here)
        - Put all your configuration in one giant dictionary setting (that's just lazy!)

        """

        MAX_ITEMS_PER_ORDER = 5
        SEND_ORDER_CONFIRMATION_EMAILS = True


        """
        Django model settings
        ---------------------

        For settings that refer to Django models, the default value should be a string
        in the format 'app_name.Model', e.g.:
        """

        ORDER_ITEM_MODEL = 'yourproject.SimpleOrderItem'


        """
        Python module settings
        ----------------------

        For settings that refer to Python modules, the default value should be an
        'import path' string, e.g.:
        """

        DISCOUNTS_BACKEND = 'yourproject.discount_backends.simple'


        """
        Other importable python object settings
        ---------------------------------------

        For settings that refer to classes, methods, or other importable Python
        objects, the default value should be an 'object import path' string, e.g.:
        """

        ORDER_FORM_CLASS = 'yourproject.forms.OrderForm'


