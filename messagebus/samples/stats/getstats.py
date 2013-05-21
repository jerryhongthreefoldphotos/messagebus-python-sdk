#!/usr/bin/env python
# -*- coding: utf-8 -*-

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
import sys
import os

path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', '..'))
if not path in sys.path:
    sys.path.insert(1, path)
del path

from messagebus import MessageBusStatsClient, MessageBusResponseError


api_key = '7215ee9c7d9dc229d2921a40e899ec5f'
uri = 'api-v4.messagebus.com'


def get_stats():
    try:
        stats_client = MessageBusStatsClient(api_key, uri=uri)
        results = stats_client.get_stats()
    except MessageBusResponseError, error:
        print error.message
    else:
        print results


if __name__ == '__main__':
    get_stats()