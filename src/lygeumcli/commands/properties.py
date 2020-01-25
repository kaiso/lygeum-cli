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

from lygeumcli.util import Subcommand
from lygeumcli.http import http
import traceback

class DownloadApp(Subcommand):
  """Download properties for a given environment and application."""
  name = "download"
  
  def setup(self, parser):
    super(DownloadApp, self).resetOptions()
    super(DownloadApp, self).addOption('-e', '--environment', help='the target environment', required=True)
    super(DownloadApp, self).addOption('-a', '--application', help='the target application', required=True)
    super(DownloadApp, self).addOption('-l', '--layout', help='the wanted format type', required=True, choices=['json', 'properties', 'yaml'])
    super(DownloadApp, self).addOption('-f', '--file', help='the output file', required=True)
    super(DownloadApp, self).setup(parser)
  
  def main(self, app):
      params = {'env':app.params.environment, 'app':app.params.application,'layout':app.params.layout}
      r = http.get('/properties/download', params=params, verbose=app.params.verbose)
      with open(app.params.file, 'wb') as fd:
          for chunk in r.iter_content(chunk_size=128):
            fd.write(chunk)

  