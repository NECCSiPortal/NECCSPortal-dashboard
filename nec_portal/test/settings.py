#  Licensed under the Apache License, Version 2.0 (the "License"); you may
#  not use this file except in compliance with the License. You may obtain
#  a copy of the License at
#
#       http://www.apache.org/licenses/LICENSE-2.0
#
#  Unless required by applicable law or agreed to in writing, software
#  distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
#  WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
#  License for the specific language governing permissions and limitations
#  under the License.
#

from horizon.test.settings import *  # noqa
from openstack_dashboard.test.settings import *  # noqa


# Load the pluggable dashboard settings
import openstack_dashboard.enabled
import openstack_dashboard.local.enabled as neccs_portal_enabled
from openstack_dashboard.utils import settings  # noqa


POLICY_FILES_PATH = "/etc/openstack-dashboard/"

NECCS_PORTAL_APPS = list(INSTALLED_APPS) + ['nec_portal']
settings_utils.update_dashboards(
    [
        openstack_dashboard.enabled,
        neccs_portal_enabled,
    ],
    HORIZON_CONFIG,
    NECCS_PORTAL_APPS,
)

NOSE_ARGS = ['--nocapture',
             '--nologcapture',
             '--cover-package=nec_portal',
             '--cover-inclusive',
             '--all-modules']
