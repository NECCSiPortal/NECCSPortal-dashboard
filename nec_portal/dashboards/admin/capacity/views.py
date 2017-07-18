# Licensed under the Apache License, Version 2.0 (the "License"); you may
# not use this file except in compliance with the License. You may obtain
# a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
# WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
# License for the specific language governing permissions and limitations
# under the License.

from django.shortcuts import redirect
from django.http import Http404, HttpResponse  # noqa
from django.utils.translation import ugettext_lazy as _

from horizon import tables
from horizon import tabs

from nec_portal.dashboards.admin.capacity import resources\
    as capacity_resources
from nec_portal.dashboards.admin.capacity import tables as capacity_tables
from nec_portal.dashboards.admin.capacity import tabs as capacity_tabs

from nec_portal.local import nec_portal_settings

CAPACITY_DASHBOARD_SERVER = \
    getattr(nec_portal_settings, 'DASHBOARD_SERVER', '')
NOVA_CAP_ADMIN_ALL_URL = \
    getattr(nec_portal_settings, 'NOVA_CAP_ADMIN_ALL_URL', '')
NOVA_CAP_COMMON_URL = \
    getattr(nec_portal_settings, 'NOVA_CAP_COMMON_URL', '')
QUERY_TEXT = 'group:"%(group)s" AND name:"%(name)s"'


class IndexView(tabs.TabbedTableView):
    tab_group_class = capacity_tabs.CapacityGroupTabs
    template_name = 'admin/capacity/index.html'
    page_title = _("Resources")

    COOKIES_PRE_WORD = '%7B%22capacity_group_tabs%22%3A%22%23'
    COOKIES_POST_WORD = '%22%7D'
    TAB_GET_KEY = 'tab'
    FIRST_TAB = 'capacity_group_tabs__capacity'

    def get(self, request):
        get_response = super(IndexView, self).get(request)

        get_parameters = request.GET
        get_cookie_tab = request.COOKIES.get('tabs', '')

        if len(get_cookie_tab) > 0:
            cookie_tab = get_cookie_tab.replace(self.COOKIES_PRE_WORD, '')\
                                       .replace(self.COOKIES_POST_WORD, '')
            if not cookie_tab == self.FIRST_TAB:
                url = './?' + self.TAB_GET_KEY + '=' + cookie_tab
                if len(get_parameters) > 0:
                    for key, value in get_parameters.items():
                        if key == self.TAB_GET_KEY:
                            url = ''
                            break
                        url += '&' + key + '=' + value

                if len(url) > 0:
                    return redirect(url)

        return get_response


class CapacityView(tables.DataTableView):
    table_class = capacity_tables.CapacityTable
    template_name = 'admin/capacity/capacity/index.html'

    def get_data(self):
        get_data = super(CapacityView, self).get_data()
        return get_data

    def get_context_data(self, **kwargs):
        context = super(CapacityView, self).get_context_data(**kwargs)
        context['detail_url'] = './detail'

        return context


class CapacityDetailView(tables.DataTableView):
    table_class = capacity_tables.CapacityTable
    template_name = 'admin/capacity/capacity/_index.html'

    def get_data(self):
        return None

    def get(self, request):
        _check_invalid(request)

        query = QUERY_TEXT % {'group': 'all', 'name': 'ALL'}

        url = ''.join([CAPACITY_DASHBOARD_SERVER,
                       NOVA_CAP_ADMIN_ALL_URL % query])

        return redirect(url)


class CapacityAZView(tables.DataTableView):
    table_class = capacity_tables.CapacityAZTable
    template_name = 'admin/capacity/capacity_az/index.html'

    def get_data(self):
        return None

    def get_context_data(self, **kwargs):
        context = super(CapacityAZView, self).get_context_data(**kwargs)

        context.update(
            capacity_resources.CapacityResources()
                              .get_az_context(self.request))
        return context


class CapacityAZDetailView(tables.DataTableView):
    table_class = capacity_tables.CapacityAZTable
    template_name = 'admin/capacity/capacity_az/_index.html'

    def get_data(self):
        return None

    def get(self, request):
        _check_invalid(request)

        group = request.GET.get('group', '')
        name = request.GET.get('name', '')

        query = QUERY_TEXT % {'group': group, 'name': name}

        url = ''.join([CAPACITY_DASHBOARD_SERVER, NOVA_CAP_COMMON_URL % query])

        return redirect(url)


class CapacityHostView(tables.DataTableView):
    table_class = capacity_tables.CapacityHostTable
    template_name = 'admin/capacity/capacity_host/index.html'

    def get_data(self):
        return None

    def get_context_data(self, **kwargs):
        context = super(CapacityHostView, self).get_context_data(**kwargs)
        context.update(
            capacity_resources.CapacityResources()
                              .get_host_context(self.request))
        return context


class CapacityHostDetailView(tables.DataTableView):
    table_class = capacity_tables.CapacityHostTable
    template_name = 'admin/capacity/capacity_host/_index.html'

    def get_data(self):
        return None

    def get(self, request):
        _check_invalid(request)

        group = request.GET.get('group', '')
        name = request.GET.get('name', '')

        query = QUERY_TEXT % {'group': group, 'name': name}
        url = ''.join([CAPACITY_DASHBOARD_SERVER, NOVA_CAP_COMMON_URL % query])

        return redirect(url)


def _check_invalid(request):
    if request.META.get('HTTP_REFERER') is None:
        raise Http404
    if not request.user.is_authenticated():
        raise Http404
