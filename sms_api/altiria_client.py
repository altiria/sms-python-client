#!/usr/bin/python
# -*- coding: utf-8 -*-

import requests
import sys
import json as JSON
import logging as log
import logging.config

sys.path.append('.')
from sms_api.exceptions import GeneralAltiriaException
from sms_api.exceptions import AltiriaGwException
from sms_api.exceptions import ConnectionException
from sms_api.exceptions import JsonException

class AltiriaModelTextMessage():

    destination=None
    message=None
    senderId=None
    ack=False
    idAck=None
    concat=False
    certDelivery=False
    encoding=None

    #Constructor
    def __init__(self, destination, message, senderId=None):
        self.destination=destination
        self.message=message
        if senderId!=None:
            self.senderId=senderId

    def replaceStr(self,str):
        if str==None:
            return 'None'
        elif str==True:
            return 'True'
        elif str==False:
            return 'False'
        else:
            return str

    def toString(self):
        return 'AltiriaModelTextMessage [destination='+self.replaceStr(self.destination)+', message='+self.replaceStr(self.message)+', senderId='+self.replaceStr(self.senderId)+', ack='+self.replaceStr(self.ack)+', idAck='+self.replaceStr(self.idAck)+', concat='+self.replaceStr(self.concat)+', certDelivery='+self.replaceStr(self.certDelivery)+', encoding='+self.replaceStr(self.encoding)+']'

class AltiriaClient():

    login=None
    passwd=None
    textMessage=None
    isApiKey=False

    #Constructor
    def __init__(self, login, password, isApiKey=False, timeout=None):
        self.login=login
        self.passwd=password
        self.isApiKey=isApiKey
        if timeout!=None:
            self.setTimeout(timeout)

    # connection timeout values are defined here
    __connectionTimeout=3000
    __maxConnectTimeout=10000
    __minConnectTimeout=1000

    # response timeout values are defined here
    __timeout=10000
    __maxTimeout=30000
    __minTimeout=1000

    # API URL
    urlBase='https://www.altiria.net:8443/apirest/ws'
    
    # Library name/version
    source='lib-python-pip-1_0'

    def setConnectionTimeout(self,connectionTimeout):
        if connectionTimeout > self.__maxConnectTimeout:
            self.__connectionTimeout=3000
        elif connectionTimeout < self.__minConnectTimeout:
            self.__connectionTimeout=3000
        else:
            self.__connectionTimeout=connectionTimeout

    def setTimeout(self,timeout):
        if timeout > self.__maxTimeout:
            self.__timeout=10000
        elif timeout < self.__minTimeout:
            self.__timeout=10000
        else:
            self.__timeout=timeout

    #Send a SMS.
    def sendSms(self, textMessage):
        log.info('Altiria-sendSms CMD: '+textMessage.toString())

        destinations=[]
        messageData={}
        try:
            if self.login==None:
                log.error('ERROR: The login parameter is mandatory')
                raise JsonException('LOGIN_NOT_NULL')
            
            if self.passwd==None:
                log.error('ERROR: The password parameter is mandatory')
                raise JsonException('PASSWORD_NOT_NULL')

            if textMessage.destination==None or textMessage.destination.strip()=='':
                log.error('ERROR: The destination parameter is mandatory')
                raise AltiriaGwException('INVALID_DESTINATION', '015')
            else:
                destinations.append(textMessage.destination)

            if textMessage.message==None or textMessage.message.strip()=='':
                log.error('ERROR: The message parameter is mandatory')
                raise AltiriaGwException('EMPTY_MESSAGE', '017')
            else:
                messageData = {'msg': textMessage.message}

            if textMessage.senderId!=None and textMessage.senderId.strip()!='':
                messageData['senderId']=textMessage.senderId

            if textMessage.ack:
                messageData['ack']=True
                if textMessage.idAck!=None and textMessage.idAck.strip()!='':
                    messageData['idAck']=textMessage.idAck

            if textMessage.concat:
                messageData['concat']=True

            if textMessage.certDelivery:
                messageData['certDelivery']=True

            if textMessage.encoding!=None and textMessage.encoding.strip()=='unicode':
                messageData['encoding']=textMessage.encoding.strip()

            loginKey =  'apikey' if self.isApiKey else 'login'
            passwordKey =  'apisecret' if self.isApiKey else 'passwd'
            credentials = {loginKey: self.login, passwordKey: self.passwd}
            jsonData = {}
            jsonData['credentials']=credentials
            jsonData['destination']=destinations
            jsonData['message']=messageData
            jsonData['source']=self.source
            contentType = {'Content-Type':'application/json;charset=utf-8'}

            try:
                response = requests.post(self.urlBase+'/sendSms',
                        data=JSON.dumps(jsonData),
                        headers=contentType,
                        timeout=(self.__connectionTimeout/1000, self.__timeout/1000))
                log.info('HTTP status: '+str(response.status_code))
                log.info('HTTP body: '+response.text)

                jsonParsed = JSON.loads(response.text)
                if str(response.status_code) != '200':
                    log.error('ERROR: Invalid request: '+response.text)
                    errorMsg = str(jsonParsed['error'])
                    raise JsonException(errorMsg)
                else:
                    status = str(jsonParsed['status'])
                    if status != '000':
                        errorMsg=self.__getStatus(status)
                        log.error('ERROR: Invalid parameter response. Error message: ' + errorMsg + ', Status: ' + status)
                        raise AltiriaGwException(errorMsg,status)
                    else:
                        return response.text
            except requests.ConnectTimeout:
                log.error('ERROR: Connection timeout')
                raise ConnectionException('CONNECTION_TIMEOUT')
            except requests.ReadTimeout:
                log.error('ERROR: Response timeout')
                raise ConnectionException('RESPONSE_TIMEOUT')
        except GeneralAltiriaException:
            raise
        except Exception as e:
            log.error('ERROR: Unexpected error: '+e)
            raise AltiriaGwException('GENERAL_ERROR','001')


    # Get the user credit.
    def getCredit(self):
        log.info('Altiria-getCredit CMD')

        try:
            if self.login==None:
                log.error('ERROR: The login parameter is mandatory')
                raise JsonException('LOGIN_NOT_NULL')
            
            if self.passwd==None:
                log.error('ERROR: The password parameter is mandatory')
                raise JsonException('PASSWORD_NOT_NULL')

            loginKey =  'apikey' if self.isApiKey else 'login'
            passwordKey =  'apisecret' if self.isApiKey else 'passwd'
            credentials = {loginKey: self.login, passwordKey: self.passwd}
            jsonData = {}
            jsonData['credentials']=credentials
            jsonData['source']=self.source
            contentType = {'Content-Type':'application/json;charset=UTF-8'}
            try:
                response = requests.post(self.urlBase+'/getCredit',
                        data=JSON.dumps(jsonData),
                        headers=contentType,
                        timeout=(self.__connectionTimeout/1000, self.__timeout/1000))
                log.info('HTTP status: '+str(response.status_code))
                log.info('HTTP body: '+response.text)

                jsonParsed = JSON.loads(response.text)
                if str(response.status_code) != '200':
                    log.error('ERROR: Invalid request: '+response.text)
                    errorMsg = str(jsonParsed['error'])
                    raise JsonException(errorMsg)
                else:
                    status = str(jsonParsed['status'])
                    if status != '000':
                        errorMsg=self.__getStatus(status)
                        log.error('ERROR: Invalid parameter response. Error message: ' + errorMsg + ', Status: ' + status)
                        raise AltiriaGwException(errorMsg,status)
                    else:
                        return jsonParsed['credit']
            except requests.ConnectTimeout:
                log.error('ERROR: Connection timeout')
                raise ConnectionException('CONNECTION_TIMEOUT')
            except requests.ReadTimeout:
                log.error('ERROR: Response timeout')
                raise ConnectionException('RESPONSE_TIMEOUT')
        except GeneralAltiriaException:
            raise
        except Exception as e:
            log.error('ERROR: Unexpected error: '+e)
            raise AltiriaGwException('GENERAL_ERROR','001')        


    #Private method that provides the status message through the status code.
    def __getStatus(self,status):
        errorMessage='GENERAL_ERROR'
        if status=='001':
            errorMessage='INTERNAL_SERVER_ERROR'
        elif status=='002':
            errorMessage = "SSL_PORT_ERROR"
        elif status=='010':
            errorMessage = 'DESTINATION_FORMAT_ERROR'
        elif status=='013':
            errorMessage = 'MESSAGE_IS_TOO_LONG'
        elif status=='014':
            errorMessage = 'INVALID_HTTP_REQUEST_ENCODING'
        elif status=='015':
            errorMessage = 'INVALID_DESTINATION'
        elif status=='016':
            errorMessage = 'DUPLICATED_DESTINATION'
        elif status=='017':
            errorMessage = 'EMPTY_MESSAGE'
        elif status=='018':
            errorMessage = 'TOO_MANY_DESTINATIONS'
        elif status=='019':
            errorMessage = 'TOO_MANY_MESSAGES'
        elif status=='020':
            errorMessage = 'AUTHENTICATION_ERROR'
        elif status=='033':
            errorMessage = 'INVALID_DESTINATION_SMS_PORT'
        elif status=='034': 
            errorMessage = 'INVALID_ORIGIN_SMS_PORT'
        elif status=='035': 
            errorMessage = 'INVALID_LANDING'
        elif status=='036': 
            errorMessage = 'LANDING_NOT_EXISTS'
        elif status=='037': 
            errorMessage = 'TOO_MANY_LANDINGS'
        elif status=='038': 
            errorMessage = 'SYNTAX_LANDING_ERROR'
        elif status=='039':
            errorMessage = 'SYNTAX_WEB_PARAMS_ERROR'
        return errorMessage








   
