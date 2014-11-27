import time
import random

from ckan.lib.celery_app import celery

def raise_at_random(p=0.5):
    r = random.random()
    if r < p:
        raise Exception('Bad luck')

@celery.task(name='helloresource.upload', max_retries=3, default_retry_delay=30)
def helloresource_upload(context, resource_dict):
    logger = helloresource_upload.get_logger()
    logger.info(
        'Processing uploaded resource: resource=%r, context=%r' % (
            resource_dict, context))

    emulate_long_process = context.get('emulate_long_process')
    emulate_retried_failure = context.get('emulate_retried_failure')
    
    if emulate_retried_failure:
        try:
            raise_at_random(0.9)
        except Exception as e:
            context['emulate_retried_failure'] = False # dont repeat it
            logger.warning('Failed (%s) but willing to retry' % (e))
            helloresource_upload.retry(exc=e)
        
    if emulate_long_process:
        logger.info('Will emulate a long running process')
        n = int(emulate_long_process)
        for i in range(0, n):
            time.sleep(5)
            logger.info('Working at %d/%d ...' % (i + 1, n))
    
    return {
        'greeting': 'Hello Resource!',
        'resource_name': resource_dict['name']
    }


