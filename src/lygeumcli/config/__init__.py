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

from __future__ import print_function, unicode_literals
import os
from lygeumcli.util import Command
from pprint import pprint
from PyInquirer import style_from_dict, Token, prompt
from PyInquirer import Validator, ValidationError
from configparser import ConfigParser



class StringNotEmptyValidator(Validator):
    def validate(self, document):
        if not document.text:
            raise ValidationError(
                message='Please enter a valid input',
                cursor_position=len(document.text))

class UrlValidator(Validator):
    def validate(self, document):
        if not document.text or not (document.text.startswith('http://') or document.text.startswith('https://')):
            raise ValidationError(
                message='Please enter a valid url',
                cursor_position=0)

class Configurator(Command):
    
    config_object = ConfigParser()
    config_file = os.path.join(os.path.expanduser("~"), '.lygeum', 'credentials')
    
    def __init__(self, name, subcommands=None, help=''):
        super(Configurator, self).__init__(name=name, subcommands=subcommands, help=help)
        self.readConfig()

    def writeConfig(self):
        if not os.path.exists(os.path.dirname(self.config_file)):
          try:
             os.makedirs(os.path.dirname(self.config_file))
          except OSError as exc: # Guard against race condition
             if exc.errno != errno.EEXIST:
               raise
        with open(self.config_file, 'w') as conf:
            self.config_object.write(conf)
    
    def readConfig(self):
        self.config_object.read(self.config_file)

    def validateConfig(self):
        self.readConfig()
        try:
            if not (self.config_object['default']['client_id'] and self.config_object['default']['client_secret'] and self.config_object['default']['url']):      
                print('Lygeum CLI configuration problem please run [lygeum configure] to initialize the config.')
                raise SystemExit(1)
        except:
            print('Lygeum CLI configuration problem please run [lygeum configure] to initialize the config.')
            raise SystemExit(1)

    def main(self, app):
        style = style_from_dict({
            Token.Separator: '#cc5454',
            Token.QuestionMark: '#673ab7 bold',
            Token.Selected: '#cc5454',
            Token.Pointer: '#673ab7 bold',
            Token.Instruction: '',
            Token.Answer: '#f44336 bold',
            Token.Question: '',
        })
        questions = [
            {
                'type': 'input',
                'name': 'client_id',
                'message': 'Client Id: ',
                'validate': StringNotEmptyValidator
            },
            {
                'type': 'input',
                'name': 'client_secret',
                'message': 'Client Secret: ',
                'validate': StringNotEmptyValidator
            },
            {
                'type': 'input',
                'name': 'url',
                'message': 'Lygeum url: ',
                'validate': UrlValidator
            }
        ]
        import sys
        try:
            answers = prompt(questions, style=style)
        except:
            type, value, traceback = sys.exc_info()
            print('Configure error:\n', 'type: {}\nexception: {}\nstacktrace: {}'.format(type, value, traceback))
            return
        self.config_object["default"] = answers
        self.writeConfig()


configuration = Configurator(name='configure', help='configure the Lygeum CLI')