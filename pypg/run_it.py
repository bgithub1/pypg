import sys
qbpython_workspace = sys.argv[1]
py_to_execute = sys.argv[2]
import os

curdir = os.getcwd()
print ("working directory = " + curdir)
subfolders = [
              qbpython_workspace + '/pygmail',
              qbpython_workspace + '/pygmail/examples',
              qbpython_workspace + '/pygmail/gmail',
              qbpython_workspace + '/pypg',
              qbpython_workspace + '/pypg/pypg',
              qbpython_workspace + '/qbapi',
              qbpython_workspace + '/qbapi/qbapi',
            ]
for folder in subfolders:
    sys.path.append(folder)
        

sys.argv = sys.argv[2:]
exec(open(py_to_execute,'r').read())