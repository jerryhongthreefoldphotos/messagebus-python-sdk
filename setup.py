#!/usr/bin/env python                                                                                                                                        

"""
  Copyright 2013 Mail Bypass, Inc.

  Licensed under the Apache License, Version 2.0 (the "License"); you may
  not use this file except in compliance with the License. You may obtain
  a copy of the License at

      http://www.apache.org/licenses/LICENSE-2.0

  Unless required by applicable law or agreed to in writing, software
  distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
  WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
  License for the specific language governing permissions and limitations
  under the License.
"""

import setuptools

setuptools.setup(
    name='messagebus',
    version='4.1.0',
    author='Message Bus',
    author_email='support@messagebus.com',
    packages=['messagebus'],
    scripts=[],
    url='http://github.com/messagebus/messagebus-python-sdk',
    license='Apache',
    description='Message Bus Python sdk.',
    long_description=open('README.md').read(),
    tests_require=["mox", "pylint"],
    test_suite="messagebus.tests",
    zip_safe=False)