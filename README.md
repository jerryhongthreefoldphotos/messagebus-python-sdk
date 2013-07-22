![MB icon](https://www.messagebus.com/img/logo.png)

###Message Bus Python sdk

Message Bus is a cloud-based platform for easily sending email at scale and with complete insight into your messaging traffic and how recipients are responding to it. All platform functions are available via [REST API](http://www.messagebus.com/documentation) as well as the language-specific documentation, sample code, libraries, and/or compiled binaries contained in this SDK.

Samples include how to:

* Create sessions
* Send messages
* Use templates
* Check email stats

If you have questions not answered by the samples or the online documentation, please contact [support](mailto:support@messagebus.com).


####Installing the module

    easy_install messagebus

####Sending emails

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
        results = api_client.send_messages([message_jane])
    except MessageBusResponseError, error:
        print error.message
    else:
        print results

####Checking email statistics

    from messagebus import MessageBusStatsClient, MessageBusResponseError

    api_key = '7215ee9c7d9dc229d2921a40e899ec5f'
    uri = 'api-v4.messagebus.com'

    try:
        stats_client = MessageBusStatsClient(api_key, uri=uri)
        results = stats_client.get_stats()
    except MessageBusResponseError, error:
        print error.message
    else:
        print results

#### Checking email feedback data

    from messagebus import MessageBusFeedbackClient, MessageBusResponseError

    api_key = '7215ee9c7d9dc229d2921a40e899ec5f'
    uri = 'api-v4.messagebus.com'

    channel = 'c1ad3825299f4fa30ff0e4f713bc2726'
    session = '4fcfa8b403ba5986200a2def578b442f'
    scope = 'unsubs|complaints'

    try:
        feedback_client = MessageBusFeedbackClient(api_key, uri=uri)
        results = feedback_client.get_feedback(channel=channel, session=session, scope=scope)
    except MessageBusResponseError, error:
        print error.message
    else:
        print results


#### License 


    Copyright (c) 2013 Mail Bypass, Inc.

    Licensed under the Apache License, Version 2.0 (the "License"); you may not use this file except in compliance
    with the License. You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

    Unless required by applicable law or agreed to in writing, software distributed under the License is
    distributed on an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
    See the License for the specific language governing permissions and limitations under the License
