from random import random
from bs4 import BeautifulSoup
import random
import lxml


class quick_report:
    soup = None

    def __init__(self, file):
        self.soup = BeautifulSoup(
            open(file, encoding="utf8"), features="lxml")

    def getdata(self):
        tables = self.soup.find_all('table')
        data = []
        for table in tables:
            datax = []
            rows = table.find_all('tr')
            for row in rows:
                columns = row.find_all('td')
                datax.append([ele.text.strip() for ele in columns if ele])
            
           
            data.append(datax)
        return data


if __name__ == "__main__":
    file = "18.html"
    report = quick_report(file)
    data = report.getdata()
    for i in range(2, len(data)):
        print(data[i][0])
        print(data[i][1])
        print(data[i][2])
        print(data[i][4])