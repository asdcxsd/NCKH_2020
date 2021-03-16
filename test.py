from subprocess import Popen, PIPE, STDOUT
def mergeDict(dict1, dict2):
      
   dict3 = {**dict1, **dict2}
   for key, value in dict3.items():
       if key in dict1 and key in dict2:
               dict3[key] = list(set(value + dict1[key]))
   return dict3
a = {'a': [1,2,3]}
b = {'a': [1, 4,5,6]}
c = mergeDict(a,b)
print(c)
