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

from horizon import tabs

from nec_portal.dashboards.admin.capacity import resources\
    as capacity_resources
from nec_portal.dashboards.admin.capacity import tables as capacity_tables


class CapacityTab(tabs.TableTab):
    name = _("Whole system")
    slug = "capacity"
    template_name = "admin/capacity/capacity/_index.html"
    table_classes = (capacity_tables.CapacityTable,)
    preload = False
    attr = {'data-loaded': 'false'}

    def get_capacity_data(self):
        return []

    def get_context_data(self, request):
        context = {
            'detail_url': './capacity/detail',
        }

        return context


class CapacityAZTab(tabs.TableTab):
    name = _("Availability zones")
    slug = "capacity_az"
    template_name = "admin/capacity/capacity_az/_index.html"
    table_classes = (capacity_tables.CapacityAZTable,)
    preload = False

    GROUP_NAME = 'az'

    def get_capacity_az_data(self):
        return []

    def get_context_data(self, request):
        return capacity_resources.CapacityResources()\
                                 .get_az_context(self.request,
                                                 './capacity_az/detail')


class CapacityHostTab(tabs.TableTab):
    name = _("Host")
    slug = "capacity_host"
    template_name = "admin/capacity/capacity_host/_index.html"
    table_classes = (capacity_tables.CapacityHostTable,)
    preload = False

    GROUP_NAME = 'host'

    def get_capacity_host_data(self):
        return []

    def get_context_data(self, request):
        return capacity_resources.CapacityResources()\
                                 .get_host_context(self.request,
                                                   './capacity_host/detail')


class CapacityGroupTabs(tabs.TabGroup):
    slug = "capacity_group_tabs"
    tabs = (CapacityTab, CapacityAZTab, CapacityHostTab)
    sticky = True
