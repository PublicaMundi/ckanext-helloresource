import json
import logging
from datetime import datetime

from pylons import config

import ckan.model as model
import ckan.plugins as p
import ckan.plugins.toolkit as toolkit
import ckan.lib.helpers as h
from ckan.lib.celery_app import celery
from ckan.lib.dictization.model_dictize import resource_dictize
from ckan.model.types import make_uuid

log1 = logging.getLogger(__name__)

class HelloResourcePlugin(p.SingletonPlugin):
    """Registers to be notified whenever CKAN resources are created or their
    URLs change, and will create a new ckanext.helloresource celery task to
    print a log message.
    """
    
    p.implements(p.IDomainObjectModification, inherit=True)
    p.implements(p.IResourceUrlChange)
    p.implements(p.IRoutes, inherit=True)

    # IDomainObjectModification, IResourceUrlChange

    def notify(self, entity, operation=None):
        log1.info(
            'Received notification on a domain object modification: entity=%r' % (
                entity))
        if not isinstance(entity, model.Resource):
            return
        if operation:
            if operation == model.domain_object.DomainObjectOperation.new:
                self._create_helloresource_task(entity)
        else:
            # if operation is None, resource URL has been changed, as the
            # notify function in IResourceUrlChange accepts 1 parameter
            self._create_helloresource_task(entity)

    # IRoutes

    def before_map(self, mapper):
        
        mapper.connect(
            'helloresource-task-result',
            '/api/helloresource/tasks/{task_id}/result',
            controller='ckanext.helloresource.controllers.greet:GreetController',
            action='get_task_result')
        
        return mapper 

    # Helpers

    def _get_site_url(self):
        try:
            return h.url_for_static('/', qualified=True)
        except AttributeError:
            return config.get('ckan.site_url', '')

    def _create_helloresource_task(self, resource):
        ''' Create the context for the task to run '''

        user = toolkit.get_action('get_site_user')({
            'model': model,
            'ignore_auth': True,
            'defer_commit': True}, {})

        context = {
            'site_url': self._get_site_url(),
            'apikey': user.get('apikey'),
            'site_user_apikey': user.get('apikey'),
            'username': user.get('name'),
        }
        
        context['emulate_long_processing'] = 5 # virtual steps

        resource_dict = resource_dictize(resource, {'model': model})
        
        task_id = make_uuid()
        celery.send_task(
            "helloresource.upload", 
            args=[context, resource_dict], 
            task_id=task_id)

        # The task is queued

        log1.info('Queued a helloresource.upload celery task (%s)' % (task_id))

        # Provide a URL to poll for this task result
        
        result_url = toolkit.url_for(
            'helloresource-task-result', task_id=task_id, qualified=True)
        h.flash('A task has been created, see %s' % (result_url))

