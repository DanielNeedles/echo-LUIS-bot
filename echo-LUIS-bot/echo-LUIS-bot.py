'''
echoLUISbot: Peforms synchronous queries against a user specified http://LUIS.ai service

BASIS:
  Microsoft Bot Framework API: 
    https://github.com/Microsoft/botbuilder-python
  Microsoft Language Understanding Intelligent Service API:
    https://github.com/Microsoft/Cognitive-LUIS-Python
  Cookie Cutter (For Python Package)
    https://www.pydanny.com/cookie-project-templates-made-easy.html

EXAMPLE LUIS APP CREATED:
  https://westus.api.cognitive.microsoft.com/luis/v2.0/apps/e992ae07-2eea-4a9e-9ed4-5916e43dbbbd?subscription-key=f5d42cc64c8e4e3085cc44b991a1d1a5&verbose=true&timezoneOffset=0&q=start my run
  EXPRESSIONS TO TRY:
    Please stop the run
    Show me the status of my swim
    Start a run
    Stop my walk now
    Please stop my run now now now

---
Copyright (c) Microsoft Corporation. All rights reserved.
Licensed under the MIT License.

Microsoft Cognitive Services (formerly Project Oxford): https://www.microsoft.com/cognitive-services

Microsoft Cognitive Services (formerly Project Oxford) GitHub:
https://github.com/Microsoft/ProjectOxford-ClientSDK

Copyright (c) Microsoft Corporation
All rights reserved.

MIT License:
Permission is hereby granted, free of charge, to any person obtaining
a copy of this software and associated documentation files (the
"Software"), to deal in the Software without restriction, including
without limitation the rights to use, copy, modify, merge, publish,
distribute, sublicense, and/or sell copies of the Software, and to
permit persons to whom the Software is furnished to do so, subject to
the following conditions:

The above copyright notice and this permission notice shall be
included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED ""AS IS"", WITHOUT WARRANTY OF ANY KIND,
EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND
NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE
LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION
OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION
WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE
'''

## PACKAGE IMPORTS
import http.server  ## HTTP SERVER
import json
import asyncio
import urllib3
from botbuilder.schema import (Activity, ActivityTypes, ChannelAccount)  ## MS BOT PACKAGES
from botframework.connector import ConnectorClient                       ## MS BOT PACKAGES
from botframework.connector.auth import (MicrosoftAppCredentials,        ## MS BOT PACKAGES
                          JwtTokenValidation, SimpleCredentialProvider)  ## MS BOT PACKAGES
from luis_sdk import LUISClient  ## LUIS API

## GLOBAL VARIABLES
APPID = ''
APPPASSWORD = ''
HOST='localhost'
PORT=9000

## PRIMARY CLASS
class BotRequestHandler(http.server.BaseHTTPRequestHandler):
    STATE = 0                                           ## Cheap state tracking
    LUISAPPID = 'e992ae07-2eea-4a9e-9ed4-5916e43dbbbd'  ## Default https://www.luis.ai/applications:
    LUISAPPKEY = 'f5d42cc64c8e4e3085cc44b991a1d1a5'     ##     Excercise.   

    @staticmethod
    def __create_reply_activity(request_activity, text):
        return Activity(
            type=ActivityTypes.message,
            channel_id=request_activity.channel_id,
            conversation=request_activity.conversation,
            recipient=request_activity.from_property,
            from_property=request_activity.recipient,
            text=text,
            service_url=request_activity.service_url)

    def __handle_conversation_update_activity(self, activity):
        self.send_response(202)
        self.end_headers()
        if activity.members_added[0].id != activity.recipient.id:
            credentials = MicrosoftAppCredentials(APPID, APPPASSWORD)
            reply = BotRequestHandler.__create_reply_activity(activity, 'Hello and welcome to the echoLUIS bot! Please input your app ID: (default: %s)' % self.LUISAPPID)
            connector = ConnectorClient(credentials, base_url=reply.service_url)
            connector.conversations.send_to_conversation(reply.conversation.id, reply)

    def __handle_LUIS_response(self,res):
        '''
        A function that processes the luis_response object and prints info from it.
        :param res: A LUISResponse object containing the response data.
        :return: text representation of LUIS app's response

        ---------------------------------------------
        LUIS Response:
        Query: start a run
        Top Scoring Intent: Fitness.Activity
        Entities:
        "start":
        Type: Fitness.Activity, Score: 0.840186954
        "run":
        Type: Fitness.ActivityType, Score: 0.956281543
        DATA: start a run
        '''

        message_parts = [
        '---------------------------------------------',
        "LUIS Response:\r\n",
        "  Query: %s\r\n" % res.get_query(),
        "  Top Scoring Intent: %s\r\n" % res.get_top_intent().get_name(),
        ]
        if res.get_dialog() is not None:
            if res.get_dialog().get_prompt() is None:
                message_parts.append("  Dialog Prompt: None")
            else:
                message_parts.append("  Dialog Prompt: %s" % res.get_dialog().get_prompt())
            if res.get_dialog().get_parameter_name() is None:
                message_parts.append("  Dialog Parameter: None")
            else:
                message_parts.append("  Dialog Parameter: %s" % res.get_dialog().get_parameter_name())
            message_parts.append("  Dialog Status: %s" % res.get_dialog().get_status())
        message_parts.append("  Entities:\r\n")
        for entity in res.get_entities():
            message_parts.append("    '%s': (Type: %s, Score: %s)\r\n" % (entity.get_name(),entity.get_type(), entity.get_score()))
        message = "\r\n".join(message_parts)
        return message

    def __handle_message_activity(self, activity):
        """
        Handle the messages.  STATE used to collect APPID and APPKEY up front.  All other messsages sent to
        LUIS for parsing.  APPID and APPKEY specify the LUIS service called via REST. For example:
          https://westus.api.cognitive.microsoft.com/luis/v2.0/apps/((APPID))?subscription-key=((APPKEY))
                &verbose=true&timezoneOffset=0&q=((TEXT-FOR-LUIS-TO-PARSE
        """
        BotRequestHandler.STATE+=1   ## POORMAN'S STATE TRACKING
        self.send_response(200)
        self.end_headers()
        credentials = MicrosoftAppCredentials(APPID, APPPASSWORD)
        connector = ConnectorClient(credentials, base_url=activity.service_url)
        LUIStext = ''

        ## FIRST, GET APPID
        if self.STATE==1:
            if activity.text:
                BotRequestHandler.LUISAPPID=activity.text
            reply = BotRequestHandler.__create_reply_activity(activity, "You entered application ID: %s\nNow, please input your subscription key (default: %s):" % (activity.text,self.LUISAPPKEY))

        ## SECOND, GET APPKEY
        elif self.STATE==2:
            if activity.text:
                BotRequestHandler.LUISAPPKEY=activity.text
            reply = BotRequestHandler.__create_reply_activity(activity, "Great! You entered application key: %s\nNow, enter some text for the LUIS model to render:" % activity.text)

        ## THIRD AND ONWARDS: SEND TEXT TO LUIS AND REPORT LUIS RESPONSE TO THE USER
        else:
            try:
                CLIENT = LUISClient(self.LUISAPPID, self.LUISAPPKEY, True)
                res = CLIENT.predict(activity.text)
                while res.get_dialog() is not None and not res.get_dialog().is_finished():
                    TEXT = input('%s\n'%res.get_dialog().get_prompt())
                    res = CLIENT.reply(TEXT, res)
                LUIStext=self.__handle_LUIS_response(res)
                reply = BotRequestHandler.__create_reply_activity(activity, 'LUIS says: %s' % LUIStext)
            except Exception as exc:
                LUIStext=exc
                print("Error: %s" % exc)
                reply = BotRequestHandler.__create_reply_activity(activity, 'About %s, LUIS complains: %s' % (activity.text,LUIStext))

        connector.conversations.send_to_conversation(reply.conversation.id, reply)

    def __handle_authentication(self, activity):
        credential_provider = SimpleCredentialProvider(APPID, APPPASSWORD)
        loop = asyncio.new_event_loop()
        try:
            loop.run_until_complete(JwtTokenValidation.assert_valid_activity(
                activity, self.headers.get("Authorization"), credential_provider))
            return True
        except Exception as ex:
            self.send_response(401, ex)
            self.end_headers()
            return False
        finally:
            loop.close()

    def __unhandled_activity(self):
        self.send_response(404)
        self.end_headers()

    def do_GET(self):
        parsed_path = urllib3.util.parse_url(self.path)
        message_parts = [
        '################  Welcome to LUIS echo BOT!  ################',
        'This bot echos back what LUIS.ai parses via one of its ReSTful APIs.',
        'Please use the Bot Framework Emulator or other POST method',
        'to test the functionality on:',
        '       http://((HOST)):((PORT))/api/messages',
        '##############################################################',
        '',
        'CLIENT VALUES:',
        '##############################################################',
        'client_address=%s (%s)' % (self.client_address,
                                    self.address_string()),
        'command=%s' % self.command,
        'path=%s' % self.path,
        'real path=%s' % parsed_path.path,
        'query=%s' % parsed_path.query,
        'request_version=%s' % self.request_version,
        '',
        'SERVER VALUES:',
        '##############################################################',
        'server_version=%s' % self.server_version,
        'sys_version=%s' % self.sys_version,
        'protocol_version=%s' % self.protocol_version,
        '',
        'HEADERS RECEIVED:',
        '##############################################################',
        ]
        for name, value in sorted(self.headers.items()):
            message_parts.append('%s=%s' % (name, value.rstrip()))
        message_parts.append('##############################################################')
        message_parts.append('')
        message = '\r\n'.join(message_parts)
        self.send_response(200)
        self.end_headers()
        self.wfile.write(message.encode())

    def do_POST(self):
        body = self.rfile.read(int(self.headers['Content-Length']))
        data = json.loads(str(body, 'utf-8'))
        activity = Activity.deserialize(data)

        if not self.__handle_authentication(activity):
            return

        if activity.type == ActivityTypes.conversation_update.value:
            self.__handle_conversation_update_activity(activity)
        elif activity.type == ActivityTypes.message.value:
            self.__handle_message_activity(activity)
        else:
            self.__unhandled_activity()

try:
    SERVER = http.server.HTTPServer((HOST, PORT), BotRequestHandler)
    print('The echo LUIS bot has started')
    SERVER.serve_forever()
except KeyboardInterrupt:
    print('^C received, shutting down server')
    SERVER.socket.close()
