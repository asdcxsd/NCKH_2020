from Tools.PocSuite.lib.controller.controller import start
from Tools.PocSuite.lib.core.common import single_time_warn_message
from Tools.PocSuite.lib.core.data import conf, kb, logger, paths
from Tools.PocSuite.lib.core.datatype import AttribDict
from Tools.PocSuite.lib.core.enums import PLUGIN_TYPE, POC_CATEGORY, VUL_TYPE, POC_SCAN
from Tools.PocSuite.lib.core.option import init, init_options
from Tools.PocSuite.lib.core.plugin import PluginBase, register_plugin
from Tools.PocSuite.lib.core.poc import POCBase, Output
from Tools.PocSuite.lib.core.register import (
    load_file_to_module,
    load_string_to_module,
    register_poc,
)
from Tools.PocSuite.lib.core.settings import DEFAULT_LISTENER_PORT
from Tools.PocSuite.lib.request import requests
from Tools.PocSuite.lib.utils import get_middle_text, generate_shellcode_list, random_str
from Tools.PocSuite.modules.ceye import CEye
from Tools.PocSuite.modules.listener import REVERSE_PAYLOAD
from Tools.PocSuite.modules.seebug import Seebug
from Tools.PocSuite.modules.zoomeye import ZoomEye
from Tools.PocSuite.modules.shodan import Shodan
from Tools.PocSuite.modules.fofa import Fofa
from Tools.PocSuite.modules.censys import Censys
from Tools.PocSuite.modules.spider import crawl
from Tools.PocSuite.modules.httpserver import PHTTPServer
from Tools.PocSuite.shellcodes import OSShellcodes, WebShell
from Tools.PocSuite.lib.core.interpreter_option import OptDict, OptIP, OptPort, OptBool, OptInteger, OptFloat, OptString, \
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
