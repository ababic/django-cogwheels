=================
Development guide
=================

Running the project locally
===========================

If you'd like a runnable Django project to help with development of this app, follow these steps to get started (Mac only). The development environment has some additional dependencies (``ipdb``, ``django-extensions``) to help with debugging:

1.  If ``virtualenvwrapper`` isn't already installed, install it from a Terminal window/console, by running:
    
    .. code-block:: console

        pip install virtualenvwrapper


2.  In a Terminal window, ``cd`` to the project’s root directory, and run:

    .. code-block:: console

        mkvirtualenv cogwheels
        setvirtualenvproject
        pip install -e '.[development,docs]' -U

3.  Create a copy of the development settings and urls: 

    .. code-block:: console

        cp cogwheels/development/settings.py.example cogwheels/development/settings.py
        cp cogwheels/development/urls.py.example cogwheels/development/urls.py

4.  Create ``manage.py`` by copying the example provided:

    .. code-block:: console

        cp manage.py.example manage.py
        
5.  Run the migrate command to set up the database tables:

    .. code-block:: console

        python manage.py migrate

6.  Run the project using ``django-extension``'s ``runserver_plus`` command: 
    
    .. code-block:: console

        python manage.py runserver_plus

Your local copies of ``settings/development.py`` and ``manage.py`` will be ignored by git when you push any changes, as will anything in the ``development/`` app, so feel free to change those as much as you like.


Running the tests suite
=======================

It's important that any new code is tested before submitting. To quickly test code in your active development environment, you should first ensure you have the necessary requirements installed, by running:

.. code-block:: console

    pip install -e '.[testing,docs]' -U

Then, run the following command to execute tests:

.. code-block:: console

    python runtests.py

If you want to run only part of the test suite, you can enter the path of an app, module, or specific test case, like so:

.. code-block:: console

    python runtests.py apptests.app_name.module_name.TestCaseName


Or if you want to measure test coverage, run:

.. code-block:: console

    coverage --source=apptests runtests.py apptests.tests.module_name.TestCaseName
    coverage report

Testing in a single environment is a quick and easy way to identify obvious issues with your code. However, it's important to test changes in other environments too, before they are submitted. In order to help with this, the project is configured to use ``tox`` for multi-environment tests. They take longer to complete, but running them is as simple as running:

.. code-block:: console

    tox

You might find it easier to set up a Travis CI service integration for your fork in GitHub (look under **Settings > Apps and integrations** in GitHub's web interface for your fork), and have Travis CI run tests whenever you commit changes. The test configuration files already present in the project should work for your fork too, making it a cinch to set up.
