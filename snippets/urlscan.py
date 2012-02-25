#!/usr/bin/env python
'''
Utility to provide the function name when url given or vice versa
Depends on django_extensions, it should be in your installed apps
Curretly the color code does not work
NOTE : this file should be in your django project directory i.e the project root directory
'''
import subprocess
import ipdb
import sys
import os

def match_url(current_path, search_string):
    """ fucntion used the match url with given string
    """
    #open subprocess with Popen, to run this command django_extensions should be installed in your settings file
    p = subprocess.Popen(["python",current_path,"show_urls"],stdout=subprocess.PIPE)
    data , errors = p.communicate()
    splited_urls = [ url.split('\t') for url in data.split('\n') ]

    pattern_list = []
    # match the url list with the give search string
    # ipdb.set_trace()
    [ pattern_list.append(pattern) for pattern in splited_urls for pat in pattern  if pat.find(search_string) != -1
            if pattern not in pattern_list ]

    # finally print the output
    print "Possible Matches"
    print "\n".join( k+"\t"+v for k,v,p in pattern_list)

# search for parameters passed else raise error and exit
try :
    search_string = sys.argv[1]
    current_path = os.getcwd() + "/manage.py"
    match_url(current_path, search_string)
except :
    print "Usage : python du.py search_string"
    sys.exit()
