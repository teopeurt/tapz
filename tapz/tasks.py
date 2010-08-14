from celery.decorators import task
from tapz.site import site

@task
def add_event(event_type, info):
    panel = site.get_panel(event_type).add_event(info)
