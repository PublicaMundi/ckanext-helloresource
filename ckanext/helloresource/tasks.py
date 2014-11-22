import json
import requests

from ckan.lib.celery_app import celery

@celery.task(name="helloresource.upload")
def helloresource_upload(context, data):
    logger = helloresource_upload.get_logger()
    logger.info(
        'Received uploaded resource: data=%r, context=%r' % (data, context))
    return 'Hello Resource!'


