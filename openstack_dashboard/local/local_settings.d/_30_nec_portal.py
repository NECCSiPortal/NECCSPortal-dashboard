# A list of applications to be added to INSTALLED_APPS.
ADD_INSTALLED_APPS = ['nec_portal']

# 'key', 'label', 'path'
AVAILABLE_THEMES = [
    ('nec_portal', 'NEC_Portal', 'themes/nec_portal'),
]

# The default theme if no cookie is present
DEFAULT_THEME = 'nec_portal'

# Site Branding
SITE_BRANDING = 'NEC Cloud System'

# WEBROOT is the location relative to Webserver root
# should end with a slash.
WEBROOT = '/dashboard/'

# The OPENSTACK_IMAGE_BACKEND settings can be used to customize features
# in the OpenStack Dashboard related to the Image service, such as the list
# of supported image formats.
OPENSTACK_IMAGE_BACKEND = {
    'image_formats': [
        ('', _('Select format')),
        ('qcow2', _('QCOW2 - QEMU Emulator')),
        ('raw', _('Raw')),
    ]
}

# Dictionary of currently available angular features
ANGULAR_FEATURES = {
    'images_panel': False,
}

# Map of local copy of service policy files
POLICY_FILES = {
    'identity': 'keystone_policy.json',
    'ticket': 'aflo_policy.json',
    'compute': 'nova_policy.json',
    'volume': 'cinder_policy.json',
    'image': 'glance_policy.json',
    'orchestration': 'heat_policy.json',
    'network': 'neutron_policy.json',
    'telemetry': 'ceilometer_policy.json',
}

MESSAGE_STORAGE = 'django.contrib.messages.storage.session.SessionStorage'

# Overrides the default domain used when running on single-domain model
# with Keystone V3. All entities will be created in the default domain.
# NOTE: This value must be the ID of the default domain, NOT the name.
# Also, you will most likely have a value in the keystone policy file like this
#    "cloud_admin": "rule:admin_required and domain_id:<your domain id>"
# This value must match the domain id specified there.
OPENSTACK_KEYSTONE_DEFAULT_DOMAIN = 'default'

# Default OpenStack Dashboard configuration.
HORIZON_CONFIG['help_url'] = "http://help.example.com"

SECRET_KEY='xxxx'
LOCAL_PATH = '/tmp'

# We recommend you use memcached for development; otherwise after every reload
# of the django development server, you will have to login again. To use
# memcached set CACHES to something like
CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.memcached.MemcachedCache',
        'LOCATION': 'localhost.example.com:11211',
    }
}

OPENSTACK_HOST = "127.0.0.1"
OPENSTACK_KEYSTONE_URL = "http://127.0.0.1:5000/v3"
OPENSTACK_KEYSTONE_DEFAULT_ROLE = "_member_"

# Overrides for OpenStack API versions. Use this setting to force the
# OpenStack dashboard to use a specific API version for a given service API.
# Versions specified here should be integers or floats, not strings.
# NOTE: The version should be formatted as it appears in the URL for the
# service API. For example, The identity service APIs have inconsistent
# use of the decimal point, so valid options would be 2.0 or 3.
# Minimum compute version to get the instance locked status is 2.9.
OPENSTACK_API_VERSIONS = {
  "identity": 3
}

# A dictionary of settings which can be used to provide the default values for
# properties found in the Launch Instance modal.
LAUNCH_INSTANCE_DEFAULTS = {
    'config_drive': True,
    'enable_scheduler_hints': True,
    'disable_image': True,
    'disable_instance_snapshot': True,
    'disable_volume': False,
    'disable_volume_snapshot': True,
}

# The OPENSTACK_CINDER_FEATURES settings can be used to enable optional
# services provided by cinder that is not exposed by its extension API.
OPENSTACK_CINDER_FEATURES = {
    'enable_backup': True,
}

# The OPENSTACK_NEUTRON_NETWORK settings can be used to enable optional
# services provided by neutron. Options currently available are load
# balancer service, security groups, quotas, VPN service.
OPENSTACK_NEUTRON_NETWORK = {
    'enable_router': True,
    'enable_quotas': True,
    'enable_ipv6': True,
    'enable_distributed_router': False,
    'enable_ha_router': False,
    'enable_lb': True,
    'enable_firewall': False,
    'enable_vpn': False,
    'enable_fip_topology_check': True,

    # The profile_support option is used to detect if an external router can be
    # configured via the dashboard. When using specific plugins the
    # profile_support can be turned on if needed.
    'profile_support': None,
    #'profile_support': 'cisco',

    # Set which provider network types are supported. Only the network types
    # in this list will be available to choose from when creating a network.
    # Network types include local, flat, vlan, gre, and vxlan.
    'supported_provider_types': ['*'],

    # Set which VNIC types are supported for port binding. Only the VNIC
    # types in this list will be available to choose from when creating a
    # port.
    # VNIC types include 'normal', 'macvtap' and 'direct'.
    'supported_vnic_types': ['*']
}

# OPENSTACK_ENDPOINT_TYPE specifies the endpoint type to use for the endpoints
# in the Keystone service catalog. Use this setting when Horizon is running
# external to the OpenStack environment. The default is 'publicURL'.
OPENSTACK_ENDPOINT_TYPE = "internalURL"

# Specify a maximum number of items to display in a dropdown.
DROPDOWN_MAX_ITEMS = 1000

SESSION_ENGINE = 'django.contrib.sessions.backends.cache'
SESSION_COOKIE_DOMAIN = ".example.com"


# Override policy.check function.
# Admin dashboard menu disabled by only admin roles.
# Setting of OPENSTACK_KEYSTONE_ADMIN_ROLES is necessary
# to use this method.
def check(actions, request, target=None):
    import inspect
    from horizon import Dashboard as dashboard
    frame = None

    try:
        # Get a caller frame
        frame = inspect.stack()[2][0]
        arginfo = inspect.getargvalues(frame)
        called_obj = arginfo.locals['self'] if 'self' in arginfo.locals else None

        # Check calld class is dashboard
        if called_obj and isinstance(called_obj, dashboard):
            roles = request.user.roles
            role_name_list = [role['name'] for role in request.user.roles]
            my_roles = set(role_name_list)
            admin_roles = set(OPENSTACK_KEYSTONE_ADMIN_ROLES)

            return 0 < len(my_roles & admin_roles)
    finally:
        if frame: del frame

    # Note(Itxaka): This is to prevent circular dependencies and apps not ready
    # If you do django imports in your settings, you are gonna have a bad time
    from openstack_auth import policy
    return policy.check(actions, request, target)


OPENSTACK_KEYSTONE_ADMIN_ROLES = [
    'admin'
]
POLICY_CHECK_FUNCTION = check
