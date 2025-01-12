from Tools.ToolReconnai.report.acunetix import quick_report as report_acunetix


def get_report_acunetix(filename):
    gen = report_acunetix(filename)
    data =gen.getdata()
    data = [{
        "Vuln" : i[0],
        "Item" :  i[1][1], 
        "Parameter" : i[2][1],
        "Request" :  i[4]
    } for i in data[2:]]
    return data