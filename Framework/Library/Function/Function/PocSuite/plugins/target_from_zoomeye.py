from Framework.Library.Function.Function.PocSuite.api import PluginBase
from Framework.Library.Function.Function.PocSuite.api import PLUGIN_TYPE
from Framework.Library.Function.Function.PocSuite.api import logger
from Framework.Library.Function.Function.PocSuite.api import conf
from Framework.Library.Function.Function.PocSuite.api import ZoomEye
from Framework.Library.Function.Function.PocSuite.api import register_plugin
from Framework.Library.Function.Function.PocSuite.api import kb
from Framework.Library.Function.Function.PocSuite.lib.core.exception import PocsuitePluginDorkException


class TargetFromZoomeye(PluginBase):
    category = PLUGIN_TYPE.TARGETS

    def init_zoomeye_api(self):
        self.zoomeye = ZoomEye(username=conf.login_user, password=conf.login_pass)
        if self.zoomeye.get_resource_info():
            info_msg = "[PLUGIN] ZoomEeye search limit {0}".format(self.zoomeye.resources)
            logger.info(info_msg)
        else:
            info_msg = "[PLUGIN] ZoomEye login faild"
            logger.error(info_msg)

    def init(self):
        self.init_zoomeye_api()
        dork = None
        if conf.dork_zoomeye:
            dork = conf.dork_zoomeye
        else:
            dork = conf.dork
        if not dork:
            msg = "Need to set up dork (please --dork or --dork-zoomeye)"
            raise PocsuitePluginDorkException(msg)

        info_msg = "[PLUGIN] try fetch targets from zoomeye with dork: {0}".format(dork)
        logger.info(info_msg)
        targets = self.zoomeye.search(dork, conf.max_page, resource=conf.search_type)
        count = 0
        if targets:
            for target in targets:
                if self.add_target(target):
                    count += 1

        info_msg = "[PLUGIN] get {0} target(s) from zoomeye".format(count)
        logger.info(info_msg)


register_plugin(TargetFromZoomeye)
