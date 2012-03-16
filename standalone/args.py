# File to validate all the parameters which are passed on terminal (args)

# python imports
import sys
import inspect

# project imports
from standalone.config import LOGGER


def args_one(args_list):
    """ Function to validate element one of args """
    import ipdb
    ipdb.set_trace()
    function_counter = 0

    # get element one
    try :
        one = args_list[1]
    except Exception, e :
        LOGGER.info('Please provide a fucntion name.')
        sys.exit(1)

    # get attr for module
    import standalone.script
    attr = dir(standalone.script)

    if one not in attr :
        LOGGER.info('%s is not defined.' % one )
        sys.exit(1)

    if not inspect.isfunction(standalone.script.__dict__[one]) :
        LOGGER.info('%s is not a valid Function.' % one )
        sys.exit(1)
