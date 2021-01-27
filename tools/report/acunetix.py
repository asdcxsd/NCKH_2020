
from bs4 import BeautifulSoup
import lxml

class report_acunetix:
    soup = None
    tags = None
    connect = None
    def __init__(self, file, connect=None):

        self.soup = BeautifulSoup(open("17.html", encoding="utf8"), features="lxml")
        self.tags = self.soup.find_all('h3')
        self.connect = connect
    def getdetails(self):
        print("Scan details")
        data1= []
        scan_details_table= self.soup.find('table', attrs={'class':'ax-scan-summary'})
        #print(scan_details_table)
        table_body1s = scan_details_table.find('tbody')
        rows = table_body1s.find_all('tr')
        for row in rows:
            cols= row.find_all('td')
            cols = [ele.text.strip() for ele in cols]
            data1.append([ele for ele in cols if ele])
        return data1
    def getdata(self):
        print('Affected items')
        affected_items_table= self.soup.find_all('table')
        dataall = []
        for table_body2 in affected_items_table:
            datax=[]
            rows = table_body2.find_all('tr')
            for row in rows:
                datax.append([ele.text.strip() for ele in row('td') if ele])
            dataall.append(datax)
        return dataall

    def pushdb(self):
        if self.connect == None: 
            print("Not connect database!")
            return 0
        
if __name__ == "__main__":
    file = "17.html"
    report = report_acunetix(file)
    data = report.getdetails()
    print(data)
    data = report.getdata()
    print(data)

