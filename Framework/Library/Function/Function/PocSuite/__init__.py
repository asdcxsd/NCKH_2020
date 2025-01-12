__title__ = 'pocsuite'
__version__ = '1.6.5'
__author__ = 'Knownsec Security Team'
__author_email__ = 's1@seebug.org'
__license__ = 'GPL 2.0'
__copyright__ = 'Copyright 2018 Knownsec'
__name__ = 'Framework..PocSuite'
__package__ = 'Framework.Library.Function.Function.PocSuite'

from .lib.core.common import set_paths
from .cli import module_path


set_paths(module_path())
