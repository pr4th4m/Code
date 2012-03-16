# Validation for standalone scripts

# python imports
import sys

# project imports
from standalone.config import LOGGER

def check_path(path):
    """ Function to check it project path and project settings are empty """

    if not path :
        LOGGER.info("Please define project path in config.py .")
        sys.exit(1)


def check_settings(settings):
    """ Function to check if project settings are sepecified """

    if not settings :
        LOGGER.info("Please define project settings in config.py .")
        sys.exit(1)
