from tapz.site import site

@task
def track_exception(panel_title, info):
    panel = site.get_panel(panel_title).add_event(info)
