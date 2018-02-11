from distutils.core import setup
from setuptools import find_packages

setup(
    name = 'amqppublisher',
    version = '2.9979', # speed of light
    packages = find_packages(exclude=['bin*', 'doc*', 'test*','debian*']),
    author = "Alexander Kasper",
    license = 'GNU General Public License v3 or later (GPLv3+)',
    long_description = open('README.rst').read(),
    description = "AMQP 0.9 publisher with minimal dependencies",
    url = "https://github.com/banduri/amqp-publisher",
    install_requires = ['pika'],
    entry_points = {
        'console_scripts': ['amqppublisher=amqppublisher.main:commandline'],
    },
 
    include_package_data = True,
    classifiers = [
        'Development Status :: 3 - Alpha',
        'Framework :: pika',
        'Intended Audience :: Developers',
        'Intended Audience :: Information Technology',
        'Intended Audience :: System Administrators',
        'Topic :: System :: Distributed Computing',
        'Topic :: System :: Systems Administration',
        'Topic :: Utilities',
        'Natural Language :: English',
        'Operating System :: POSIX',
        'License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)',
        'Programming Language :: Python :: 3 :: Only',
        'Programming Language :: Python :: 3.2',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.6',
],
)
