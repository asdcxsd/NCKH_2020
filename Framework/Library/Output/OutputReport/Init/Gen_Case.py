from __future__ import print_function
from numpy.core.fromnumeric import size
import pandas as pd
import numpy as np
from weasyprint import HTML
import os
import html 
from Framework.Library.Output.OutputReport.Init.template_case import *
from Framework.Library.Output.OutputReport.Init.data_case import *
#from template_case import *
#from data_case import *
from json2html import *
def convert_html(data):
    if isinstance(data, dict):
        data_new = {}
        for key,value in data.items():
            data_new[key] = json2html.convert(json = value, table_attributes="class=\"table_inbound\"")
        return data_new
    return  json2html.convert(json = data, table_attributes="class=\"table_inbound\"")


def gen_report_case_from_json(data_case, namefile):
    
    html_out = template_head.format('THEO HỒ SƠ ' +  "<br><br><br>HỒ SƠ: " + data_case['IN_NAME'][0])	# case

        # Process case I.1
    html_out = html_out + mark_I + mark_1
#--index_header 
    index_header = 0
    for i in range(len(data_case['OTHER_PROCESS'])):
        try:
            
            ss = ", ".join(data_case['OTHER_PROCESS'][i]['Module'])
            data_case['OTHER_PROCESS'][i]['Module'] = [ss for _ in  range(len(data_case['OTHER_PROCESS'][i]['Name']))]
        except:
            pass
    for name in data_case['OTHER_PROCESS']:
        temp_header = '''<h3>{} {}</h3>'''
        index_header  += 1
        string_index_header  = "1.1.{}".format(index_header)
        html_out += temp_header.format(string_index_header, "Lần quét " + str(index_header))
        tmp_item = [{} for i in range(len(name['Name']))]
        
        for key,value in name.items():
            for ii, val in enumerate(value):
                try:
                    tmp_item[ii][key] = val
                except  Exception as e :
                    print(e)
                    pass
        tmp_items = tmp_item
        index = 0
        '''for _ in tmp_item:
            try:
                index +=1
                tmp_items.append({
                    "TT": index,
                    name:  json2html.convert(json = _, table_attributes="class=\"table_inbound\"")
                    })
            except Exception as e:
                print(e)
        '''

        try:
            df = pd.DataFrame(data=tmp_items)
        
            df.style.set_properties(subset=['TT'], **{'width': '10'})
            #df.reset_index(drop=True, inplace=True)
            #df.index = df.index + 1
            df = df.to_html(index=False)
            #print(df)
            tmp_table = template_table.format('', df)
            # html_out = html_out + mark_TongHop + tmp_table
            html_out = html_out + tmp_table
        except Exception as e:
            print(e)

    html_out = html_out +  mark_2
   # Process Tổng hợp
    index_header = 0
    for name in data_case.keys():
        if not "IN_" in name:
            continue
        temp_header = '''<h3>{} {}</h3>'''
        index_header  += 1
        string_index_header  = "1.2.{}".format(index_header)
        html_out += temp_header.format(string_index_header, name.replace("IN_", ""))
        try:
            tmp_items = []
            index = 0
            if isinstance(data_case[name], list):
                for  _ in data_case[name]:
                    index +=1
                    tmp_items.append({
                        "TT": index,
                        name:  json2html.convert(json = _, table_attributes="class=\"table_inbound\"")
                        
                    })
           
        except Exception as e:
            print(e)

        try:
            df = pd.DataFrame(data=tmp_items)
           
            df.style.set_properties(subset=['TT'], **{'width': '10'})
            #df.reset_index(drop=True, inplace=True)
            #df.index = df.index + 1
            df = df.to_html(index=False)
            #print(df)
            tmp_table = template_table.format('', df)
            # html_out = html_out + mark_TongHop + tmp_table
            html_out = html_out + tmp_table
        except Exception as e:
            print(e)
    index_header = 0
    html_out = html_out + mark_II
    for name in data_case.keys():
        if not "RECON_" in name:
            continue
        temp_header = '''<h2>{} {}</h2>'''
        index_header  += 1
        string_index_header  = "2.{}".format(index_header)
        html_out += temp_header.format(string_index_header, name.replace("RECON_", ""))
        try:
            tmp_items = []
            index = 0
            if isinstance(data_case[name], list):
                for  _ in data_case[name]:
                    index +=1
                    tmp_items.append({
                        "TT": index
                    }
                    )
                    if isinstance(_, dict):
                        tmp_items[-1].update(_)
                    else:
                        tmp_items[-1][name] = json2html.convert(json = _, table_attributes="class=\"table_inbound\"")
           
        except Exception as e:
            print(e)

        try:
            df = pd.DataFrame(data=tmp_items)
           
            df.style.set_properties(subset=['TT'], **{'width': '10'})
            #df.reset_index(drop=True, inplace=True)
            #df.index = df.index + 1
            df = df.to_html(index=False)
            #print(df)
            tmp_table = template_table.format('', df)
            # html_out = html_out + mark_TongHop + tmp_table
            html_out = html_out + tmp_table
        except Exception as e:
            print(e)
    index_header = 0
    html_out = html_out + mark_III
    for name in data_case.keys():
        if not "EXPLOIT_" in name:
            continue
        temp_header = '''<h2>{} {}</h2>'''
        index_header  += 1
        string_index_header  = "3.{}".format(index_header)
        html_out += temp_header.format(string_index_header, name.replace("EXPLOIT_", ""))
        try:
            tmp_items = []
            index = 0
            if isinstance(data_case[name], list):
                for  _ in data_case[name]:
                    index +=1
                    tmp_items.append({
                        "TT": index 
                        })
                    if isinstance(_, dict):
                        #print(convert_html(_))
                        tmp_items[-1].update(convert_html(_))
                    else:
                        tmp_items[-1][name] = convert_html(_)
           
        except Exception as e:
            print("Error", e)

        try:
            df = pd.DataFrame(data=tmp_items)
           
            df.style.set_properties(subset=['TT'], **{'width': '10'})
            #df.reset_index(drop=True, inplace=True)
            #df.index = df.index + 1
            df = df.to_html(index=False)
            #print(df)
            tmp_table = template_table.format('', df)
            # html_out = html_out + mark_TongHop + tmp_table
            html_out = html_out + tmp_table
        except Exception as e:
            print(e)
    
    index_header = 0
    html_out = html_out + mark_IV
    for name in data_case.keys():
        if not "OUTPUT_" in name:
            continue
        temp_header = '''<h2>{} {}</h2>'''
        index_header  += 1
        string_index_header  = "3.{}".format(index_header)
        html_out += temp_header.format(string_index_header, name.replace("OUTPUT_", ""))
        try:
            tmp_items = []
            index = 0
            if isinstance(data_case[name], list):
                for  _ in data_case[name]:
                    index +=1
                    tmp_items.append({
                        "TT": index 
                        })
                    if isinstance(_, dict):
                        #print(convert_html(_))
                        tmp_items[-1].update(convert_html(_))
                    else:
                        tmp_items[-1][name] = convert_html(_)
           
        except Exception as e:
            print("Error", e)

        try:
            df = pd.DataFrame(data=tmp_items)
           
            df.style.set_properties(subset=['TT'], **{'width': '10'})
            #df.reset_index(drop=True, inplace=True)
            #df.index = df.index + 1
            df = df.to_html(index=False)
            #print(df)
            tmp_table = template_table.format('', df)
            # html_out = html_out + mark_TongHop + tmp_table
            html_out = html_out + tmp_table
        except Exception as e:
            print(e)
    html_out = html_out + template_tail


    # create html
    
    folder_data = os.path.abspath(os.path.dirname(__file__)) 
    HTML(string=html.unescape(html_out)).write_pdf(namefile, stylesheets=[folder_data + "/css.css"])


if __name__ == "__main__":
    gen_report_case_from_json(data_case, "./report.pdf")
    
