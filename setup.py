import os
from setuptools import setup, find_packages
from apputils import __version__

with open(os.path.join(os.path.dirname(__file__), 'README.rst')) as readme:
    README = readme.read()

# allow setup.py to be run from any path
os.chdir(os.path.normpath(os.path.join(os.path.abspath(__file__), os.pardir)))

base_url = "https://github.com/ababic/django-cogwheels/"
download_url = '%starball/v%s' % (base_url, __version__)

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

setup(
    name="django-cogwheels",
    version=__version__,
    author="Andy Babic",
    author_email="andyjbabic@gmail.com",
    description=(
        "A handy API to allow you to more easily offer and maintain 'user "
        "overridable settings' in your Django package, framework or reuseable "
        "app."
    ),
    long_description=README,
    packages=find_packages(),
    license="MIT",
    keywords="django package reusable app settings config API utility",
    download_url=download_url,
    url=base_url,
    include_package_data=True,
    zip_safe=False,
    classifiers=[
        "Environment :: Web Environment",
        "Intended Audience :: Developers",
        "Operating System :: OS Independent",
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Framework :: Django',
        'Framework :: Django :: 1.11',
        'Framework :: Django :: 2.0',
        'Topic :: Internet :: WWW/HTTP',
        "Topic :: Internet :: WWW/HTTP :: Dynamic Content",
    ],
    python_requires='>=3.4,<3.7',
    extras_require={
        'testing': testing_extras,
        'development': development_extras,
        'docs': documentation_extras,
    },
)
