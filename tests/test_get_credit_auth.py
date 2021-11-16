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


class TestGetCreditAuth(unittest.TestCase,Config):

    
    # The login parameter is missed.
    def test_error_no_login(self):
        if Config.debug:
            print('test_error_no_login')

        try:
            client = AltiriaClient(None, Config.password)
            client.getCredit()
            self.fail('JsonException should have been thrown')

        except JsonException as je:
            self.assertEqual('LOGIN_NOT_NULL', je.message)
    

    # The password parameter is missed.
    def test_error_no_password(self):
        if Config.debug:
            print('test_error_no_password')

        try:
            client = AltiriaClient(Config.login, None)
            client.getCredit()
            self.fail('JsonException should have been thrown')

        except JsonException as je:
            self.assertEqual('PASSWORD_NOT_NULL', je.message)


if __name__ == '__main__':
    unittest.main()