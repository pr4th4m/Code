# Connecting / Settings up system path and django settings module

# python imports
import os, sys

# project imports
from standalone.config import PROJECT_PATH, PROJECT_SETTINGS, LOGGER
from standalone.validation import check_path, check_settings


def connect(path=PROJECT_PATH,settings=PROJECT_SETTINGS):
    """ Function to set system path and django settings module """

    # check for empty settings
    check_path(path)
    check_settings(settings)

    try :
        sys.path.append(path)
    except Exception, e :
        LOGGER.error("Failed to set project path in OS sys path. " + str(e))
        sys.exit(1)

    try :
        os.environ['DJANGO_SETTINGS_MODULE'] = settings
    except Exception, e :
        LOGGER.error("Failed to set project settings in OS environment. " + str(e))
        sys.exit(1)

