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

import sys
import traceback
from pprint import pprint
from cli.log import LoggingApp
from lygeumcli.config import configuration
from lygeumcli.util import Command,Subcommand,getVersion
from lygeumcli.commands.properties import DownloadApp
from lygeumcli.commands.environments import EnvironmentsApp


def get_commands():
  a = Command('properties', [ DownloadApp ], help='manage properties' )
  c = Command('environments', [ DownloadApp, EnvironmentsApp], help='manage environments' )
  return [ a, c, configuration ]

class Application(LoggingApp):
  """The Lygeum CLI
  """
  name = "lygeum"
  commands = { }

  def setup(self):
    # just after wrapping argument during __call__
    # !? or during __init__
    self.exit_after_main = True
    super(Application, self).setup()
    self.add_param("--version", help="print the Lygeum CLI version", version=getVersion(), action='version')
    self.subparsers = self.argparser.add_subparsers(dest='command', help='')
    for dev in get_commands():
      self.add_command( dev )

  def pre_run(self):
    # called just before main, updates params, parses args
    super(Application, self).pre_run()

  def add_command(self, command):
    self.commands[command.name] = command
    parser = self.subparsers.add_parser(command.name, help=command.help())
    #parser.set_defaults(run=self.main)
    command.setup(parser)

  def start(self):
    command  = self.commands[self.params.command]
    try:
      command.main(self)
    except:
      raise

  main = start 

def main():
    """Entry point for the application script"""
    try:
        app = Application()
        app.run()
    except: # catch *all* exceptions
        exec_type, exec_value, exec_traceback = sys.exc_info()
        if(exec_type == SystemExit):
           return
        else:
           print('Lygeum CLI error:\n', 'type: {}\nexception: {}\nstacktrace: {}'.format(exec_type, exec_value, exec_traceback))
           if app.params.verbose >= 1:
             traceback.print_exception(exec_type, exec_value, exec_traceback,limit=50, file=sys.stdout)