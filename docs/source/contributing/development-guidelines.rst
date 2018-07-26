======================
Development guidelines
======================

.. contents:: Contents
    :local:
    :depth: 2


Developing the project locally
==============================

If you'd like a runnable Django project to help with development of this app, follow these steps to get started (Mac only). The development environment has some additional dependencies (``ipdb``, ``django-extensions``) to help with debugging:

1.  If ``virtualenvwrapper`` isn't already installed, install it by running:
    
    .. code-block:: console

        $ pip install virtualenvwrapper

2.  ``cd`` to the project’s root directory, and run:

    .. code-block:: console

        $ mkvirtualenv cogwheels
        $ setvirtualenvproject
        $ pip install -e '.[development,docs]' -U

3.  Create a copy of the development settings and URLs: 

    .. code-block:: console

        $ cp cogwheels/development/settings.py.example cogwheels/development/settings.py
        $ cp cogwheels/development/urls.py.example cogwheels/development/urls.py

4.  Create ``manage.py`` by copying the example provided:

    .. code-block:: console

        $ cp manage.py.example manage.py
        
5.  Run the migrate command to populate the database:

    .. code-block:: console

        $ python manage.py migrate

6.  Run the project using ``django-extension``'s ``runserver_plus`` command: 
    
    .. code-block:: console

        $ python manage.py runserver_plus

Your local copies of ``settings/development.py`` and ``manage.py`` will be ignored by git when you push any changes, as will anything in the ``development/`` app, so feel free to change those as much as you like.


Running the test suite
======================

It's important that any new code is tested before submitting. To quickly test code in your active development environment, you should first ensure you have the necessary requirements installed, by running:

.. code-block:: console

    $ pip install -e '.[testing]' -U

Use the following command to execute tests:

.. code-block:: console

    $ python runtests.py

If you want to run only part of the test suite, you can enter the path of an app, module, or specific test case, like so:

.. code-block:: console

    $ python runtests.py cogwheels.app_name.test_module_name.TestCaseName

If you want to measure coverage, run:

.. code-block:: console

    $ coverage --source=cogwheels runtests.py cogwheels.app_name.test_module_name.TestCaseName
    $ coverage report


Testing against multiple Python/Django versions
-----------------------------------------------

Testing in a single environment is a quick and easy way to identify obvious issues with your code. However, it's important to test changes in other environments too, as Cogwheels has to support multiple Python and Django versions.

To help with this, Cogwheels uses ``tox``, and Travis CI. The easiest way for you to run multi-environment tests is to set up a Travis CI integration for your fork in GitHub (https://github.com/settings/installations), and have Travis CI run tests whenever you commit changes. The test configuration files already present in the project should work for you too.


Building the documentation
==========================

If you make any updates to the documentation to accompany a pull request, please follow these steps to help spot any potential issues before submitting:

1.  Install the necessary requirements by running:

    .. code-block:: console

        $ pip install -e '.[docs]' -U

2.  ``cd`` to the project’s `docs` directory:

    .. code-block:: console

        $ cd docs

3.  Run the following to check for any spelling errors raised by sphinx, and fix any issues where possible:

    .. code-block:: console

        $ make spelling


4.  Run the following to check that the documentation still builds okay, and fix any issues where possible:

    .. code-block:: console

        $ make html
