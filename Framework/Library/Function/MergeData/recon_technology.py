
import string
class MergeData():
    name  = "RECON_TECHNOLOGY"
    def merge_data(self, data1, data2):
        data_ans = []
        for i in data1:
            status, index = self.check_duplicate_and_update(i,data_ans)
            if status == False:
                data_ans.append(i)
            elif status == 2:
                data_ans[index] = i
        for i in data2:
            status, index = self.check_duplicate_and_update(i,data_ans)
            if status == False:
                data_ans.append(i)
            elif status == 2:
                data_ans[index] = i
        return data_ans
    def check_duplicate_default(self, data1, datas2):
        for index in datas2:
            if (isinstance(index, str) and isinstance(data1, str)):
                if index.lower() == data1.lower():
                    return True
            if index == data1:
                return True
        return False

    def check_duplicate_and_update(self, data1, datas2):
        for index, tech in enumerate(datas2):
            try:
                if self.compare_string_name(tech['name'] , data1['name']) and tech['port'] ==  data1['port']:
                    if tech['version'] ==  data1['version']:
                        return 1 , 0
                    if ("version" not in tech or tech['version'] == "" or tech['version'] == None) and   data1['version'] != "":
                        return 2, index
                    
                    if (data1['version'] == '' and tech['version'] != ''):
                        return 1, 0

            except Exception as e:
                print("Error output nuclei", e)
        return False , 0

    def compare_string_name(self, string1, string2):
        string1 = string1.lower()
        string2 = string2.lower()
        if (len(string1) != len(string2)):
            return False
        for i in range(len(string1)):
            if string1[i] in  string.ascii_letters + string.digits and string1[i] != string2[i]:
                return False
        return True 
