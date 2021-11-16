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


class TestSendSmsAuth(unittest.TestCase,Config):

    
    # The login parameter is missed.
    def test_error_no_login(self):
        if Config.debug:
            print('test_error_no_login')

        try:
            message='Lorem Ipsum is simply dummy text'
            client = AltiriaClient(None, Config.password)
            textMessage = AltiriaModelTextMessage(Config.destination, message)
            client.sendSms(textMessage)
            self.fail('JsonException should have been thrown')

        except JsonException as je:
            self.assertEqual('LOGIN_NOT_NULL', je.message)
    

    # The password parameter is missed.
    def test_error_no_password(self):
        if Config.debug:
            print('test_error_no_password')

        try:
            message='Lorem Ipsum is simply dummy text'
            client = AltiriaClient(Config.login, None)
            textMessage = AltiriaModelTextMessage(Config.destination, message)
            client.sendSms(textMessage)
            self.fail('JsonException should have been thrown')

        except JsonException as je:
            self.assertEqual('PASSWORD_NOT_NULL', je.message)
    

    # The destination parameter is missed.
    def test_error_no_destination(self):
        if Config.debug:
            print('test_error_no_destination')

        try:
            message='Lorem Ipsum is simply dummy text'
            client = AltiriaClient(Config.login, Config.password)
            textMessage = AltiriaModelTextMessage(None, message)
            client.sendSms(textMessage)
            self.fail('JsonException should have been thrown')

        except AltiriaGwException as ae:
            self.assertEqual('INVALID_DESTINATION', ae.message)
            self.assertEqual('015', ae.status)
    

    # The message parameter is missed.
    def test_error_no_message(self):
        if Config.debug:
            print('test_error_no_message')

        try:
            message='Lorem Ipsum is simply dummy text'
            client = AltiriaClient(Config.login, Config.password)
            textMessage = AltiriaModelTextMessage(Config.destination, None)
            client.sendSms(textMessage)
            self.fail('JsonException should have been thrown')

        except AltiriaGwException as ae:
            self.assertEqual('EMPTY_MESSAGE', ae.message)
            self.assertEqual('017', ae.status)


if __name__ == '__main__':
    unittest.main()