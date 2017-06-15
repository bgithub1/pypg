import sys
qbpython_workpace = sys.argv[1]
py_to_execute = sys.argv[2]
import os

curdir = os.getcwd()
print "working directory = " + curdir
subfolders = [
              qbpython_workpace + '/attachmentprocessor',
              qbpython_workpace + '/attachmentprocessor/attachmentprocessor',
              qbpython_workpace + '/bai_parse',
              qbpython_workpace + '/bai_parse/bai2',
              qbpython_workpace + '/caponelockbox',
              qbpython_workpace + '/caponelockbox/caponelockbox',
              qbpython_workpace + '/dbqbsync',
              qbpython_workpace + '/dbqbsync/dbqbsync',
              qbpython_workpace + '/dbqbsync/figscripts',
              qbpython_workpace + '/pnclockbox',
              qbpython_workpace + '/pnclockbox/pnclockbox',
              qbpython_workpace + '/pygmail',
              qbpython_workpace + '/pygmail/examples',
              qbpython_workpace + '/pygmail/gmail',
              qbpython_workpace + '/pypostgres',
              qbpython_workpace + '/pypostgres/pypg',
              qbpython_workpace + '/qbpythonapi',
              qbpython_workpace + '/qbpythonapi/qbapi',
            ]
for folder in subfolders:
    sys.path.append(folder)
        

sys.argv = sys.argv[2:]
execfile(py_to_execute)