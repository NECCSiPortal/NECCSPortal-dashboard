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

"""
Views for Links.
"""

from django.utils.translation import ugettext_lazy as _

from horizon import tables

from nec_portal.dashboards.admin.links import tables as links_tables
from nec_portal.local import nec_portal_settings
from openstack_auth import utils as auth_utils


class IndexView(tables.DataTableView):
    table_class = links_tables.LinksTable
    template_name = 'admin/links/index.html'
    page_title = _('Links')

    def get_data(self):
        return None

    def get_context_data(self, **kwargs):
        context = super(IndexView, self).get_context_data(**kwargs)
        context['link_list'] = []

        roles = self._get_user_roles()
        link_list = self._get_admin_links()

        for link in link_list:

            if 'role' not in link:
                context['link_list'].append(
                    self._create_link(link))
                continue

            if not link['role']:
                context['link_list'].append(
                    self._create_link(link))
                continue
            else:
                role_list = link['role'].split(',')

            for role_select in role_list:

                if role_select in roles:
                    context['link_list'].append(
                        self._create_link(link))
                    break

        return context

    def _get_user_roles(self):
        user = auth_utils.get_user(self.request)
        return [role['name'] for role in user.roles]

    def _get_admin_links(self):
        return getattr(nec_portal_settings, 'ADMIN_LINKS', {})

    def _create_link(self, link):
        disp = {}
        if 'name' in link:
            disp['name'] = link['name'] if link['name'] else ''
        if 'description' in link:
            disp['description'] =\
                link['description'] if link['description'] else ''
        if 'url' in link:
            disp['url'] = link['url'] if link['url'] else ''
        return disp
