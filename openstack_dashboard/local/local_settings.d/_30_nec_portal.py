# A list of applications to be added to INSTALLED_APPS.
ADD_INSTALLED_APPS = ['nec_portal']

AVAILABLE_THEMES = [
    ('nec_portal', 'NEC_Portal', 'themes/nec_portal'),
]
DEFAULT_THEME = 'nec_portal'

# Site Branding
SITE_BRANDING = 'NEC Cloud System'

# NECCS Support Format
OPENSTACK_IMAGE_BACKEND = {
    'image_formats': [
        ('', _('Select format')),
        ('qcow2', _('QCOW2 - QEMU Emulator')),
        ('raw', _('Raw')),
    ]
}

POLICY_FILES = {
    'ticket': 'aflo_policy.json',
    'identity': 'keystone_policy.json',
    'compute': 'nova_policy.json',
    'volume': 'cinder_policy.json',
    'image': 'glance_policy.json',
    'orchestration': 'heat_policy.json',
    'network': 'neutron_policy.json',
    'telemetry': 'ceilometer_policy.json',
}

MESSAGE_STORAGE = 'django.contrib.messages.storage.session.SessionStorage'
