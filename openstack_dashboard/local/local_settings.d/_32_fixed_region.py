from django.contrib import auth
from django.contrib.auth import models
from openstack_auth import utils

# Please set the region name to be fixed.
# If it is empty, it will not be fixed.
FIXED_REGION_NAME = ''


def get_user_fixed_region(request):
    try:
        user_id = request.session[auth.SESSION_KEY]
        backend_path = request.session[auth.BACKEND_SESSION_KEY]
        backend = auth.load_backend(backend_path)
        backend.request = request
        user = backend.get_user(user_id) or models.AnonymousUser()
    except KeyError:
        user = models.AnonymousUser()
    finally:
        if FIXED_REGION_NAME:
            user.endpoint = OPENSTACK_KEYSTONE_URL
            user._services_region = FIXED_REGION_NAME
    return user


utils.get_user = get_user_fixed_region
