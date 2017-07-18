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

from django.utils.translation import ugettext_lazy as _

from horizon import exceptions

from openstack_dashboard.api import nova

AZ_GROUP_NAME = 'az'
HOST_GROUP_NAME = 'host'


class CapacityResources(object):

    def get_az_context(self, request, detail_base='./detail'):
        context = {}

        try:
            az_list = nova.novaclient(request).availability_zones.list()
            context['az_list'] = [az.zoneName for az in az_list
                                  if az.zoneName != 'internal']
        except Exception:
            az_list = []
            context['az_list'] = []
            exceptions.handle(request,
                              _('Unable to retrieve availability zones.'))

        context.update(
            self.get_common_context(
                request, detail_base, context['az_list'],
                AZ_GROUP_NAME))
        return context

    def get_host_context(self, request, detail_base='./detail'):
        context = {}

        try:
            hypervisor_list = nova.novaclient(request).hypervisors.list()
            context['host_list'] = [hypervisor.hypervisor_hostname
                                    for hypervisor in hypervisor_list]
        except Exception:
            hypervisor_list = []
            context['host_list'] = []
            exceptions.handle(request,
                              _('Unable to retrieve hosts.'))

        context.update(
            self.get_common_context(
                request, detail_base, context['host_list'],
                HOST_GROUP_NAME))
        return context

    def get_common_context(self, request, detail_base, target_list,
                           default_group):
        group = request.GET.get('group', '')
        name = request.GET.get('name', '')

        default_name = (target_list[0] if len(target_list) > 0 else '')

        if name:
            if name not in target_list:
                name = default_name
        else:
            name = default_name

        if not group:
            group = default_group
            name = default_name
        elif not group == default_group:
            group = default_group
            name = default_name

        common_context = {
            'detail_url': detail_base + '?group=' + group + '&name=' + name,
            'name': name,
        }

        return common_context
