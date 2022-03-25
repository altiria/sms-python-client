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


class TestGetCreditHttp(unittest.TestCase,Config):

    
    # Basic case.
    def test_ok(self):
        if Config.debug:
            print('test_ok')
        
        client = AltiriaClient(Config.login, Config.password)
        credit = client.getCredit()

        # Check your credit here    
        # self.assertEqual('100.00',credit)

    # Basic case using apikey.
    def test_ok_apikey(self):
        if Config.debug:
            print('test_ok_apikey')
        
        client = AltiriaClient(Config.apiKey, Config.apiSecret, True)
        credit = client.getCredit()

        # Check your credit here
        # self.assertEqual('100.00',credit) 

    # Invalid credentials.
    def test_error_invalid_credentials(self):
        if Config.debug:
            print('test_error_invalid_credentials')

        try:
            client = AltiriaClient('unknown', Config.password)
            client.getCredit()
            self.fail('AltiriaGwException should have been thrown')

        except AltiriaGwException as ae:
            self.assertEqual('AUTHENTICATION_ERROR', ae.message)
            self.assertEqual('020', ae.status)

if __name__ == '__main__':
    unittest.main()