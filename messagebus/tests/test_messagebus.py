#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
  Copyright 2013 Mail Bypass, Inc.

  Licensed under the Apache License, Version 2.0 (the 'License'); you may
  not use this file except in compliance the License. You may obtain
  a copy of the License at

      http://www.apache.org/licenses/LICENSE-2.0

  Unless required by applicable law or agreed to in writing, software
  distributed under the License is distributed on an 'AS IS' BASIS, WITHOUT
  WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
  License for the specific language governing permissions and limitations
  under the License.
"""

import unittest
from httplib import HTTPSConnection
import sys
import os
import datetime
import urllib
import json

import mox
from pylint.lint import Run

path = os.path.abspath(
    os.path.join(os.path.dirname(__file__), '', '..', '..'))
if not path in sys.path:
    sys.path.insert(1, path)
del path

from messagebus import MessageBusTemplatesClient, MessageBusResponseError, MessageBusAPIClient, MessageBusStatsClient, constants
import messagebus


class MockResponse:
    def __init__(self, status, body):
        self.status = status
        self.body = body

    def read(self):
        return self.body


class MBAPIClientTests(unittest.TestCase):
    maxDiff = None

    def setUp(self):
        self.mocker = mox.Mox()
        self.api_key = 'mock_api_key'

    def _setup_mock_connection(self, request_method, request_path, request_body, response_code, response_body):
        conn_mock = self.mocker.CreateMock(HTTPSConnection)

        py_version = '.'.join(map(str, sys.version_info[:3]))
        user_agent = 'MessageBusAPI:%s-PYTHON:%s' % (
            constants.version, py_version)

        headers = {'X-MessageBus-Key': self.api_key, 'User-agent': user_agent}
        if request_method in ('POST', 'PUT'):
            headers['Content-Type'] = 'application/json; charset=utf-8'

        conn_mock.request(
            request_method, request_path, body=request_body, headers=headers)
        conn_mock.getresponse(
        ).AndReturn(MockResponse(response_code, response_body))
        self.mocker.ReplayAll()
        return conn_mock

    def _validate_results(self, expected_resp, received_resp):
        self.mocker.VerifyAll()
        self.assertEquals(expected_resp, received_resp)

    def test_version(self):
        expected_resp = json.dumps({
                                       u'APIName': u'api',
                                       u'APIVersion': u'1.1.12.0-beta-201210081020',
                                       u'status_code': 200,
                                       u'status_message': u'API Version Lookup',
                                       u'status_time': u'2010-10-22T17:42:59.556Z'}, sort_keys=True)

        mb = MessageBusAPIClient(self.api_key)
        mb.__dict__['_MessageBusBase__connection'] = self._setup_mock_connection('GET', '/api/version', '', 200,
                                                                                 expected_resp)

        received_resp = json.dumps(mb.api_version(), sort_keys=True)
        self._validate_results(expected_resp, received_resp)

        self.mocker.UnsetStubs()

    def test_mb_rest_headers(self):
        mb = MessageBusAPIClient(self.api_key)

        base_headers = mb.__base_headers__()
        self.assertEquals(len(base_headers.items()), 2)
        self.assertEquals(base_headers['X-MessageBus-Key'], self.api_key)

        post_headers = mb.__post_headers__()
        self.assertEquals(len(post_headers.items()), 1)
        self.assertEquals(
            post_headers['Content-Type'], 'application/json; charset=utf-8')

    def test_init(self):
        mb = MessageBusAPIClient(self.api_key)

        self.assertEquals(mb.api_key, self.api_key)
        self.assertTrue(mb.uri.find('api') >= 0)

    def test_unauthorized_403(self):
        mb = MessageBusAPIClient(self.api_key)
        self.assertRaises(MessageBusResponseError, mb.send_messages, [])
        self.assertRaises(MessageBusResponseError, mb.create_session, 'channel', 'session')
        self.assertRaises(MessageBusResponseError, mb.rename_session, 'channel', 'session', 'newname')
        self.assertRaises(MessageBusResponseError, mb.get_channel_config, 'channel')
        self.assertRaises(MessageBusResponseError, mb.get_channel_sessions, 'channel')

    def test_underscorify(self):
        input_camel = json.dumps({
                                     u'stats': {
                                         u'msgsAttemptedCount': 0,
                                         u'openCount': 0,
                                         u'unsubscribeCount': 0,
                                         u'complaintCount': 0,
                                         u'clickCount': 0,
                                     },
                                     u'smtp': {
                                         u'rejectCount': 0,
                                         u'bounceCount': 0,
                                         u'acceptCount': 0,
                                         u'deferralCount': 0,
                                     },
                                     u'filter': {u'rcptBadMailboxCount': 0, u'rcptChannelBlockCount': 0},
                                     u'statusTime': u'2012-09-19T22:40:45.123Z',
                                     u'statusMessage': u'stats request succeeded',
                                     u'statusCode': 200,
                                 }, sort_keys=True)

        expected_resp_dict = {
            u'stats': {
                u'msgs_attempted_count': 0,
                u'open_count': 0,
                u'unsubscribe_count': 0,
                u'complaint_count': 0,
                u'click_count': 0,
            },
            u'smtp': {
                u'reject_count': 0,
                u'bounce_count': 0,
                u'accept_count': 0,
                u'deferral_count': 0,
            },
            u'filter': {u'rcpt_bad_mailbox_count': 0, u'rcpt_channel_block_count': 0},
            u'status_time': u'2012-09-19T22:40:45.123Z',
            u'status_message': u'stats request succeeded',
            u'status_code': 200,
        }

        mb = MessageBusAPIClient("foo")

        converted_dict = mb.__camel_to_underscore__(input_camel)
        self.assertEquals(expected_resp_dict, converted_dict)

        _, convertedCamel = mb.__underscore_to_camel__(converted_dict)
        self.assertEquals(convertedCamel, input_camel)

    def test_get_stats(self):
        expected_resp = json.dumps({
                                       u'stats': {
                                           u'msgs_attempted_count': 0,
                                           u'open_count': 0,
                                           u'unsubscribe_count': 0,
                                           u'complaint_count': 0,
                                           u'click_count': 0,
                                       },
                                       u'smtp': {
                                           u'reject_count': 0,
                                           u'bounce_count': 0,
                                           u'accept_count': 0,
                                           u'deferral_count': 0,
                                       },
                                       u'filter': {u'rcpt_bad_mailbox_count': 0, u'rcpt_channel_block_count': 0},
                                       u'status_time': u'2012-09-19T22:40:45.123Z',
                                       u'status_message': u'stats request succeeded',
                                       u'status_code': 200,
                                   }, sort_keys=True)

        mb = MessageBusStatsClient(self.api_key)
        start_date = datetime.datetime(2012, 10, 10)
        end_date = datetime.datetime(2012, 10, 15)
        query_params = urllib.urlencode(
            {'endDate': end_date.isoformat(), 'startDate': start_date.isoformat()})

        ## stats/email
        path = '%s?%s' % (constants.end_points['stats'], query_params)
        mb.__dict__['_MessageBusBase__connection'] = self._setup_mock_connection('GET', path, '', 200, expected_resp)
        received_resp = json.dumps(mb.get_stats(
            start_date=start_date, end_date=end_date), sort_keys=True)
        self._validate_results(expected_resp, received_resp)
        self.mocker.UnsetStubs()

        channel = 'test_channel'
        ## stats/email/channel/<channel_uuid>
        path = '%s?%s' % (constants.end_points['stats_channel'] % {'channel_key': channel}, query_params)
        mb.__dict__['_MessageBusBase__connection'] = self._setup_mock_connection(
            'GET', path, '', 200, expected_resp)
        received_resp = json.dumps(mb.get_stats(start_date=start_date, end_date=end_date, channel='test_channel'),
                                   sort_keys=True)
        self._validate_results(expected_resp, received_resp)
        self.mocker.UnsetStubs()

        ## stats/email/channel/<channel_uuid>/session/<session_uuid>
        channel = 'test_channel'
        session = 'test_session'
        path = '%s?%s' % (
            constants.end_points['stats_channel_session'] % {'channel_key': channel, 'session_key': session},
            query_params)
        mb.__dict__['_MessageBusBase__connection'] = self._setup_mock_connection(
            'GET', path, '', 200, expected_resp)
        received_resp = json.dumps(
            mb.get_stats(start_date=start_date, end_date=end_date, channel=channel, session=session), sort_keys=True)
        self._validate_results(expected_resp, received_resp)
        self.mocker.UnsetStubs()

    def test_channels(self):
        expected_resp = json.dumps({})
        mb = MessageBusAPIClient(self.api_key)
        channel = 'test_channel'

        path = '%s' % constants.end_points['channels']
        mb.__dict__['_MessageBusBase__connection'] = self._setup_mock_connection(
            'GET', path, '', 200, expected_resp)
        received_resp = json.dumps(mb.get_channels(), sort_keys=True)
        self._validate_results(expected_resp, received_resp)
        self.mocker.UnsetStubs()

        path = '%s' % constants.end_points['channels']
        mb.__dict__['_MessageBusBase__connection'] = self._setup_mock_connection(
            'GET', path, '', 200, expected_resp)
        received_resp = json.dumps(mb.get_channels(), sort_keys=True)
        self._validate_results(expected_resp, received_resp)
        self.mocker.UnsetStubs()

        path = '%s' % constants.end_points[
            'channel_config'] % {'channel_key': channel}
        mb.__dict__['_MessageBusBase__connection'] = self._setup_mock_connection(
            'GET', path, '', 200, expected_resp)
        received_resp = json.dumps(
            mb.get_channel_config('test_channel'), sort_keys=True)
        self._validate_results(expected_resp, received_resp)
        self.mocker.UnsetStubs()

    def test_session_create(self):
        expected_resp = json.dumps({
                                       u'session_name': u'test session name',
                                       u'session_key': u'test_session_key',
                                       u'status_message': u'',
                                       u'status_time': u'2012-10-31T23:37:44.560Z',
                                       u'status_code': 202}, sort_keys=True)

        mb = MessageBusAPIClient(self.api_key)
        channel = 'test_channel'
        session_name = 'test session name'
        path = '%s' % constants.end_points[
            'channel_sessions'] % {'channel_key': channel}
        mb.__dict__['_MessageBusBase__connection'] = self._setup_mock_connection('POST', path, json.dumps(
            {"sessionName": session_name}, sort_keys=True), 200, expected_resp)
        received_resp = json.dumps(
            mb.create_session(channel, session_name), sort_keys=True)
        self._validate_results(expected_resp, received_resp)
        self.mocker.UnsetStubs()

    def test_mb_send_207(self):
        expected_resp = json.dumps({u'failure_count': 1,
                                    u'results': [{u'message_id': u'fbeeb6e0838911e289f5bc764e049d62',
                                                  u'message_status': 0,
                                                  u'to_email': u'bob@example.com'},
                                                 {u'message_id': u'fbeeddf0838911e289f5bc764e049d62',
                                                  u'message_status': 1002,
                                                  u'to_email': u'usarin'}],
                                    u'status_code': 207,
                                    u'status_message': u'One or more emails not sent. See individual error messages.',
                                    u'status_time': u'2013-03-02T22:39:03.581Z',
                                    u'success_count': 1}, sort_keys=True)

        mb = MessageBusAPIClient(self.api_key)
        mb._last_init_time = datetime.datetime.now()

        body = json.dumps({'messages': []})
        mb.__dict__['_MessageBusBase__connection'] = self._setup_mock_connection('POST', constants.end_points[
            'message_emails_send'], body, 207, expected_resp)

        received_resp = mb.send_messages([])
        self.assertEqual(
            json.dumps(received_resp, sort_keys=True), expected_resp)
        self.mocker.UnsetStubs()

    def test_mb_flush_non_2xx(self):
        expected_resp = json.dumps(
            {u'status_code': 400, u'status_message': u'A non 2xx message',
             u'status_time': u'2013-03-02T22:39:03.581Z'})
        mb = MessageBusAPIClient(self.api_key)
        mb._last_init_time = datetime.datetime.now()

        body = json.dumps({'messages': []})
        mb.__dict__['_MessageBusBase__connection'] = self._setup_mock_connection('POST', constants.end_points[
            'message_emails_send'], body, 400, expected_resp)

        # should raise exception
        self.assertRaises(MessageBusResponseError, mb.send_messages, [])
        self.mocker.UnsetStubs()

    def test_mb_simulate_sends(self):
        expected_resp_400 = json.dumps(
            {u'status_code': 400, u'status_message': u'A non 2xx message',
             u'status_time': u'2013-03-02T22:39:03.581Z'})

        expected_resp_207 = json.dumps({u'failure_count': 1,
                                        u'results': [{u'message_id': u'fbeeb6e0838911e289f5bc764e049d62',
                                                      u'message_status': 0,
                                                      u'to_email': u'bob@example.com'},
                                                     {u'message_id': u'fbeeddf0838911e289f5bc764e049d62',
                                                      u'message_status': 1002,
                                                      u'to_email': u'bob'}],
                                        u'status_code': 207,
                                        u'status_message': u'One or more emails not sent. See individual error messages.',
                                        u'status_time': u'2013-03-02T22:39:03.581Z',
                                        u'success_count': 1}, sort_keys=True)

        expected_resp_202 = json.dumps({u'failure_count': 0,
                                        u'results': [{u'message_id': u'fbeeb6e0838911e289f5bc764e049d62',
                                                      u'message_status': 0,
                                                      u'to_email': u'bob@example.com'},
                                                     {u'message_id': u'fbeeddf0838911e289f5bc764e049d62',
                                                      u'message_status': 0,
                                                      u'to_email': u'bob@example.com'}],
                                        u'status_code': 202,
                                        u'status_message': u'.',
                                        u'status_time': u'2013-03-02T22:39:03.581Z',
                                        u'success_count': 2}, sort_keys=True)

        mb = MessageBusAPIClient(self.api_key)

        body = json.dumps({'messages': []})
        mb.__dict__['_MessageBusBase__connection'] = self._setup_mock_connection('POST', constants.end_points[
            'message_emails_send'], body, 400, expected_resp_400)
        self.assertRaises(MessageBusResponseError, mb.send_messages, [])
        self.mocker.UnsetStubs()

        body = json.dumps({'messages': []})
        mb.__dict__['_MessageBusBase__connection'] = self._setup_mock_connection('POST', constants.end_points[
            'message_emails_send'], body, 207, expected_resp_207)

        # should not raise exception
        received_resp = mb.send_messages([])

        self.assertEqual(json.dumps(received_resp, sort_keys=True), expected_resp_207)
        self.mocker.UnsetStubs()

        body = json.dumps({'messages': []})
        mb.__dict__['_MessageBusBase__connection'] = self._setup_mock_connection('POST', constants.end_points[
            'message_emails_send'], body, 202, expected_resp_202)

        # should not raise exception
        received_resp = mb.send_messages([])

        self.assertEqual(
            json.dumps(received_resp, sort_keys=True), expected_resp_202)
        self.mocker.UnsetStubs()

    def test_send_above_buffer_limit(self):
        mb = MessageBusTemplatesClient(self.api_key)
        self.assertRaises(ValueError, mb.send_messages, 'fake_key', ['msg'] * 101)


class MBTemplatesClientTests(unittest.TestCase):
    maxDiff = None

    def setUp(self):
        self.mocker = mox.Mox()
        self.api_key = 'mock_api_key'

    def assertRaisesWithMessage(self, msg, func, *args, **kwargs):
        try:
            func(*args, **kwargs)
            self.assertFalse(False)
        except Exception as inst:
            self.assertEqual(inst.message, msg)

    def __setup_mock_connection__(self, request_method, request_path, request_body, response_code, response_body):
        conn_mock = self.mocker.CreateMock(HTTPSConnection)

        py_version = '.'.join(map(str, sys.version_info[:3]))
        user_agent = 'MessageBusAPI:%s-PYTHON:%s' % (
            constants.version, py_version)

        headers = {'X-MessageBus-Key': self.api_key, 'User-agent': user_agent}
        if request_method in ('POST', 'PUT'):
            headers['Content-Type'] = 'application/json; charset=utf-8'

        conn_mock.request(
            request_method, request_path, body=request_body, headers=headers)
        conn_mock.getresponse(
        ).AndReturn(MockResponse(response_code, response_body))
        self.mocker.ReplayAll()
        return conn_mock

    def _validate_results(self, expected_resp, received_resp):
        self.mocker.VerifyAll()
        self.assertEquals(expected_resp, received_resp)

    def test_version_mock(self):
        expected_resp = json.dumps({u'status_code': 200,
                                    u'status_message': u'API Version Lookup',
                                    u'status_time': u'2010-10-22T17:42:59.556Z'}, sort_keys=True)

        mb = MessageBusTemplatesClient(self.api_key)
        mb.__dict__['_MessageBusBase__connection'] = self.__setup_mock_connection__(
            'GET', '/api/v4/templates/version', '', 200, expected_resp)
        received_resp = json.dumps(mb.api_version(), sort_keys=True)
        self._validate_results(expected_resp, received_resp)
        self.mocker.UnsetStubs()

    def test_version(self):
        mb = MessageBusTemplatesClient(self.api_key)
        result = mb.api_version()
        # Templates version is of the form 1.13.x
        self.assertEquals(len(result['version'].split('.')), 3)

    def test_create_template(self):
        template = {
            u'to_email': u'{{rcpt_email}}',
            u'from_name': u'{{sender_name}}',
            u'subject': u'blah blah {{unique_subject_value}}',
            u'from_email': u'{{sender_email}}',
            u'return_path': u'{{return_path}}',
            u'to_name': u'{{rcpt_name}}',
            u'custom_headers': {u'x-header': u'{{x_value}}'},
            u'session_key': u'DEFAULT',
            u'options': {u'track_clicks': True},
            u'plaintext_body': u'Lacus sociis congue',
            u'html_body': u'<HTML>{{some_key}}</HTML><br>'
        }

        template_out = {
            u'toEmail': u'{{rcpt_email}}',
            u'fromName': u'{{sender_name}}',
            u'subject': u'blah blah {{unique_subject_value}}',
            u'fromEmail': u'{{sender_email}}',
            u'returnPath': u'{{return_path}}',
            u'toName': u'{{rcpt_name}}',
            u'customHeaders': {u'x-header': u'{{x_value}}'},
            u'sessionKey': u'DEFAULT',
            u'options': {u'trackClicks': True},
            u'plaintextBody': u'Lacus sociis congue',
            u'htmlBody': u'<HTML>{{some_key}}</HTML><br>'
        }

        mb = MessageBusTemplatesClient(self.api_key)

        expected_resp = json.dumps({"template_key": "0eef707e-f25f-45bd-ae52-35090b69f13b",
                                    "status_code": 201,
                                    "status_message": "Template saved",
                                    "status_time": "2013-02-21T21:27:35.338Z"
                                   }, sort_keys=True)

        expect_resp_out = json.dumps({"templateKey": "0eef707e-f25f-45bd-ae52-35090b69f13b",
                                      "statusCode": 201,
                                      "statusMessage": "Template saved",
                                      "statusTime": "2013-02-21T21:27:35.338Z"
                                     }, sort_keys=True)

        mb.__dict__['_MessageBusBase__connection'] = self.__setup_mock_connection__('POST', '/api/v4/templates/',
                                                                                    json.dumps(template_out,
                                                                                               sort_keys=True), 201,
                                                                                    expect_resp_out)

        received_resp = json.dumps(mb.create_template(template), sort_keys=True)

        self._validate_results(expected_resp, received_resp)
        self.mocker.UnsetStubs()

    def test_get_template(self):
        template = {
            u'to_email': u'{{rcpt_email}}',
            u'from_name': u'{{sender_name}}',
            u'subject': u'blah blah {{unique_subject_value}}',
            u'from_email': u'{{sender_email}}',
            u'return_path': u'{{return_path}}',
            u'to_name': u'{{rcpt_name}}',
            u'custom_headers': {u'x-header': u'{{x_value}}'},
            u'session_key': u'DEFAULT',
            u'options': {u'track_clicks': True},
            u'plaintext_body': u'Lacus sociis congue',
            u'html_body': u'<HTML>{{some_key}}</HTML><br>',
            u'template_key': u'foo_key'
        }

        mb = MessageBusTemplatesClient(self.api_key)
        expected_resp = json.dumps(
            dict(template=template, status_code=200, status_message="template", status_time="2013-02-21T21:27:35.338Z"),
            sort_keys=True)

        mb.__dict__['_MessageBusBase__connection'] = self.__setup_mock_connection__('GET', '/api/v4/template/foo_key',
                                                                                    '', 200, expected_resp)

        received_resp = json.dumps(mb.get_template('foo_key'), sort_keys=True)
        self._validate_results(expected_resp, received_resp)

        self.mocker.UnsetStubs()

    def test_auth_exceptions(self):
        mb = MessageBusTemplatesClient(self.api_key)
        self.assertRaises(MessageBusResponseError, mb.get_template, 'fake_key')
        self.assertRaises(MessageBusResponseError, mb.get_templates)
        self.assertRaises(MessageBusResponseError, mb.create_template, {})
        self.assertRaises(MessageBusResponseError, mb.send_messages, 'fake_key', [])

    def test_send_mock_multiple(self):
        messages = [
            {
                "rcpt_email": "bob@example.com",
                "sender_email": "bob@messagebus.com",
                "x_value": "42",
                "foo_key": "some key value",
                "unique_subject_value": "test subject"
            },
            {
                "rcpt_email": "bob@example.com",
                "sender_email": "bob@messagebus.com",
                "x_value": "43",
                "foo_key": "some key value #2",
                "unique_subject_value": "test subject"
            }
        ]

        mb = MessageBusTemplatesClient(self.api_key)
        expected_resp_out = json.dumps({
            "failureCount": 0,
            "results": [
                {
                    "toEmail": "bob@gmail.com",
                    "messageId": "8a37a4a07c7011e29a5890b8d09e776a",
                    "messageStatus": 0
                }
            ],
            "statusCode": 202,
            "statusMessage": "",
            "statusTime": "2013-02-21T21:49:17.284Z",
            "successCount": 1
        })

        expected_resp = json.dumps({
                                       "failure_count": 0,
                                       "results": [
                                           {
                                               "to_email": "bob@gmail.com",
                                               "message_id": "8a37a4a07c7011e29a5890b8d09e776a",
                                               "message_status": 0
                                           }
                                       ],
                                       "status_code": 202,
                                       "status_message": "",
                                       "status_time": "2013-02-21T21:49:17.284Z",
                                       "success_count": 1
                                   }, sort_keys=True)

        mb.__dict__['_MessageBusBase__connection'] = self.__setup_mock_connection__('POST',
                                                                                    '/api/v4/templates/email/send',
                                                                                    json.dumps(
                                                                                        dict(templateKey='template_key',
                                                                                             messages=messages),
                                                                                        sort_keys=True), 202,
                                                                                    expected_resp_out)
        received_resp = json.dumps(mb.send_messages(template='template_key', messages=messages), sort_keys=True)
        self._validate_results(expected_resp, received_resp)

        self.mocker.UnsetStubs()

    def test_send_mock_single(self):
        message = {
            "rcpt_email": "bob@example.com",
            "sender_email": "bob@messagebus.com",
            "x_value": "42",
            "foo_key": "some key value",
            "unique_subject_value": "test subject"
        }
        mb = MessageBusTemplatesClient(self.api_key)
        expected_resp_out = json.dumps({
            "failureCount": 0,
            "results": [
                {
                    "toEmail": "bob@example.com",
                    "messageId": "8a37a4a07c7011e29a5890b8d09e776a",
                    "messageStatus": 0
                }
            ],
            "statusCode": 202,
            "statusMessage": "",
            "statusTime": "2013-02-21T21:49:17.284Z",
            "successCount": 1
        })

        expected_resp = json.dumps({"failure_count": 0,
                                    "results": [
                                        {
                                            "to_email": "bob@example.com",
                                            "message_id": "8a37a4a07c7011e29a5890b8d09e776a",
                                            "message_status": 0
                                        }
                                    ],
                                    "status_code": 202,
                                    "status_message": "",
                                    "status_time": "2013-02-21T21:49:17.284Z",
                                    "success_count": 1
                                   }, sort_keys=True)

        mb.__dict__['_MessageBusBase__connection'] = self.__setup_mock_connection__('POST',
                                                                                    '/api/v4/templates/email/send',
                                                                                    json.dumps(
                                                                                        dict(templateKey='template_key',
                                                                                             messages=[message]),
                                                                                        sort_keys=True), 202,
                                                                                    expected_resp_out)
        received_resp = json.dumps(mb.send_messages(template='template_key', messages=[message]), sort_keys=True)
        self._validate_results(expected_resp, received_resp)

        self.mocker.UnsetStubs()

    def test_non_2xx(self):
        message = {
            "rcpt_email": "bob@example.com",
            "sender_email": "bob@messagebus.com",
            "x_value": "42",
            "foo_key": "some key value",
            "unique_subject_value": "test subject"
        }
        mb = MessageBusTemplatesClient(self.api_key)
        expected_resp_out = json.dumps(
            {u'statusCode': 400, u'statusMessage': u'A non 2xx message - test',
             u'statusTime': u'2013-03-02T22:39:03.581Z'})

        mb.__dict__['_MessageBusBase__connection'] = self.__setup_mock_connection__('POST',
                                                                                    '/api/v4/templates/email/send',
                                                                                    json.dumps(
                                                                                        dict(templateKey='template_key',
                                                                                             messages=[message]),
                                                                                        sort_keys=True), 202,
                                                                                    expected_resp_out)

        self.assertRaisesWithMessage('Error: status_code:400 , status_message:A non 2xx message - test',
                                     mb.send_messages, 'template_key', [message])
        self.mocker.UnsetStubs()

    def test_send_above_buffer_limit(self):
        mb = MessageBusTemplatesClient(self.api_key)
        self.assertRaises(ValueError, mb.send_messages, 'fake_key', ['msg'] * 100)

    def test_pylint(self):
        Run(['-E', messagebus.__file__.replace('.pyc', '.py')], exit=False)


if __name__ == '__main__':
    unittest.main()
