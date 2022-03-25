#!/usr/bin/env python
# -*- coding: utf-8 -*-

from setuptools import setup, find_packages
import io

with io.open('README.md', 'r', encoding='utf8') as f:
    long_description = f.read()

setup(
    name='sms-python-client',
    version='1.0.4',
    description='Client library to send SMS using Altiria SMS API',
    author='altiria',
    author_email='soporte@altiria.com',
    url='https://github.com/altiria/sms-python-client',
    packages=find_packages(exclude=["tests.*",  "tests"]),
    include_package_data=True,
    install_requires=[
        'requests'
    ],
    classifiers=(
        'Development Status :: 5 - Production/Stable',
        'License :: OSI Approved :: MIT License',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7'
    ),
    test_suite='tests.suite',
    long_description=long_description,
    long_description_content_type='text/markdown'
)
