#!/usr/bin/env python

# Module providing utilities for printing stuff
import pprint

def pretty(data_struct) :
    """ just a wrapper round the standard python module pprint
    Args : Data Structure
    Returns : pprint Data Structure
    """
    pr = pprint.PrettyPrinter(indent=4)
    return pr.pprint(data_struct)
