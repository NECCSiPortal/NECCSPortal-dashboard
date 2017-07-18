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

from django.conf import settings


class FixedRegionMiddleware(object):
    """Fixed region from setting middleware"""
    fixed_region_name = getattr(settings, 'FIXED_REGION_NAME', '')
    openstack_keystone_url = getattr(settings, 'OPENSTACK_KEYSTONE_URL', '')

    def process_response(self, request, response):
        if self.fixed_region_name and hasattr(request, 'session'):
            request.session['services_region'] = self.fixed_region_name
            request.session['region_endpoint'] = self.openstack_keystone_url

        return response
