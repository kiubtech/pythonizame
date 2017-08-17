from pythonizame.apps.website.models import SiteConfiguration


def get_config():
    try:
        config = SiteConfiguration.get_solo()
    except:
        config = None
    return config


def website(request):
    context = {'config': get_config()}
    return context
