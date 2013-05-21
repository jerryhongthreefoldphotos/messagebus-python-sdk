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

version = '4.1.0'

max_messages = 100
max_template_messages = 25
timeout = 30
debug_level = 0
reconnect_interval = 60

uri = 'api-v4.messagebus.com'
template_uri = 'templates-v4-jy01-prod.messagebus.com'

user_agent = 'MessageBusAPI:%s-PYTHON:%s' % (version, '.'.join(map(str, sys.version_info[:3])))

end_points = {
    'message_emails_send': '/api/v4/message/email/send',
    'template_emails_send': '/api/v4/templates/email/send',
    'template': '/api/v4/template/%(template_key)s',
    'templates': '/api/v4/templates/',
    'templates_version': '/api/v4/templates/version',
    'channels': '/api/v4/channels',
    'channel_config': '/api/v4/channel/%(channel_key)s/config',
    'channel_sessions': '/api/v4/channel/%(channel_key)s/sessions',
    'channel_session_rename': '/api/v4/channel/%(channel_key)s/session/%(session_key)s/rename',
    'version': '/api/version',
    'feedback': '/api/v4/feedback',
    'feedback_channel': '/api/v4/feedback/channel/%(channel_key)s',
    'feedback_channel_session': '/api/v4/feedback/channel/%(channel_key)s/session/%(session_key)s',
    'stats': '/api/v4/stats/email',
    'stats_channel': '/api/v4/stats/email/channel/%(channel_key)s',
    'stats_channel_session': '/api/v4/stats/email/channel/%(channel_key)s/session/%(session_key)s'
}