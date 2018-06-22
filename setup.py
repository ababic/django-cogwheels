import os
from setuptools import setup, find_packages
from apputils import __version__, stable_branch_name

with open(os.path.join(os.path.dirname(__file__), 'README.rst')) as readme:
    README = readme.read()

# allow setup.py to be run from any path
os.chdir(os.path.normpath(os.path.join(os.path.abspath(__file__), os.pardir)))

base_url = "https://github.com/ababic/django-app-utils/"
download_url = '%starball/v%s' % (base_url, __version__)
branch_url = "%stree/stable/%s" % (base_url, stable_branch_name)

# Testing dependencies
testing_extras = [
    'coverage',
]

# Documention dependencies
documentation_extras = [
    'pyenchant>=2.0',
    'Sphinx>=1.7.4',
    'sphinxcontrib-spelling>=1.4',
    'sphinx_rtd_theme>=0.3',
]

# Development dependencies
development_extras = [
    'ipdb',
    'werkzeug',
    'django-extensions',
    'django>=2.0,<2.1',
]

setup(
    name="django-app-utils",
    version=__version__,
    author="Andy Babic",
    author_email="andyjbabic@gmail.com",
    description="",
    long_description=README,
    packages=find_packages(),
    license="MIT",
    keywords="django reusable app settings config utils",
    download_url=download_url,
    url=branch_url,
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
    install_requires=[],
    python_requires='>=3.4,<3.7',
    extras_require={
        'testing': testing_extras,
        'development': development_extras,
        'docs': documentation_extras,
    },
)
