from Tools.PocSuite.api import PluginBase
from Tools.PocSuite.api import PLUGIN_TYPE
from Tools.PocSuite.api import logger
from Tools.PocSuite.api import conf
from Tools.PocSuite.api import Censys
from Tools.PocSuite.api import register_plugin
from Tools.PocSuite.api import kb
from Tools.PocSuite.lib.core.exception import PocsuitePluginDorkException


class TargetFromCensys(PluginBase):
    category = PLUGIN_TYPE.TARGETS

    def init_censys_api(self):
        self.censys = Censys(uid=conf.censys_uid, secret=conf.censys_secret)
        if self.censys.get_resource_info():
            info_msg = "[PLUGIN] Censys credits limit {0}".format(self.censys.credits)
            logger.info(info_msg)

    def init(self):
        self.init_censys_api()
        dork = None
        if conf.dork_censys:
            dork = conf.dork_censys
        else:
            dork = conf.dork
        if not dork:
            msg = "Need to set up dork (please --dork or --dork-censys)"
            raise PocsuitePluginDorkException(msg)
        if kb.comparison:
            kb.comparison.add_dork("Censys", dork)
        info_msg = "[PLUGIN] try fetch targets from censys with dork: {0}".format(dork)
        logger.info(info_msg)
        search_type = conf.search_type
        if search_type == "web":
            search_type = "websites"
        else:
            search_type = "ipv4"
        targets = self.censys.search(dork, conf.max_page, resource=search_type)
        count = 0
        if targets:
            for target in targets:
                if kb.comparison:
                    kb.comparison.add_ip(target, "Censys")
                if self.add_target(target):
                    count += 1

        info_msg = "[PLUGIN] get {0} target(s) from Censys".format(count)
        logger.info(info_msg)


register_plugin(TargetFromCensys)
