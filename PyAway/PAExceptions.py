'''
Exception class
'''

class PAException(Exception):
    '''
    Custom exception class
    '''
    def __init__(self, status_code, message, errorCode):
        super(PAException, self).__init__(message)
        self.status_code = status_code
        self.errorCode = errorCode
