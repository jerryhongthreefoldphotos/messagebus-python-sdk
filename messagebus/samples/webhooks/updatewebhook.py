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

path = os.path.abspath(
    os.path.join(os.path.dirname(__file__), '..', '..', '..'))
if not path in sys.path:
    sys.path.insert(1, path)
del path

from messagebus import MessageBusWebhooksClient, MessageBusResponseError


api_key = '7215ee9c7d9dc229d2921a40e899ec5f'
webhook_key = '2ff80e9159b517704ce43f0f74e6e247'

def update_webhook():
    webhook_config = dict(enabled=True)

    try:
        webhook_client = MessageBusWebhooksClient(api_key)
        result = webhook_client.update_webhook(webhook_key, webhook_config)
    except MessageBusResponseError, error:
        raise error
    else:
        print result


def get_webhook():
    try:
        webhooks_client = MessageBusWebhooksClient(api_key)
        result = webhooks_client.get_webhook(webhook_key)
    except MessageBusResponseError, error:
        print error.message
    else:
        print result

if __name__ == '__main__':
    update_webhook()
    get_webhooks()
