from Framework.Library.Function.Function.PocSuite.api import PluginBase
from Framework.Library.Function.Function.PocSuite.api import PLUGIN_TYPE
from Framework.Library.Function.Function.PocSuite.api import logger
from Framework.Library.Function.Function.PocSuite.api import conf
from Framework.Library.Function.Function.PocSuite.api import Fofa
from Framework.Library.Function.Function.PocSuite.api import register_plugin
from Framework.Library.Function.Function.PocSuite.api import kb
from Framework.Library.Function.Function.PocSuite.lib.core.exception import PocsuitePluginDorkException


class TargetFromFofa(PluginBase):
    category = PLUGIN_TYPE.TARGETS

    def init_fofa_api(self):
        self.fofa = Fofa(user=conf.fofa_user,token=conf.fofa_token)

    def init(self):
        self.init_fofa_api()
        dork = None
        if conf.dork_fofa:
            dork = conf.dork_fofa
        else:
            dork = conf.dork
        if not dork:
            msg = "Need to set up dork (please --dork or --dork-fofa)"
            raise PocsuitePluginDorkException(msg)

        if kb.comparison:
            kb.comparison.add_dork("Fofa", dork)
        info_msg = "[PLUGIN] try fetch targets from Fofa with dork: {0}".format(dork)
        logger.info(info_msg)
        targets = self.fofa.search(dork, conf.max_page, resource=conf.search_type)
        count = 0
        if targets:
            for target in targets:
                if kb.comparison:
                    kb.comparison.add_ip(target, "Fofa")
                if self.add_target(target):
                    count += 1

        info_msg = "[PLUGIN] get {0} target(s) from Fofa".format(count)
        logger.info(info_msg)

register_plugin(TargetFromFofa)
