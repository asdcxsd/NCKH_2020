from subprocess import Popen, PIPE, STDOUT
import os
from os.path import isfile, join
root = "Framework/Library/Reconnaissance/Nuclei/init_tools/nuclei-templates/"
ans = []
ans2 = []
for path, subdirs, files in os.walk(root):
    for name in files:
      if name not in ans:
         ans.append(name)
      else:
         print(name)
      ans2.append(name)
print(len(ans))
print(len(ans2))