#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Message Bus Python SDK
"""

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

import httplib
import urllib
import re
import datetime
import types
import json
import shutil

import constants


class MessageBusBase(object):

    def __init__(
            self,
            api_key,
            uri=constants.uri,
            timeout=constants.timeout
    ):
        self.api_key = api_key
        self.uri = uri
        self.timeout = timeout

        self.__connection = None
        self.__init_connect__()

    def __init_connect__(self):
        self.__connection = httplib.HTTPSConnection(
            self.uri, timeout=self.timeout)
        self.__connection.connect()
        self.__last_init_time = datetime.datetime.now()

    def __base_headers__(self):
        return {'User-agent': constants.user_agent, 'X-MessageBus-Key': self.api_key}

    def __post_headers__(self):
        return {'Content-Type': 'application/json; charset=utf-8'}

    def __call_api__(self, path, method='GET', body='', params=None, ignore_keys=None, fp=None):
        if not params:
            params = dict()
        headers = self.__base_headers__()

        if path[:1] != '/': path = '/%s' % path

        if method in ('POST', 'PUT'):
            headers = dict(headers.items() + self.__post_headers__().items())
            if type(body) in types.StringTypes:
                _, body = MessageBusBase.__underscore_to_camel__(
                    json.loads(body), ignore_keys=ignore_keys)
            else:
                _, body = MessageBusBase.__underscore_to_camel__(
                    body, ignore_keys=ignore_keys)
        else:
            path = '%s?%s' % (
                path, urllib.urlencode(params)) if params else path

        if not self.__connection or not self.__last_init_time or \
            (datetime.datetime.now() - self.__last_init_time).seconds > constants.reconnect_interval:
            self.__init_connect__()

        self.__connection.request(method, path, body=body, headers=headers)
        if fp:
            return shutil.copyfileobj(self.__connection.getresponse(), fp)
        else:
            return self.__check_response__(self.__connection.getresponse())

    def __check_response__(self, response):
        raw_body = response.read()
        parsed_body = dict()
        try:
            parsed_body = MessageBusBase.__camel_to_underscore__(raw_body)
        except:
            pass
        finally:
            status_code = parsed_body.get('status_code', response.status)
            status_message = parsed_body.get('status_message', raw_body)

        if status_code in (httplib.OK, httplib.CREATED, httplib.ACCEPTED, httplib.MULTI_STATUS):
            return parsed_body
        else:
            raise MessageBusResponseError(
                'Error: status_code:%s , status_message:%s' % (status_code, status_message))

    @staticmethod
    def __camel_to_underscore__(content, ignore_keys=None):
        if not ignore_keys:
            ignore_keys = []

        data = json.loads(content)

        def camelToUnderscore(match):
            return match.group()[0] + "_" + match.group()[1].lower()

        def underscorize(data):
            if isinstance(data, types.DictionaryType):
                new_dict = {}
                for key, value in data.items():
                    if key not in ignore_keys:
                        new_key = re.sub(r"[a-z][A-Z]", camelToUnderscore, key)
                        new_dict[new_key] = underscorize(value)
                    else:
                        new_dict[key] = value
                return new_dict
            if type(data) in [types.ListType, types.TupleType]:
                for i in range(len(data)):
                    data[i] = underscorize(data[i])
                return data
            return data

        return underscorize(data)

    @staticmethod
    def __underscore_to_camel__(data, ignore_keys=None):
        if not ignore_keys:
            ignore_keys = []

        def underscoreToCamel(match):
            return match.group()[0] + match.group()[2].upper()

        def camelize(data):
            if isinstance(data, types.DictionaryType):
                new_dict = {}
                for key, value in data.items():
                    if key not in ignore_keys:
                        new_key = re.sub(
                            r"[a-z]_[a-z]", underscoreToCamel, key)
                        new_dict[new_key] = camelize(value)
                    else:
                        new_dict[key] = value
                return new_dict
            if type(data) in [types.ListType, types.TupleType]:
                for i in range(len(data)):
                    data[i] = camelize(data[i])
                return data
            return data

        camelized_data = camelize(data)
        return camelized_data, json.dumps(camelized_data, sort_keys=True)


class MessageBusTemplatesClient(MessageBusBase):

    """
     MessageBusTemplatesClient sends email using server side templates.
    """

    def __init__(self, api_key, uri=constants.template_uri, timeout=constants.timeout):
        super(MessageBusTemplatesClient, self).__init__(api_key, uri, timeout)

    def api_version(self):
        """Call template api version route and return a dict with the api version."""
        return self.__call_api__(constants.end_points['templates_version'])

    def create_template(self, template):
        """
        Store an email template and return a dict with the template_key.

        Parameters
        ----------
        template : dict
            Template to save.

        """
        return self.__call_api__(constants.end_points['templates'], body=template, method='POST')

    def get_template(self, template):
        """
        Fetch a given template based on template.

        Parameters
        ----------
        template : str
            Template key.
        """
        return self.__call_api__(constants.end_points['template'] % dict(template_key=template))

    def delete_template(self, template_key):
        """
        Delete a given template based on templateKey.

        Parameters
        ----------
        template : str
            Template key.
        """
        return self.__call_api__(method='DELETE',
                                 path=constants.end_points['template'] % dict(template_key=template_key))

    def update_template(self, template_key, template):
        """
        Delete a given template based on templateKey.

        Parameters
        ----------
        template : str
            Template key.
        """
        return self.__call_api__(method='PUT',
                                 path=constants.end_points['template'] % dict(template_key=template_key), body=template)

    def get_templates(self):
        """
        Fetch the list of templates associated with the account.
        """
        return self.__call_api__(constants.end_points['templates'])

    def send_messages(self, template, messages):
        """
        Send template formatted emails.

        Parameters
        ----------
        template : str
            Template key.

        messages : list
            List containing dict values that represent the message.
        """
        if not isinstance(messages, (types.TupleType, types.ListType)):
            raise ValueError('Messages should be a list or tuple type')

        if len(messages) > constants.max_template_messages:
            raise ValueError(
                'Send %s messages, maximum allowed per batch %s', len(
                    messages),
                constants.max_template_messages)

        return self.__call_api__(
            constants.end_points['template_emails_send'], method='POST',
            body=dict(template_key=template, messages=messages), ignore_keys=['messages'])


class MessageBusAPIClient(MessageBusBase):

    """
    MessageBusAPIClient sends email and provides methods for channel and session based segmentation.
    """

    def __init__(self, api_key, uri=constants.uri, timeout=constants.timeout):
        super(MessageBusAPIClient, self).__init__(
            api_key, uri=uri, timeout=timeout)

    def api_version(self):
        """Call api version route and return a dict with the api version."""
        return self.__call_api__(constants.end_points['version'], 'GET')

    def send_messages(self, messages):
        """
        Send emails.

        Parameters
        ----------
        messages : list
            List containing dict values that represent the message.
        """
        if not isinstance(messages, (types.TupleType, types.ListType)):
            raise ValueError('Messages should be a list or tuple type')

        if len(messages) > constants.max_messages:
            raise ValueError(
                'Send %s messages, maximum allowed per batch %s', len(messages), constants.max_messages)

        return self.__call_api__(
            constants.end_points['message_emails_send'], method='POST',
            body=dict(messages=messages))

    def get_channels(self):
        """
        Retrieves all the channels associated with the account.
        """
        return self.__call_api__(constants.end_points['channels'])

    def get_channel_config(self, channel):
        """
        Configuration settings for the channel.

        Parameters
        ----------
        channel : str
            Channel key.
        """
        return self.__call_api__(constants.end_points['channel_config'] % dict(channel_key=channel))

    def get_channel_sessions(self, channel):
        """
        Retrieves sessions associated with the channel.

        Parameters
        ----------
        channel : str
            Channel key.
        """
        return self.__call_api__(constants.end_points['channel_sessions'] % dict(channel_key=channel))

    def create_session(self, channel, session_name):
        """
        Creates a new session within the channel.

        Parameters
        ----------
        channel : str
            Channel key.
        session_name : str
            New session name to create.
        """
        return self.__call_api__(
            constants.end_points['channel_sessions'] % dict(channel_key=channel), method='POST',
            body=dict(session_name=session_name))

    def rename_session(self, channel, session, new_session_name):
        """
        Rename a session.

        Parameters
        ----------
        channel : str
            Channel key.
        session : str
            Key of the session who's name needs to be modified.
        new_session_name : str
            New session name.
        """
        return self.__call_api__(
            constants.end_points['channel_session_rename'] % dict(
                channel_key=channel, session_key=session),
            method='PUT',
            body=dict(session_name=new_session_name))


class MessageBusReportsClient(MessageBusBase):

    """
    MessageBusReportsClient provides methods to feedback data.
    """

    def __init__(self, api_key, uri=constants.uri, timeout=constants.timeout):
        super(MessageBusReportsClient, self).__init__(
            api_key, uri=uri, timeout=timeout)

    def create_report(self, report_params):
        """
        Parameters
        ----------
        report_params : dict
            Report creation parameters.

        """
        return self.__call_api__(path=constants.end_points['reports'], method='POST', body=report_params)

    def get_report_status(self, report_key):
        """
        Parameters
        ----------
        report_key : str
            Report Key generated by create report.\
        """
        return self.__call_api__(path=constants.end_points['report_status'] % dict(report_key=report_key))

    def get_report(self, report_key, fp):
        """
        Parameters
        ----------
        report_key : str
            Report Key generated by create report.
        fp : file
            Output file object
        """
        return self.__call_api__(path=constants.end_points['report'] % dict(report_key=report_key), fp=fp)


class MessageBusWebhooksClient(MessageBusBase):

    """
    MessageBusWebhooksClient provides methods to manage webhooks data.
    """

    def __init__(self, api_key, uri=constants.uri, timeout=constants.timeout):
        super(MessageBusWebhooksClient, self).__init__(
            api_key, uri=uri, timeout=timeout)

    def create_webhook(self, webhook_params):
        """
        Parameters
        ----------
        webhook_params : dict
            Webhook creation parameters.

        """
        return self.__call_api__(path=constants.end_points['webhooks'], method='POST', body=webhook_params)

    def update_webhook(self, webhook_key, webhook_params):
        """
        Parameters
        ----------
        webhook_key : str
            Webhook Key of the webhook to update.
        webhook_params : dict
            Webhook creation parameters.

        """
        return self.__call_api__(path=constants.end_points['webhook'] % dict(webhook_key=webhook_key), method='PUT', body=webhook_params)

    def get_webhook(self, webhook_key):
        """
        Parameters
        ----------
        webhook_key : str
            Webhook Key generated by create webhook.
        """
        return self.__call_api__(path=constants.end_points['webhook'] % dict(webhook_key=webhook_key))

    def get_webhooks(self):
        """
        Parameters
        ----------
            Get all the webhooks associated with the account.
        """
        return self.__call_api__(path=constants.end_points['webhooks'])

    def delete_webhook(self, webhook_key):
        """
        Parameters
        ----------
        webhook_key : str
            Webhook Key of the webhook to delete.
        """
        return self.__call_api__(path=constants.end_points['webhook'] % dict(webhook_key=webhook_key), method='DELETE')


class MessageBusResponseError(StandardError):

    """
    Message Bus Client error, raised when the service responds with a non 200 level response.
    """

    def __init__(self, reason, *args):
        StandardError.__init__(self, reason, *args)
        self.reason = reason

    def __repr__(self):
        return 'MessageBusResponseError: %s' % self.reason

    def __str__(self):
        return 'MessageBusResponseError: %s' % self.reason
