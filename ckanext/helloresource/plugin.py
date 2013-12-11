import json
import logging
from datetime import datetime

from pylons import config
from ckan import model
from ckan.model.types import make_uuid
from ckan.plugins import (SingletonPlugin, implements, IDomainObjectModification, IResourceUrlChange, IConfigurable)
from ckan.logic import get_action
from ckan.lib.celery_app import celery
import ckan.lib.helpers as h
from ckan.lib.dictization.model_dictize import resource_dictize

log1 = logging.getLogger(__name__)

class HelloResourcePlugin(SingletonPlugin):
    """
    Registers to be notified whenever CKAN resources are created or their
    URLs change, and will create a new ckanext.helloresource celery task to
    print a log message.
    """
    implements(IDomainObjectModification, inherit=True)
    implements(IResourceUrlChange)

    def notify(self, entity, operation=None):
        log1.info ('Received a notification on a object-modification event (entity=%s)' %(repr(entity)))
        if not isinstance(entity, model.Resource):
            return
        if operation:
            if operation == model.domain_object.DomainObjectOperation.new:
                self._create_helloresource_task(entity)
        else:
            # if operation is None, resource URL has been changed, as the
            # notify function in IResourceUrlChange accepts 1 parameter
            self._create_helloresource_task(entity)

    def _get_site_url(self):
        try:
            return h.url_for_static('/', qualified=True)
        except AttributeError:
            return config.get('ckan.site_url', '')

    def _create_helloresource_task(self, resource):
        ''' Create the context for the task to run '''

        user = get_action('get_site_user')({
            'model': model,
            'ignore_auth': True,
            'defer_commit': True}, {})

        context = json.dumps({
            'site_url': self._get_site_url(),
            'apikey': user.get('apikey'),
            'site_user_apikey': user.get('apikey'),
            'username': user.get('name'),
        })

        data = json.dumps(resource_dictize(resource, {'model': model}))

        task_id = make_uuid()

        celery.send_task ("helloresource.upload", args=[context, data], task_id=task_id)
        log1.info('Sent a helloresource celery task to queue')
