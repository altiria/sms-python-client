# -*- coding: utf-8 -*-

class GeneralAltiriaException(Exception):
    message=None
    status=None

    #Constructor
    def __init__(self,message,status):
        self.message=message
        self.status=status

class AltiriaGwException(GeneralAltiriaException):

    #Constructor
    def __init__(self,message,status):
        GeneralAltiriaException.__init__(self,message,status)

class ConnectionException(GeneralAltiriaException):

    #Constructor
    def __init__(self,message):
       GeneralAltiriaException.__init__(self,message,None)

class JsonException(GeneralAltiriaException):

    #Constructor
    def __init__(self,message):
        GeneralAltiriaException.__init__(self,message,None)