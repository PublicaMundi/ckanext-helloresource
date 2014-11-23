import json

from ckan.lib.base import (
    c, BaseController, render, abort, redirect, request, response)
import ckan.model as model
import ckan.plugins.toolkit as toolkit
import ckan.lib.helpers as h
from ckan.lib.celery_app import celery

_ = toolkit._

class GreetController(BaseController):
    '''Demonstrate a request for an asynchronous result being processed in
    Celery queue.
    '''

    def get_task_result(self, task_id):
        rep = {}

        res = celery.AsyncResult(task_id=task_id)
        rep = { 
            'task_name': res.task_name,
            'task_id': res.task_id,
            'state': res.state,
            'status': res.status,
        }
        if res.ready():
            rep['result'] = res.result
        
        response.headers['Content-Type'] = 'application/json'
        return [json.dumps(rep)]

