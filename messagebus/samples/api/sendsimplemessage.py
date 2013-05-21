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

from messagebus import MessageBusAPIClient, MessageBusResponseError


api_key = '7215ee9c7d9dc229d2921a40e899ec5f'
uri = 'api-v4.messagebus.com'


def send_emails():
    try:
        api_client = MessageBusAPIClient(api_key, uri=uri)
        message_jane = {
            'to_email': 'jane.smith@example.com',
            'to_name': 'Jane Smith',
            'from_email': 'noreply@example.com',
            'from_name': 'Example Corporation',
            'subject': 'Single Message Sample for Jane Smith',
            'custom_headers': {'envelope-sender': 'bounces@bounces.example.com', 'reply-to': 'reply@example.com'},
            'plaintext_body': 'This message to Jane Smith is a test sent by the Python Message Bus client library.',
            'html_body': '<html><body>This message to Jane Smith is a test sent by the Python Message Bus sdk.</body></html>',
            'session_key': 'DEFAULT',
        }

        message_john = {
            'to_email': 'john.doe@example.com',
            'to_name': 'John Doe',
            'from_email': 'noreply@example.com',
            'from_name': 'Example Corporation',
            'subject': 'Single Message Sample for John Doe',
            'custom_headers': {'envelope-sender': 'bounces@bounces.example.com', 'reply-to': 'reply@example.com'},
            'plaintext_body': 'This message to John Doe is a test sent by the Python Message Bus client library.',
            'html_body': '<html><body>This message to John Doe is a test sent by the Python Message Bus sdk.</body></html>',
            'session_key': 'DEFAULT',
        }
        results = api_client.send_messages([message_jane, message_john])
    except MessageBusResponseError, error:
        print error.message
    else:
        print results


if __name__ == '__main__':
    send_emails()