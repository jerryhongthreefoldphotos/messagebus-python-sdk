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

from messagebus import MessageBusTemplatesClient, MessageBusResponseError


api_key = '7215ee9c7d9dc229d2921a40e899ec5f'
uri = 'templates-v4-jy01-prod.messagebus.com'


def create_template():
    template = {
        "to_name": "{{rcpt_name}}",
        "to_email": "{{rcpt_email}}",
        "from_name": "{{sender_name}}",
        "from_email": "{{sender_email}}",
        "return_path": "{{return_path}}",
        "options": {
            "track_clicks": True
        },
        "custom_headers": {
            "x-messagebus-sdk": "py"
        },
        "subject": "Hey! {{rcpt_name}}",
        "plaintext_body": "Plain text content",
        "html_body": "<HTML>Hey! <br>{{rcpt_name}}</br></HTML>"
    }

    try:
        template_client = MessageBusTemplatesClient(api_key, uri=uri)
        results = template_client.create_template(template)
    except MessageBusResponseError, error:
        print error.message
    else:
        print "Successfully created template with key %s" % results['template_key']


def get_templates():
    try:
        template_client = MessageBusTemplatesClient(api_key, uri=uri)
        results = template_client.get_templates()
    except MessageBusResponseError, error:
        print error.message
    else:
        print "Saved templates:"
        for template in results['templates']:
            print "Template Key: %s" % template['template_key']


if __name__ == '__main__':
    create_template()
    get_templates()
