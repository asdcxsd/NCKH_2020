

class MergeData():
    name  = "IN_DOMAIN"
    def merge_data(self, data1, data2):
        data_ans = []
        for i in data1:
            if self.check_duplicate(i,data_ans):
                data_ans.append(i)
        for i in data2:
            if self.check_duplicate(i,data_ans):
                data_ans.append(i)
        return data_ans
    def check_duplicate(self, data1, datas2):
        for index in datas2:
            if (isinstance(index, str) and isinstance(data1, str)):
                if index.lower() == data1.lower():
                    return True
            if index == data1:
                return True
        return False