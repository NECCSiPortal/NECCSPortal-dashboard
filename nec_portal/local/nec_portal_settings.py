from django.utils.translation import ugettext_lazy as _

# dashboard server's root url.
DASHBOARD_SERVER = 'http://localhost:5601'

LOG_MANAGEMENT_GROUP_NAME = _('Log Management')
LINK_GROUP_NAME = _('Link')

# Logging service server's root url
LOGGING_SERVICE_SERVER = 'http://localhost:5601'

# Default retrieval period by a unit on a month for Kibana.
DEFAULT_PERIOD = '1'

# iframe src for admin/history.
# %(start)s : set retrieval start day by views.py
# %(end)s : set retrieval end day by views.py
# %(seach)s : set keyword filter by views.py
ADMIN_HISTORY_FRAME = \
    DASHBOARD_SERVER + "/#/dashboard/portal-history-project?"\
    "embed&_g=(refreshInterval:(display:Off,pause:!f,section:0,value:0),"\
    "time:(from:'%(start)s',mode:absolute,to:'%(end)s'))&_a=(filters:!(),"\
    "panels:!((col:1,id:portal-history-project,row:1,size_x:12,size_y:3,type:"\
    "visualization),(col:1,columns:!(project_name,user_name,operation_type,"\
    "operation_target,operation_message,request_parameter),"\
    "id:portal-history-project,row:4,size_x:12,size_y:5,sort:!('@timestamp',"\
    "desc),type:search)),query:(query_string:(analyze_wildcard:!t,query:"\
    "'*%(search)s')),title:portal-history-project)"

# iframe src for project/history.
# %(start)s : set retrieval start day by views.py
# %(end)s : set retrieval end day by views.py
# %(project_id)s : set project_id filter by views.py
# %(seach)s : set keyword filter by views.py
PROJECT_HISTORY_FRAME = \
    DASHBOARD_SERVER + "/#/dashboard/portal-history-project?"\
    "embed&_g=(refreshInterval:(display:Off,pause:!f,section:0,value:0),"\
    "time:(from:'%(start)s',mode:absolute,to:'%(end)s'))&_a=(filters:!(),"\
    "panels:!((col:1,id:portal-history-project,row:1,size_x:12,size_y:3,type:"\
    "visualization),(col:1,columns:!(project_name,user_name,operation_type,"\
    "operation_target,operation_message,request_parameter),"\
    "id:portal-history-project,row:4,size_x:12,size_y:5,sort:!('@timestamp',"\
    "desc),type:search)),query:(query_string:(analyze_wildcard:!t,query:"\
    "'%(project_id)s%(search)s')),title:portal-history-project)"

# iframe src for admin/log_management.
ADMIN_LOG_MANAGEMENT_FRAME = \
    LOGGING_SERVICE_SERVER + "/#/discover?_g=(refreshInterval:("\
    "display:Off,pause:!f,section:0,value:0),time:(from:now-"\
    + DEFAULT_PERIOD + "M,mode:relative,to:now))&_a=(columns:!(_source),"\
    "index:'portal-*',interval:auto,query:(query_string:("\
    "analyze_wildcard:!t,query:'*')),sort:!('@timestamp',desc))"

CAPACITY_GROUP_NAME = _('Capacity')

NOVA_CAP_ADMIN_ALL_URL = \
    "/#/dashboard/nova-capacity-all?embed&_g=(refreshInterval:(display:Off,"\
    "pause:!f,section:0,value:0),time:(from:now-5M,mode:relative,to:now))&"\
    "_a=(filters:!(),panels:!((col:1,id:Cpu-Usage,row:1,size_x:12,size_y:2,"\
    "type:visualization),(col:1,id:Memory-Usage,row:3,size_x:12,size_y:2,"\
    "type:visualization),(col:1,id:Disk-Usage,row:5,size_x:12,size_y:2,"\
    "type:visualization),(col:1,id:Cpu-Quota,row:7,size_x:12,size_y:2,"\
    "type:visualization),(col:1,id:Memory-Quota,row:9,size_x:12,size_y:2,"\
    "type:visualization)),query:(query_string:(analyze_wildcard:!t,"\
    "query:'%s')),title:nova-capacity-all)"

NOVA_CAP_PROJECT_ALL_URL = \
    "/#/dashboard/nova-capacity-project?embed&_g=(refreshInterval:(display:"\
    "Off,pause:!f,section:0,value:0),time:(from:now-5M,mode:relative,to:now)"\
    ")&_a=(filters:!(),panels:!((col:1,id:Cpu-Usage,row:1,size_x:12,"\
    "size_y:2,type:visualization),(col:1,id:Memory-Usage,row:3,size_x:12,"\
    "size_y:2,type:visualization),(col:1,id:Disk-Usage,row:5,size_x:12,"\
    "size_y:2,type:visualization)),query:(query_string:(analyze_wildcard:"\
    "!t,query:'%s')),title:nova-capacity-project)"

NOVA_CAP_COMMON_URL = \
    "/#/dashboard/nova-capacity-project?embed&_g=(refreshInterval:(display:"\
    "Off,pause:!f,section:0,value:0),time:(from:now-4M,mode:relative,to:now)"\
    ")&_a=(filters:!(),panels:!((col:1,id:Cpu-Usage,row:1,size_x:12,"\
    "size_y:2,type:visualization),(col:1,id:Memory-Usage,row:3,size_x:12,"\
    "size_y:2,type:visualization),(col:1,id:Disk-Usage,row:5,size_x:12,"\
    "size_y:2,type:visualization)),query:(query_string:(analyze_wildcard:"\
    "!t,query:'%s')),title:nova-capacity-project)"

# Admin links list.
# NOTE: If you want to add an external link,
# please add the specified name description and url.
#   name: Specifies the name of the external link.
#   description: Specifies the description of the external link.
#   url: Specifies the URL of the external link.
# If you want to multi language display,
#   please add the name and description values to 'po' files.
ADMIN_LINKS = [
    {
        'name': _('repository'),
        'description': _('Do centralized management of resource files.'),
        'url': 'https://localhost',
    },
]

# Project links list.
# NOTE: If you want to add an external link,
# please add the specified name description and url.
#   name: Specifies the name of the external link.
#   description: Specifies the description of the external link.
#   url: Specifies the URL of the external link.
# If you want to multi language display,
#   please add the name and description values to 'po' files.
PROJECT_LINKS = [
]
