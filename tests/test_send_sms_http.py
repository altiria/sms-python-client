# -*- coding: utf-8 -*-

import sys
import unittest
import json as JSON

sys.path.append('.')
from sms_api.altiria_client import AltiriaClient
from sms_api.altiria_client import AltiriaModelTextMessage
from sms_api.exceptions import AltiriaGwException
from sms_api.exceptions import ConnectionException
from sms_api.exceptions import JsonException
from tests import Config


class TestSendSmsHttp(unittest.TestCase,Config):

    
    # Only mandatory parameters are sent.
    def test_ok_mandatory_params(self):
        if Config.debug:
            print('test_ok_mandatory_params')

        message='Lorem Ipsum is simply dummy text'
        client = AltiriaClient(Config.login, Config.password)
        textMessage = AltiriaModelTextMessage(Config.destination, message)
        jsonText = client.sendSms(textMessage)
        jsonObject = JSON.loads(jsonText)

        self.assertEqual('000',jsonObject['status'])
        details=jsonObject['details']
        self.assertEqual(Config.destination, str(details[0]['destination']))
        self.assertEqual('000', str(details[0]['status']))
    
    
    # All params are sent.
    # Features:
    # - sender
    # - delivery confirmation with identifier
    # - concatenated
    # - set unicode encoding
    # - request delivery certificate
    def test_ok_all_params(self):
        if Config.debug:
            print('test_ok_all_params')

        message='Lorem Ipsum is simply dummy text of the printing and typesetting industry \u20AC'
        idAck='idAck'

        client = AltiriaClient(Config.login, Config.password)
        textMessage = AltiriaModelTextMessage(Config.destination, message, Config.sender)
        # You can also assign the sender here
        #textMessage.senderId=Config.sender

        # Need to configure a callback URL to use it. Contact comercial@altiria.com.
        #textMessage.ack=True
        #textMessage.idAck=idAck

        textMessage.concat=True
        textMessage.encoding='unicode'

        # If it is uncommented, additional credit will be consumed.
        #textMessage.certDelivery=True

        jsonText = client.sendSms(textMessage)
        jsonObject = JSON.loads(jsonText)

        self.assertEqual('000',jsonObject['status'])
        details=jsonObject['details']
        self.assertEqual(Config.destination+'(0)', str(details[0]['destination']))
        self.assertEqual('000', str(details[0]['status']))

        # Uncomment if idAck is used.
        #self.assertEqual(idAck, str(details[0]['idAck']))

        self.assertEqual(Config.destination+'(1)', str(details[1]['destination']))
        self.assertEqual('000', str(details[1]['status']))

        # Uncomment if idAck is used.
        #self.assertEqual(idAck, str(details[1]['idAck']))

    
    # Invalid credentials.
    def test_error_invalid_credentials(self):
        if Config.debug:
            print('test_error_invalid_credentials')

        try:
            message='Lorem Ipsum is simply dummy text'
            client = AltiriaClient('unknown', Config.password)
            textMessage = AltiriaModelTextMessage(Config.destination, message)
            client.sendSms(textMessage)
            self.fail('AltiriaGwException should have been thrown')

        except AltiriaGwException as ae:
            self.assertEqual('AUTHENTICATION_ERROR', ae.message)
            self.assertEqual('020', ae.status)
    

    # The destination parameter is invalid.
    def test_error_invalid_destination(self):
        if Config.debug:
            print('test_error_invalid_destination')

        try:
            message='Lorem Ipsum is simply dummy text'
            client = AltiriaClient(Config.login, Config.password)
            textMessage = AltiriaModelTextMessage('invalid', message)
            client.sendSms(textMessage)
            self.fail('AltiriaGwException should have been thrown')

        except AltiriaGwException as ae:
            self.assertEqual('INVALID_DESTINATION', ae.message)
            self.assertEqual('015', ae.status)
    
    
    # The message parameter is empty.
    def test_error_empty_message(self):
        if Config.debug:
            print('test_error_empty_message')

        try:
            message=''
            client = AltiriaClient(Config.login, Config.password)
            textMessage = AltiriaModelTextMessage(Config.destination, message)
            client.sendSms(textMessage)
            self.fail('AltiriaGwException should have been thrown')

        except AltiriaGwException as ae:
            self.assertEqual('EMPTY_MESSAGE', ae.message)
            self.assertEqual('017', ae.status)
    

if __name__ == '__main__':
    unittest.main()
