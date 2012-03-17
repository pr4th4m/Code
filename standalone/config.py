# Configuration file for Django standalone scripts

# python imports
import os


# set django project path ( complete path till project directory )
PROJECT_PATH = '/home/pratz/www/portimmo/trunk/code/portimmo'

# set django project settings file
PROJECT_SETTINGS = 'portimmo.settings'

# set domain
SITE_DOMAIN = 'portimmo.com'

# set language
LANGUAGE_CODE = 'en'

# get base / current directory
BASE_DIR = os.path.abspath(os.getcwd())


# Logger settings
import logging
import dictconfig
LOGGING = {
        'version': 1,
        'disable_existing_loggers': False,
        'formatters': {
            'verbose': {
                'format': '%(levelname)s %(asctime)s %(module)s %(process)d %(thread)d %(message)s'
                },
            'simple': {
                'format': '%(levelname)s %(message)s'
                },
            'detailed': {
                # 'class':'IPython.ColorANSI.TermColors',
                'format': '%(asctime)-8s %(module)-8s line:%(lineno)-4d ' \
                        '%(levelname)-8s %(message)s',
                        },
            },
        'filters': {
            },
        'handlers': {
            'console':{
                'level':'DEBUG',
                'class':'logging.StreamHandler',
                'formatter': 'simple'
                },
            'file': {
                'class': 'logging.handlers.RotatingFileHandler',
                'level': 'ERROR',
                'formatter': 'detailed',
                'filename': BASE_DIR + '/logs/standalone.log',
                'mode': 'a',
                'maxBytes': 10485760,
                'backupCount': 5,
                },
            },
        'loggers': {
            'standalone': {
                'handlers':['console','file'],
                'propagate': True,
                'level':'DEBUG',
                },
            }
        }


# assign it to logging dictconfig
dictconfig.dictConfig(LOGGING)

# get root logger
LOGGER = logging.getLogger('standalone')
