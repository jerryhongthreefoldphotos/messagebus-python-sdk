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

version = '5.0.0'
max_messages = 100
max_template_messages = 25
timeout = 300
debug_level = 0
reconnect_interval = 60

uri = 'api.messagebus.com'
template_uri = 'templates.messagebus.com'

user_agent = 'MessageBusAPI:%s-PYTHON:%s' % (
    version, '.'.join(map(str, sys.version_info[:3])))

end_points = {
    'message_emails_send': '/v5/messages/send',
    'template_emails_send': '/v5/templates/send',
    'template': '/v5/template/%(template_key)s',
    'templates': '/v5/templates/',
    'templates_version': '/v5/templates/version',
    'channels': '/v5/channels',
    'channel_config': '/v5/channel/%(channel_key)s/config',
    'channel_sessions': '/v5/channel/%(channel_key)s/sessions',
    'channel_session_rename': '/v5/channel/%(channel_key)s/session/%(session_key)s/rename',
    'reports': '/v5/reports',
    'report': '/v5/report/%(report_key)s',
    'report_status': '/v5/report/%(report_key)s/status',
    'version': '/version',
    'webhooks': '/v5/webhooks',
    'webhook': '/v5/webhook/%(webhook_key)s'
}
