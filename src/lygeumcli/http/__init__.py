#/**
#  Copyright © Kais OMRI <kais.omri.int@gmail.com>.
#
#  Licensed under the Apache License, Version 2.0 (the "License");
#  you may not use this file except in compliance with the License.
#  You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#/

import requests
import json
from lygeumcli.config import configuration


class Http(object):
    token_uri = '/lygeum/auth/access_token'
    token = ''
    def login(self):
        configuration.validateConfig()
        payload = {'grant_type':'client_credentials', 'client_id':configuration.config_object['default']['client_id'], 'client_secret':configuration.config_object['default']['client_secret']}
        url = configuration.config_object['default']['url'] + self.token_uri
        result = requests.post(url=url,data=payload)
        response = self.response(result)
        if not self.is_json(result.content):
            print('unable to login please check your configuration \n', result.content)
            raise SystemExit()
        self.token = response.json()['access_token']
    
    def get(self, uri, params={}):
        self.login()
        headers = {'Authorization': 'Bearer {}'.format(self.token)}
        url= configuration.config_object['default']['url'] + '/lygeum/api' + uri
        result = requests.get(url, headers=headers,params=params)
        return self.response(result)

    def response(self, result):
        if self.is_json(result.content) and hasattr(result.json(), 'error'):
            print('got lygeum api error ', result.json()['message'])
            raise SystemExit()
        else:
            return result
    
    def is_json(self, str):
        try:
            json.loads(str)
        except ValueError as e:
            return False
        return True


http = Http()