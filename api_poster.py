import requests
from config import *


class GUKLYAPI:
    
    def __init__(self, api_token, endpoint):
        self.api_token = api_token
        self.endpoint = endpoint
        self.session = requests.Session()
        self.session.headers = {'Authorization': self.api_token}
        
    def list(self, params=None):
        if params is None:
            params = {}
        return self.session.get(self.endpoint, params=params,).json()
    
    def get(self, pk):
        return self.session.get(self.endpoint + str(pk) + '/', ).json()
    
    def create(self, data):
        return self.session.post(self.endpoint, data)

    def delete(self, pk):
        return self.session.delete(self.endpoint + str(pk) + '/', ).json()
    
    def update(self, pk, data):
        return self.session.put(self.endpoint + str(pk) + '/', data=data).json()


api = GUKLYAPI(API_TOKEN, 'https://gukly.com/clients/lionpost/')
