from search_engine_parser import GoogleSearch
from urllib.parse import urlparse
import json, sys
from Wappalyzer import Wappalyzer, WebPage

def get_technology(ch): 
    
    wappalyzer = Wappalyzer.latest(update=True)
    webpage = WebPage.new_from_url(ch)
    technology = wappalyzer.analyze_with_versions_and_categories(webpage)
  
    result = {}
    for key, val in technology.items():
        for i in val['categories']:
            value = key + "|" + "|".join(val['versions'])
            if i in result.keys():    
                result[i].append(value)
            else:
                result[i] = [value]
    return str(result)

def get_domain(domain_to_get):
    domains = []
    for ch in domain_to_get: 
        for i in ch:
            temp = i.split("q=")[1].split("&")[0]
            parsed_uri = urlparse(temp)
            domain = '{uri.scheme}://{uri.netloc}/'.format(uri=parsed_uri)
            domains.append(domain)
    return domains
            


def google(query):
    result = []
    count = 1
    while True: 
        search_args = (query,count)
        gsearch = GoogleSearch()
        gresults = gsearch.search(*search_args)
        if len(gresults) != 0: 
            result.append(gresults["link"])
            count += 1
        else: 
    	    break
    
    return get_domain(result)


#domains = []    
#domains = google('site:*.*.gov.vn')
#print(domains)
#domains = ['http://ttnn.mta.edu.vn']
#get_domain(domains)


if __name__ == '__main__':
    try:
        print(get_technology(sys.argv[1]))
    except Exception as e:
        print(e)