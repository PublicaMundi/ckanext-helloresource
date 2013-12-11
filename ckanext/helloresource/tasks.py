import json
import requests

from ckan.lib.celery_app import celery

@celery.task(name="helloresource.upload")
def helloresource_upload(context, data):
    logger = helloresource_upload.get_logger()
    try:
        data = json.loads(data)
        context = json.loads(context)
        logger.info ('Received uploaded resource: data=%s' %(repr(data)))
        return 'Hello Resource'
    except Exception as e:
        pass


