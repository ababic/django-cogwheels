============================
Release packaging guidelines
============================

.. contents::
    :local:
    :depth: 2


Preparing a new release
=======================

Follow the steps outlined below to prep changes in your fork:

1.  Merge any changes from ``upstream/master`` into your fork's ``master``
    branch.

    .. code-block:: console

        $ git fetch upstream
        $ git checkout master
        $ git merge upstream/master

2.  From your fork's ``master`` branch, create a new branch for preparing the
    release, e.g.:

    .. code-block:: console

        $ git checkout -b release-prep/1.X.X

3.  Ensure ``CHANGELOG.md`` is up-to-date with details of any changes since
    the last release.

4.  Ensure the release notes for the new version are up-to-date
    updated in ``docs/source/releases/``.

    If preparing a final feature (or major) release, also ensure any references to 
    'alpha' or 'beta' are removed.

5.  Ensure the new version's release notes and are referenced in 
    ``docs/source/releases/index.rst``. 

6.  ``cd`` into the ``docs`` directory to check documentation-related stuff:

    .. code-block:: console

        $ cd docs

7.  Check for and correct any spelling errors raised by sphinx:

    .. code-block:: console

        $ make spelling

8.  Check that the docs build okay, and fix any errors raised by sphinx:

    .. code-block:: console

        $ make html

9.  Update the ``__version__`` value ``cogwheels/__version__.py`` to reflect the new
    release version.

10. Commit changes so far:

    .. code-block:: console
    
        $ git commit -am 'Bumped version and updated release notes'
       
11. Update the source translation files by running the following from the
    project's root directory:

    .. code-block:: console

        $ django-admin.py makemessages -l en
        $ git commit -am 'Update source translation files'

12. Push all outstanding changes to GitHub:

    .. code-block:: console
    
        git push

13. Submit your changes as a PR to the main repository via
    https://github.com/ababic/django-cogwheels/compare


Packaging and pushing to PyPi
=============================

When satisfied with the PR for preparing the files:

1.  From https://github.com/ababic/django-cogwheels/pulls, merge the PR into the
    ``master`` branch using the "Merge commit" option.

2.  Locally, ``cd`` to the project's root directory, checkout the ``master``
    branch, and ensure the local copy is up-to-date: 

    .. code-block:: console
        
        $ workon cogwheels-upstream
        $ git checkout master
        $ git pull

3.  Ensure dependencies are up-to-date:

    .. code-block:: console

        $ pip install -e '.[packaging]' -U

4.  Create a new tag for the new version and push to GitHub:

    .. code-block:: console
        
        $ git tag -a v1.X.X
        $ git push --tags

5.  Create a new source distribution and universal wheel for the new version

    .. code-block:: console

        $ python setup.py sdist
        $ python setup.py bdist_wheel --universal

        
7.  Push files to the PyPi test environment and test that new distribution installs okay:

    .. code-block:: console

        $ twine upload dist/* -r pypitest
        $ mktmpenv
        $ pip install -i https://test.pypi.org/simple/ --extra-index-url https://pypi.org/simple django-cogwheels

8.  Reactivate the original ``virtualenv``:

    .. code-block:: console

        $ deactivate
        $ workon cogwheels-upstream

8. Push new distribution files to live PyPi:

    .. code-block:: console

        $ twine upload dist/* -r pypi

9. On the releases page in GitHub (https://github.com/ababic/django-cogwheels/releases), Update the new release description with a link to the release notes in the relevant release notes in the docs (e.g. https://django-cogwheels.readthedocs.io/en/latest/releases/1.X.X.html).
    

