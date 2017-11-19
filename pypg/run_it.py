import sys
qbpython_workspace = sys.argv[1]
py_to_execute = sys.argv[2]
import os

curdir = os.getcwd()
print "working directory = " + curdir
subfolders = [
              qbpython_workspace + '/attachmentprocessor',
              qbpython_workspace + '/attachmentprocessor/attachmentprocessor',
              qbpython_workspace + '/bai_parse',
              qbpython_workspace + '/bai_parse/bai2',
              qbpython_workspace + '/caponelockbox',
              qbpython_workspace + '/caponelockbox/caponelockbox',
              qbpython_workspace + '/dbqbsync',
              qbpython_workspace + '/dbqbsync/dbqbsync',
              qbpython_workspace + '/dbqbsync/figscripts',
              qbpython_workspace + '/pnclockbox',
              qbpython_workspace + '/pnclockbox/pnclockbox',
              qbpython_workspace + '/pygmail',
              qbpython_workspace + '/pygmail/examples',
              qbpython_workspace + '/pygmail/gmail',
              qbpython_workspace + '/pypostgres',
              qbpython_workspace + '/pypostgres/pypg',
              qbpython_workspace + '/qbpythonapi',
              qbpython_workspace + '/qbpythonapi/qbapi',
            ]
for folder in subfolders:
    sys.path.append(folder)
        

sys.argv = sys.argv[2:]
execfile(py_to_execute)