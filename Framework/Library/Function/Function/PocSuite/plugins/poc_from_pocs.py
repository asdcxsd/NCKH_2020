# load poc from pocs directories
import os

from Framework.Library.Function.Function.PocSuite.api import PLUGIN_TYPE
from Framework.Library.Function.Function.PocSuite.api import PluginBase
from Framework.Library.Function.Function.PocSuite.api import logger
from Framework.Library.Function.Function.PocSuite.api import paths
from Framework.Library.Function.Function.PocSuite.api import register_plugin


class PocFromPocs(PluginBase):
    category = PLUGIN_TYPE.POCS

    def init(self):
        _pocs = []
        for root, dirs, files in os.walk(paths.POCSUITE_POCS_PATH):
            files = filter(lambda x: not x.startswith("__") and x.endswith(".py"), files)
            _pocs.extend(map(lambda x: os.path.join(root, x), files))
        for f in _pocs:

            if self.add_poc_from_file(f):
                info_msg = "[PLUGIN] load PoC script '{0}' from pocs directories success".format(f)
            else:
                info_msg = "[PLUGIN] load PoC script '{0}' from pocs directories failed".format(f)
            logger.info(info_msg)


register_plugin(PocFromPocs)
