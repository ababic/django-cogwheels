import os
from codecs import open
from setuptools import setup

here = os.path.abspath(os.path.dirname(__file__))

packages = ['cogwheels']

# Essential dependencies
requires = []

# Testing dependencies
testing_extras = [
    "coverage",
]

# Documention dependencies
documentation_extras = [
    "pyenchant>=2.0",
    "Sphinx>=1.7.4",
    "sphinxcontrib-spelling>=1.4",
    "sphinx_rtd_theme>=0.3",
]

# Development dependencies
development_extras = [
    "ipdb",
    "werkzeug",
    "django-extensions",
]

about = {}
with open(os.path.join(here, 'cogwheels', '__version__.py'), 'r', 'utf-8') as f:
    exec(f.read(), about)

with open('README.rst', 'r', 'utf-8') as f:
    readme = f.read()


setup(
    name=about['__title__'],
    version=about['__version__'],
    description=about['__description__'],
    long_description=readme,
    long_description_content_type='text/x-rst',
    author=about['__author__'],
    author_email=about['__author_email__'],
    url=about['__url__'],
    packages=packages,
    package_dir={'cogwheels': 'cogwheels'},
    include_package_data=True,
    install_requires=requires,
    license=about['__license__'],
    zip_safe=False,
    classifiers=(
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "Operating System :: OS Independent",
        "Natural Language :: English",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.4",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
        "Framework :: Django",
        "Framework :: Django :: 1.11",
        "Framework :: Django :: 2.0",
        "Topic :: Internet :: WWW/HTTP",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ),
    python_requires='>=3.4,<3.7',
    extras_require={
        'testing': testing_extras,
        'development': development_extras,
        'docs': documentation_extras,
    },
)
