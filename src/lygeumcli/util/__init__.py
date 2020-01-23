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

import pkg_resources
from pprint import pprint


class Subcommand(object):
    name = ''
    __options__ = []

    def __init__(self, handler):
        self.session = handler


    def addOption(self, *args, **kwargs):
      self.__options__.append([args,kwargs])

    def resetOptions(self):
      self.__options__ = []

    def options(self):
      return self.__options__

    def setup(self, parser):
        self.parser = parser
        requiredNamed = parser.add_argument_group('required arguments')
        for args, kwds in self.options():
            requiredNamed.add_argument(*args, **kwds)

    def help(self):
        return self.__doc__

    def main(self, app):
        print(self.name)


class Command(object):
    "Default Command help"
    subcommands = None

    def __init__(self, name, subcommands=None, help=''):
        self.__doc__ = help
        self.name = name
        if subcommands is not None:
            self.subcommands = {}
            for Flow in subcommands:
                self.addFlow(Flow)

    def __repr__(self):
        return "%s:%s" % (self.name, type(self))

    def subcommand_factory(self, Flow):
        return Flow(self)

    def addFlow(self, Flow):
        flow = self.subcommand_factory(Flow)
        self.subcommands[flow.name] = flow

    def setup(self, parser):
        self.parser = parser
        if self.subcommands is not None:
            self.commands = parser.add_subparsers(dest='subcommand',
                                                title=self.name,
                                                help=self.help(),
                                                prog="lygeum "+self.name)
            for flow in self.subcommands.values():
                p = self.commands.add_parser(flow.name, help=flow.help())
                flow.setup(p)

    def help(self):
        return self.__doc__

    def main(self, app):
        import sys
        subcommand = self.subcommands[app.params.subcommand]
        try:
            subcommand.main(app)
        except:
            raise



def getVersion():
    try:
        __version__ = pkg_resources.get_distribution('lygeumcli').version
    except Exception:
        __version__ = 'unknown'
    return __version__
