import os
import sys
from setuptools import setup

VERSION = "0.0.1"


def get_requirements():
    basedir = os.path.dirname(__file__)
    with open(os.path.join(basedir, 'requirements.txt')) as f:
        return [l.strip() for l in f]


if sys.argv[-1] == 'test':
    status = os.system('./virtualenv-run.sh flake8 leeroy/*.py')
    sys.exit(status)


setup(
    name="observatory",
    version=VERSION,
    url="https://github.com/lonnen/observatory",
    license="BSD",
    author="Lonnen",
    author_email="lonnen@mozilla.com",
    description="Observatory keeps notes about what is deployed where",
    include_package_data=True,
    zip_safe=False,
    platforms="any",
    install_requires=get_requirements(),
    packages=["observatory"],
    classifiers=[
        # From http://pypi.python.org/pypi?%3Aaction=list_classifiers
        "Development Status :: 1 - Planning",
        #"Development Status :: 2 - Pre-Alpha",
        #"Development Status :: 3 - Alpha",
        #"Development Status :: 4 - Beta",
        #"Development Status :: 5 - Production/Stable",
        #"Development Status :: 6 - Mature",
        #"Development Status :: 7 - Inactive",
        "Environment :: Web Environment",
        "License :: OSI Approved :: MIT License",
        "Operating System :: MacOS",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: POSIX",
        "Operating System :: POSIX :: Linux",
        "Programming Language :: Python",
        "Programming Language :: Python :: 2",
        "Programming Language :: Python :: 2.6",
        "Programming Language :: Python :: 2.7",
        "Topic :: Internet :: WWW/HTTP :: WSGI :: Application",
        "Topic :: Software Development :: Quality Assurance",
        "Topic :: Software Development :: Documentation",
        "Topic :: Software Development :: Bug Tracking",
        "Topic :: Software Development :: Version Control",
        "Topic :: Utilities",
    ]
)
