import openai
from config import conf
from common.expired_dict import ExpiredDict

if conf().get('expires_in_seconds'):
    user_session = ExpiredDict(conf().get('expires_in_seconds'))
else:
    user_session = dict()

def main(query,msg):
    pass
