import pprint

def pretty(data_struct) :
    """ just a wrapper round the standard python module pprint
    """
    pr = pprint.PrettyPrinter(indent=4)
    return pr.pprint(data_struct)

