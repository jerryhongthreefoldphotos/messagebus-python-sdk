#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
  Copyright 2014 Message Bus

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
import time

path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', '..'))
if not path in sys.path:
    sys.path.insert(1, path)
del path

from messagebus import MessageBusReportsClient

api_key = '7215ee9c7d9dc229d2921a40e899ec5f'
uri = 'api.messagebus.com'

report_params = dict(
    report_type='blocklist',
    channel_key='4033dea0a3b711e28b5490b8d0fafdcc',
    format='JSON')

if __name__ == '__main__':
    reports_client = MessageBusReportsClient(api_key, uri=uri)

    # Create report request
    create_job_result = reports_client.create_report(report_params)
    print 'Report created with key: ' + create_job_result['report_key']

    # Check for report's completion
    report_status = reports_client.get_report_status(create_job_result['report_key'])
    while report_status['report_status'] == 'running':
        print 'Report status: ' + report_status['report_status']
        report_status = reports_client.get_report_status(create_job_result['report_key'])
        time.sleep(5)

    # Download completed report
    if report_status['report_status'] == 'done':
        print 'Downloading report to blocklist.json'
        reports_client.get_report(create_job_result['report_key'], open('blocklist.json', 'wa'))

