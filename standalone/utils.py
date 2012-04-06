# Utilies related to portimmo project

# python imports
import sys
import json

# project imports
from portimmo.organization.models import DomainOrganizationModel
from portimmo.language.models import LanguageModel
from portimmo.entity.models import EntityModel
from portimmo.event.models import EventModel
from portimmo.exhibitor.models import ExhibitorModel, ExhibitorTokenModel
from portimmo.country.models import CountryModel, CountryTranslationModel
from portimmo.country.country import Country, CountryTranslation
from standalone.config import SITE_DOMAIN, LANGUAGE_CODE, LOGGER

EVENT_ID = 1

def get_organization(organization_domain=SITE_DOMAIN):
    """ Function to get project domain """
    try :
        organization = DomainOrganizationModel.objects.get(domain__name=organization_domain,is_active=True)
    except Exception, e :
        LOGGER.error('Failed to get organization for domain %s.' % organization_domain + str(e))
        organization = None

    return organization

def get_language(code=LANGUAGE_CODE) :
    """ Fucntion to get project language """

    try :
        language = LanguageModel.objects.get(code=code)
    except Exception, e :
        LOGGER.error('Failed to get language for language code %s.' % code + str(e))
        language = None
        sys.exit(1)

    return language

def get_entity_by_name(name=''):
    """ Function to get entity by name """
    try :
        entity_list = EntityModel.objects.filter(entitytranslationmodel__name__icontains=name,
                is_active=True,is_delete=False)
    except Exception, e :
        LOGGER.error('Failed to get entity for name %s. ' % name + str(e))
        entity_list = []

    return entity_list

def get_event_by_id(organization=None,language=None,event_id=EVENT_ID) :
    """ Function to get event with id """

    try :
        event = EventModel.objects.get(id=event_id,is_active=True,
                event_name__organization=organization)
    except Exception, e :
        LOGGER.error('Failed to get event with id %s. ' % event_id + str(e))
        event = None
        sys.exit(1)
    return event

def get_exhibitor_by_event_n_entity(organization=None,language=None,event=None,entity=None) :
    """ Function to get exhibitor by event and entity """

    status = True
    try :
        exhibitor = ExhibitorModel.objects.get(event=event,entity=entity,
                is_active=True,is_delete=False)
    except Exception, e :
        LOGGER.error('Failed to get Exhibitor. ' + str(e))
        status = False

    return status, exhibitor

def get_token_by_exhibitor(organization=None,language=None,exhibitor=None) :
    """ Function to get exhibitor tokens by exhibitor """
    status = True
    try :
        exhibitor_token = ExhibitorTokenModel.objects.get(exhibitor=exhibitor)
    except Exception, e :
        LOGGER.error('Failed to get exhibitor tokens.' + str(e))
        status = False
        exhibitor_token = None

    return status,exhibitor_token

def add_token_to_exhibitor(organization=None,language=None,exhibitor_token=None,token_range=[]):
    """ Function to add exhibitor_token """

    range_dict = {}
    status = True
    try :
        current_tokens = json.loads(exhibitor_token.tokens)

        for i in token_range :
            for x in range(i[0],i[1]+1) :
                range_dict.update({ x: 0})

        current_tokens = dict( current_tokens.items() + range_dict.items() )
        exhibitor_token.tokens = json.dumps(current_tokens)
        exhibitor_token.save()

    except Exception,e :
        LOGGER.error('Failed to add exhibitor token.' + str(e))
        status = False

    return status

def open_file(file,mode='r'):
    """ Function to open a file """
    status = True
    try :
        file_object = open(file,mode)
    except :
        LOGGER.error('Failed to open File.')
        file_object = None
        status = False

    return status, file_object

def add_country_code(code_list=[]) :
    """ Function to set / add country code in CountryModel """

    country_obj = Country()

    for code in code_list :
        # check if country code already exist
        status ,country = country_obj.get_by_code(data={'country_code':code})

        if not status :
            # save in CountryModel
            country_new_obj = CountryModel()
            country_new_obj.code = code
            country_new_obj.save()

def add_country(language=None,country_dict={}) :
    """ Function used to add country """

    country_obj = Country(language=language)
    country_trans_obj = CountryTranslation()

    for code, country_name in country_dict.items() :
        # check if country code already exist
        status ,country = country_obj.get_by_code(data={'country_code':code})

        if status :
            # check if country traslation with country and language exists
            trans_status, country_trans = country_trans_obj.get_by_country_n_language(data={'language':language,
                'country':country})

            if not trans_status :
                country_trans = CountryTranslationModel()

            country_trans.country = country
            country_trans.language = language
            country_trans.name = country_name
            country_trans.save()

