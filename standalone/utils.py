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
