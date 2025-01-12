from Framework.Library.Function.Function.PocSuite.lib.controller.controller import start
from Framework.Library.Function.Function.PocSuite.lib.core.common import single_time_warn_message
from Framework.Library.Function.Function.PocSuite.lib.core.data import conf, kb, logger, paths
from Framework.Library.Function.Function.PocSuite.lib.core.datatype import AttribDict
from Framework.Library.Function.Function.PocSuite.lib.core.enums import PLUGIN_TYPE, POC_CATEGORY, VUL_TYPE, POC_SCAN
from Framework.Library.Function.Function.PocSuite.lib.core.option import init, init_options
from Framework.Library.Function.Function.PocSuite.lib.core.plugin import PluginBase, register_plugin
from Framework.Library.Function.Function.PocSuite.lib.core.poc import POCBase, Output
from Framework.Library.Function.Function.PocSuite.lib.core.register import (
    load_file_to_module,
    load_string_to_module,
    register_poc,
)
from Framework.Library.Function.Function.PocSuite.lib.core.settings import DEFAULT_LISTENER_PORT
from Framework.Library.Function.Function.PocSuite.lib.request import requests
from Framework.Library.Function.Function.PocSuite.lib.utils import get_middle_text, generate_shellcode_list, random_str
from Framework.Library.Function.Function.PocSuite.modules.ceye import CEye
from Framework.Library.Function.Function.PocSuite.modules.listener import REVERSE_PAYLOAD
from Framework.Library.Function.Function.PocSuite.modules.seebug import Seebug
from Framework.Library.Function.Function.PocSuite.modules.zoomeye import ZoomEye
from Framework.Library.Function.Function.PocSuite.modules.shodan import Shodan
from Framework.Library.Function.Function.PocSuite.modules.fofa import Fofa
from Framework.Library.Function.Function.PocSuite.modules.censys import Censys
from Framework.Library.Function.Function.PocSuite.modules.spider import crawl
from Framework.Library.Function.Function.PocSuite.modules.httpserver import PHTTPServer
from Framework.Library.Function.Function.PocSuite.shellcodes import OSShellcodes, WebShell
from Framework.Library.Function.Function.PocSuite.lib.core.interpreter_option import OptDict, OptIP, OptPort, OptBool, OptInteger, OptFloat, OptString, \
    OptItems, OptDict

__all__ = (
    'requests', 'PluginBase', 'register_plugin',
    'PLUGIN_TYPE', 'POCBase', 'Output', 'AttribDict', 'POC_CATEGORY', 'VUL_TYPE',
    'register_poc', 'conf', 'kb', 'logger', 'paths', 'DEFAULT_LISTENER_PORT', 'load_file_to_module',
    'load_string_to_module', 'single_time_warn_message', 'CEye', 'Seebug',
    'ZoomEye', 'Shodan', 'Fofa', 'Censys', 'PHTTPServer', 'REVERSE_PAYLOAD', 'get_listener_ip', 'get_listener_port',
    'get_results', 'init_pocsuite', 'start_pocsuite', 'get_poc_options', 'crawl',
    'OSShellcodes', 'WebShell', 'OptDict', 'OptIP', 'OptPort', 'OptBool', 'OptInteger', 'OptFloat', 'OptString',
    'OptItems', 'OptDict', 'get_middle_text', 'generate_shellcode_list', 'random_str')


def get_listener_ip():
    return conf.connect_back_host


def get_listener_port():
    return conf.connect_back_port


def get_current_poc_obj():
    pass


def get_poc_options(poc_obj=None):
    poc_obj = poc_obj or kb.current_poc
    return poc_obj.get_options()


def get_results():
    return kb.results


def init_pocsuite(options={}):
    init_options(options)
    init()


def start_pocsuite():
    start()
