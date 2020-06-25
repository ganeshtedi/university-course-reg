import os

class Config(object):
    SECRET_KEY = os.environ.get('SECRET_KEY') or b'\xf8\xf6K\x17V%\xb8z\x1fE\xd5\xda\xa6\x00\x7f\xd1'
    
    
    MONGODB_SETTINGS = { 'db' : 'UTA_Enrollment'
    }