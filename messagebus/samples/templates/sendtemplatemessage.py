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

path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', '..'))
if not path in sys.path:
    sys.path.insert(1, path)
del path

from messagebus import MessageBusTemplatesClient, MessageBusResponseError

api_key = '7215ee9c7d9dc229d2921a40e899ec5f'
uri = 'templates.messagebus.com'
template_key = '66f6181bcb4cff4cd38fbc804a036db6'


def send_email():
    message = {
        'rcpt_name': 'Tim',
        'rcpt_email': 'tim@example.com',
        'sender_name': 'Bob',
        'sender_email': 'bob@example.com',
        'plaintext_body': 'Plain text body',
        'some_key': 'some text value'
    }
    templates_client = MessageBusTemplatesClient(api_key, uri=uri)
    try:
        result = templates_client.send_messages(template=template_key, messages=[message])
    except MessageBusResponseError, error:
        print error.message
    else:
        print('Success with status code: %s' % result['status_code'])
        print('Send results: %s' % result['results'])


if __name__ == '__main__':
    send_email()
