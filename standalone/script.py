# File to hold all the script functions
# NOTE : This file is specific to only one project

# python imports
import sys
import json

# project imports
from standalone.utils import get_organization, get_language, get_entity_by_name, get_event_by_id, \
        get_exhibitor_by_event_n_entity, get_token_by_exhibitor, add_token_to_exhibitor, open_file, \
        add_country_code, add_country
from standalone.args import args_two, args_three, check_option, check_format, check_number
from standalone.config import LOGGER


def set_token():
    """ Function to set tokens for an exhibitor """

    # get organization
    organization = get_organization()

    # get language
    language = get_language()

    # get args ( element two )
    status, entity_name = args_two(sys.argv)
    if not status :
        LOGGER.info("Please provide Entity/Exhibitor Name.")
        sys.exit(1)

    # get args ( element three )
    status, token_range = args_three(sys.argv)
    if not status :
        LOGGER.info("Please provide token range.")
        sys.exit(1)

    # check for option standards
    option_status, token_range = check_option(token_range)
    if not option_status :
        LOGGER.info("Please provide option as per Python standards.")
        sys.exit(1)

    # check for option format
    format_status  = check_format(token_range)
    if not format_status :
        LOGGER.info("Please Provide Proper Format ex:'[(100,200),(500,800)]'.")
        sys.exit(1)

    # check for option format
    number_status  = check_number(token_range)
    if not number_status :
        LOGGER.info("Please Provide proper ranges ex:'[(100,200),(500,800)]'.")
        sys.exit(1)

    # get entity list
    entity_list = get_entity_by_name(name=entity_name)

    # check for empty list
    if not entity_list :
        LOGGER.info("Entity/Exhibitor with name %s does not exist" %entity_name)
        sys.exit(1)

    # check for multiple exhibitors
    if len(entity_list) > 1 :
        counter = 0
        # get entity values
        entity_values_list = entity_list.values('id','entitytranslationmodel__name')

        print("Please select appropriate entity")
        for v in entity_values_list :
            print(str(counter) + ".ID: " + str(v['id']) + "  " + "Name :" + v['entitytranslationmodel__name'])
            counter = counter + 1

        print("Type 'exit' or 'e' to quit")
        while True :
            request_entity = raw_input("Please select an option:")

            if str(request_entity).lower() == 'exit' or str(request_entity).lower() == 'e' :
                sys.exit(1)

            try :
                if int(request_entity) < len(entity_list) and int(request_entity) >= 0 :
                    break
                else :
                    LOGGER.info("Wrong option selected")
            except Exception, e :
                LOGGER.info("Wrong option selected")

        entity = entity_list[int(request_entity)]
    else :
        entity = entity_list[0]

    # get event
    event = get_event_by_id(organization=organization,language=language)

    # get exhibitor
    exhibitor_status, exhibitor = get_exhibitor_by_event_n_entity(organization=organization,language=language,
            event=event,entity=entity)

    # check exhibitor status
    if not exhibitor_status :
        LOGGER.info('Exhibitor for Event %s and Entity %s does not exist.' % (event,entity))
        sys.exit(1)


    # get exhibitor tokens
    exhibitor_token_status, exhibitor_token = get_token_by_exhibitor(organization=organization,language=language,
            exhibitor=exhibitor)

    # check exhibitor token status
    if not exhibitor_token_status :
        LOGGER.info('Exhibitor Token for Event %s and Entity %s does not exist.' % (event,entity))
        sys.exit(1)

    # add token to exhibitor
    token_status = add_token_to_exhibitor(organization=organization,language=language,
            exhibitor_token=exhibitor_token,token_range=token_range)

    # check exhibitor token status
    if not token_status :
        LOGGER.info('Failed to add token for Exhibitor %s.' % (exhibitor))
        sys.exit(1)

    LOGGER.info('Congratulations! Tokens added successfully.')

def set_country_code() :
    """ Function to set country code """


    # get args ( element two )
    status, country_code_file = args_two(sys.argv)
    if not status :
        LOGGER.info("Please provide Country Code file.")
        LOGGER.info("Usage : python execute set_country_code <CountryCodeFile>.")
        sys.exit(1)


    # open the given file
    status, file = open_file(country_code_file)
    if not status :
        LOGGER.info('Please check file location.')
        sys.exit(1)

    # read content
    country_list = file.read()

    # load json format
    country_list = json.loads(country_list)

    # get country code list
    country_code_list = [ k for k in country_list ]

    # add country code to CountryModel
    add_country_code(code_list=country_code_list)

    LOGGER.info('Congratulations! Country Code added successfully.')

def set_country():
    """ Function used to set country """


    # get args ( element two )
    status, language_code = args_two(sys.argv)
    if not status :
        LOGGER.info("Please provide Language Code.")
        LOGGER.info("Usage : python execute set_country <LanguageCode> <CountryCodeFile>.")
        sys.exit(1)

    # get args ( element three )
    status, country_file = args_three(sys.argv)
    if not status :
        LOGGER.info("Please provide Country file.")
        LOGGER.info("Usage : python execute set_country <LanguageCode> <CountryCodeFile>.")
        sys.exit(1)


    # get language
    language = get_language(code=language_code)

    # open the given file
    status, file = open_file(country_file)
    if not status :
        LOGGER.info('Please check file location.')
        sys.exit(1)

    # read content
    country_list = file.read()

    # load json format
    country_list = json.loads(country_list)

    # add country to CountryTranslationModel
    add_country(language=language,country_dict=country_list)

    LOGGER.info('Congratulations! Countries added successfully.')
