import time

from ckan.lib.celery_app import celery

@celery.task(name="helloresource.upload")
def helloresource_upload(context, resource_dict):
    logger = helloresource_upload.get_logger()
    logger.info(
        'Received uploaded resource: resource=%r, context=%r' % (
            resource_dict, context))
    
    if 'emulate_long_processing' in context:
        logger.info('Will emulate a long running process')
        n = int(context['emulate_long_processing'])
        for i in range(0, n):
            time.sleep(5)
            logger.info('Working at %d/%d ...' % (i + 1, n))
    
    return {
        'greeting': 'Hello Resource!',
        'resource_name': resource_dict['name']
    }


