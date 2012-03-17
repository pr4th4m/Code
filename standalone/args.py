# File to validate all the parameters which are passed on terminal (args)

# python imports
import sys
import inspect
from types import ListType, TupleType, IntType

# project imports
from standalone.config import LOGGER


def args_one(args_list):
    """ Function to validate element one of args """
    function_counter = 0
    request_function = None

    # get element one
    try :
        one = args_list[1]
    except Exception, e :
        LOGGER.info('Please provide a function name.')
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
    else :
        request_function = standalone.script.__dict__[one]

    return request_function

def args_two(args_list):
    """ Function to return element two of sys args """

    status = True
    try :
        two = args_list[2]
    except Exception, e :
        LOGGER.error('Failed to get element 2 for sys args')
        two = ''
        status = False

    return status, two

def args_three(args_list):
    """ Function to return element three of sys args """

    status = True
    try :
        three = args_list[3]
    except Exception, e :
        LOGGER.error('Failed to get element 3 for sys args')
        three = ''
        status = False

    return status, three

def check_option(option):
    """ Function to check if give option is as per python standards """
    status = True
    try :
        request_option = eval(option)
    except Exception, e :
        LOGGER.error('Failed to covert to Python standards.')
        status = False
        request_option = []
    return status, request_option

def check_format(option):
    """ Function to check format """

    status = True
    try :
        if not isinstance(option,ListType) :
            status = False

        for tup in option :
            if not isinstance(tup,TupleType):
                status = False
            if not isinstance(tup[0],IntType) or not isinstance(tup[1],IntType) :
                status = False

    except Exception, e:
        LOGGER.error('Formatting error.')
        status = False
        request_option = []

    return status

def check_number(option):
    """ Function to check ranges """
    status = True
    try :
        for tup in option :
            if not len(tup) == 2 :
                status = False
            if tup[0] > tup[1] :
                status = False
    except Exception, e :
        LOGGER.error('Token Ranges not proper.')
        status = False

    return status
