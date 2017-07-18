LOGGING = {
    'version': 1,
    # When set to True this will disable all logging except
    # for loggers specified in this configuration dictionary. Note that
    # if nothing is specified here and disable_existing_loggers is True,
    # django.db.backends will still log unless it is disabled explicitly.
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format': '%(asctime)s %(process)d %(levelname)s %(name)s '
                      '%(message)s'
        },
        'normal': {
            'format': 'dashboard-%(name)s: %(levelname)s %(message)s'
        },
    },
    'handlers': {
        'operation': {
            'level': 'INFO',
            'class': 'logging.FileHandler',
            'filename': '/var/log/horizon/operation/operation.log',
            'formatter': 'verbose',
        },
        'null': {
            'level': 'DEBUG',
            'class': 'django.utils.log.NullHandler',
        },
        'console': {
            # Set the level to "DEBUG" for verbose output logging.
            'level': 'INFO',
            'class': 'logging.StreamHandler',
        },
        'file': {
            'level': 'INFO',
            'class': 'logging.FileHandler',
            'filename': '/var/log/horizon/horizon.log',
            'formatter': 'verbose',
        },
        'syslog': {
            'level': 'INFO',
            'facility': 'local1',
            'class': 'logging.handlers.SysLogHandler',
            'address': '/dev/log',
            'formatter': 'normal',
        }
    },
    'loggers': {
        'horizon.operation_log_middleware.OperationLogMiddleware': {
            'handlers': ['operation'],
            'level': 'INFO',
            'propagate': False,
        },
        'nec_portal': {
            'handlers': ['file'],
            'level': 'INFO',
            'propagate': False,
        },
        # Logging from django.db.backends is VERY verbose, send to null
        # by default.
        'django.db.backends': {
            'handlers': ['null'],
            'propagate': False,
        },
        'requests': {
            'handlers': ['null'],
            'propagate': False,
        },
        'horizon': {
            # 'handlers': ['console'],
            'handlers': ['file'],
            # 'level': 'DEBUG',
            'level': 'INFO',
            'propagate': False,
        },
        'openstack_dashboard': {
            # 'handlers': ['console'],
            'handlers': ['file'],
            # 'level': 'DEBUG',
            'level': 'INFO',
            'propagate': False,
        },
        'novaclient': {
            # 'handlers': ['console'],
            'handlers': ['file'],
            # 'level': 'DEBUG',
            'level': 'INFO',
            'propagate': False,
        },
        'cinderclient': {
            # 'handlers': ['console'],
            'handlers': ['file'],
            # 'level': 'DEBUG',
            'level': 'INFO',
            'propagate': False,
        },
        'keystoneclient': {
            # 'handlers': ['console'],
            'handlers': ['file'],
            # 'level': 'DEBUG',
            'level': 'INFO',
            'propagate': False,
        },
        'glanceclient': {
            # 'handlers': ['console'],
            'handlers': ['file'],
            # 'level': 'DEBUG',
            'level': 'INFO',
            'propagate': False,
        },
        'neutronclient': {
            # 'handlers': ['console'],
            'handlers': ['file'],
            # 'level': 'DEBUG',
            'level': 'INFO',
            'propagate': False,
        },
        'heatclient': {
            # 'handlers': ['console'],
            'handlers': ['file'],
            # 'level': 'DEBUG',
            'level': 'INFO',
            'propagate': False,
        },
        'ceilometerclient': {
            # 'handlers': ['console'],
            'handlers': ['file'],
            # 'level': 'DEBUG',
            'level': 'INFO',
            'propagate': False,
        },
        'troveclient': {
            # 'handlers': ['console'],
            'handlers': ['file'],
            # 'level': 'DEBUG',
            'level': 'INFO',
            'propagate': False,
        },
        'swiftclient': {
            # 'handlers': ['console'],
            'handlers': ['file'],
            # 'level': 'DEBUG',
            'level': 'INFO',
            'propagate': False,
        },
        'openstack_auth': {
            # 'handlers': ['console'],
            'handlers': ['file'],
            # 'level': 'DEBUG',
            'level': 'INFO',
            'propagate': False,
        },
        'nose.plugins.manager': {
            # 'handlers': ['console'],
            'handlers': ['file'],
            # 'level': 'DEBUG',
            'level': 'INFO',
            'propagate': False,
        },
        'django': {
            # 'handlers': ['console'],
            'handlers': ['file'],
            # 'level': 'DEBUG',
            'level': 'INFO',
            'propagate': False,
        },
    }
}

# A value for OperationMiddleware
# OPENSTACK_HORIZON_OPERATION_ENABLED is flag to use OperationMiddleware
# OPENSTACK_HORIZON_OPERATION_MASK_TARGETS is arrangement for appointing
# a target to mask.
# OPENSTACK_HORIZON_OPERATION_METHOD_TARGETS is arrangement of HTTP method
# to output log.
OPENSTACK_HORIZON_OPERATION_ENABLED = True
OPENSTACK_HORIZON_OPERATION_MASK_TARGETS = ['password', 'confirm_admin_pass']
OPENSTACK_HORIZON_OPERATION_METHOD_TARGETS = ['POST', 'GET']

MIDDLEWARE_CLASSES += (
    'horizon.operation_log_middleware.OperationLogMiddleware',
)
