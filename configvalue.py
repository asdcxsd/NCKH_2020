MONGODB_HOST = 'localhost'
MONGODB_PORT = 27017
MONGODB_USERNAME = ''
MONGODB_PASSWORD =  ''
MONGODB_NAMEDB = 'mta_frameworkscan'

# value run excute
import os
DICTIONARY_HOME =  os.path.abspath(os.path.dirname(__file__)) + "/"
PUBLIC_FOLDER = DICTIONARY_HOME + "PUBLIC/"
ALLOWED_EXTENSIONS = set(['html', 'zip'])
UPLOAD_FOLDER_TOOLS = DICTIONARY_HOME + "Tools/ToolsUpload/"
FOLDER_TOOLS = DICTIONARY_HOME + "Framework/Library/"
UPDATE_FOLDER_POCS = DICTIONARY_HOME + "Tools/PocsUpload/"
FOLDER_POCS = DICTIONARY_HOME + "Framework/Library/Function/Function/PocSuite/pocs/"

DB_PDFRECON = 'reportPDF'
DB_TOOLRECON = "recontool"
DB_DIR = "dir"
DB_ENTRYPOINT = 'entrypoint'
DB_PORT = 'port'
DB_TECHNOLOGY = 'framework'
DB_SCREENSHOT = 'screenshot'
DB_CVES = 'cves_scan'
DB_VULN = 'vulnerable'

PUBLIC_IP = "75.119.131.210" 
USERNAME_VPS = "parisk" 
PASSWORD_VPS = "1"


