from Tools.PocSuite.api import PluginBase
from Tools.PocSuite.api import PLUGIN_TYPE
from Tools.PocSuite.api import logger
from Tools.PocSuite.api import conf
from Tools.PocSuite.api import Shodan
from Tools.PocSuite.api import register_plugin
from Tools.PocSuite.api import kb
from Tools.PocSuite.lib.core.exception import PocsuitePluginDorkException


class TargetFromShodan(PluginBase):
    category = PLUGIN_TYPE.TARGETS

    def init_shodan_api(self):
        self.shodan = Shodan(token=conf.shodan_token)
        if self.shodan.get_resource_info():
            info_msg = "[PLUGIN] shodan credits limit {0}".format(self.shodan.credits)
            logger.info(info_msg)

    def init(self):
        self.init_shodan_api()
        dork = None
        if conf.dork_shodan:
            dork = conf.dork_shodan
        else:
            dork = conf.dork
        if not dork:
            msg = "Need to set up dork (please --dork or --dork-shodan)"
            raise PocsuitePluginDorkException(msg)

        if kb.comparison:
            kb.comparison.add_dork("Shodan", dork)
        info_msg = "[PLUGIN] try fetch targets from shodan with dork: {0}".format(dork)
        logger.info(info_msg)
        targets = self.shodan.search(dork, conf.max_page, resource=conf.search_type)
        count = 0
        if targets:
            for target in targets:
                if kb.comparison:
                    kb.comparison.add_ip(target, "Shodan")
                if self.add_target(target):
                    count += 1

        info_msg = "[PLUGIN] get {0} target(s) from shodan".format(count)
        logger.info(info_msg)


register_plugin(TargetFromShodan)
