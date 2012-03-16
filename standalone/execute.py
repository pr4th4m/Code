# Main file from where the script starts

# python imports
import sys
import os

# set current path in sys path
try :
    sys.path.append(os.path.abspath(os.path.join(os.getcwd(),os.path.pardir)))
except Exception, e :
    print("Failed to set standalone in system path. " + str(e))

# project imports
from standalone.config import PROJECT_PATH, PROJECT_SETTINGS
from standalone.connection import connect
from standalone.args import args_one

# make connection, set path and settings for project
connect(path=PROJECT_PATH, settings=PROJECT_SETTINGS)

# check for function name in args element one
args_one(sys.argv)
