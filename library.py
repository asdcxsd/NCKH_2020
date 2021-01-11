def mergeDict(dict1, dict2):
      
    dict3 = {**dict1, **dict2}
    for key, value in dict3.items():
       if key in dict1 and key in dict2:
            try:
                dict3[key] = list(set(value + dict1[key]))
            except:
                dict3[key]  = mergeDict(value, dict1[key])
    return dict3