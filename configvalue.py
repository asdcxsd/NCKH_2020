MONGODB_HOST = 'localhost'
MONGODB_PORT = 27017
MONGODB_USERNAME = ''
MONGODB_PASSWORD =  ''
MONGODB_NAMEDB = 'nckh_2020_frameworkscan'

# value run excute
import os
DICTIONLARY_HOME =  os.path.abspath(os.path.dirname(__file__)) + "/"
PUBLIC_FOLDER = DICTIONLARY_HOME + "PUBLIC/"
ALLOWED_EXTENSIONS = set(['html', 'zip'])
UPLOAD_FOLDER_TOOLS = DICTIONLARY_HOME + "Tools/ToolReconnai/tools/"
FOLDER_TOOLS = DICTIONLARY_HOME + "Tools/ToolReconnai/"

DB_PDFRECON = 'reportPDF'
DB_TOOLRECON = "recontool"
DB_DIR = "dir"
DB_ENTRYPOINT = 'entrypoint'
DB_PORT = 'port'
DB_TECHNOLOGY = 'framework'
DB_SCREENSHOT = 'screenshot'
DB_VULN = 'vulnerable'

PUBLIC_IP = "75.119.131.210" 
USERNAME_VPS = "parisk" 
PASSWORD_VPS = "1"

