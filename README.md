![MB icon](https://www.messagebus.com/img/logo.png)

###Message Bus Python SDK

Message Bus is a cloud-based platform for easily sending email at scale and with complete insight into your messaging traffic and how recipients are responding to it. All platform functions are available via [REST API](http://www.messagebus.com/documentation) as well as the language-specific documentation, sample code, libraries, and/or compiled binaries contained in this SDK.

Samples include how to:

* Create sessions
* Send messages
* Use templates
* Check email stats
* Configure Webhooks

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
            'return_path': 'bounces@bounces.example.com',
            'plaintext_body': 'This message to Jane Smith is a test sent by the Python Message Bus client library.',
            'html_body': '<html><body>This message to Jane Smith is a test sent by the Python Message Bus sdk.</body></html>',
            'session_key': 'DEFAULT',
        }
        results = api_client.send_messages([message_jane])
    except MessageBusResponseError, error:
        print error.message
    else:
        print results

#### License 


    Copyright (c) 2014 Message Bus

    Licensed under the Apache License, Version 2.0 (the "License"); you may not use this file except in compliance
    with the License. You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

    Unless required by applicable law or agreed to in writing, software distributed under the License is
    distributed on an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
    See the License for the specific language governing permissions and limitations under the License
