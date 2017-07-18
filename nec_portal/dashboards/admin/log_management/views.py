# -*- coding: utf-8 -*-

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
Views for managing operation logs.
"""

from django.http import Http404
from django.http import HttpResponseForbidden
from django.shortcuts import redirect
from django.utils.translation import ugettext_lazy as _

from horizon import tables

from nec_portal.dashboards.admin.log_management \
    import tables as log_management_tables

from nec_portal.local import nec_portal_settings

ADMIN_LOG_MANAGEMENT_FRAME = \
    getattr(nec_portal_settings, 'ADMIN_LOG_MANAGEMENT_FRAME', '')


class IndexView(tables.DataTableView):
    table_class = log_management_tables.LogManagementTable
    template_name = 'admin/log_management/index.html'
    page_title = _('Infrastructure Log')

    def get_data(self):
        return None


class DetailView(tables.DataTableView):
    table_class = log_management_tables.LogManagementTable
    template_name = 'admin/log_management/index.html'

    def get_data(self):
        return None

    def get(self, request):
        if request.META.get('HTTP_REFERER') is None:
            raise Http404
        if not request.user.is_authenticated():
            return HttpResponseForbidden()
        if ADMIN_LOG_MANAGEMENT_FRAME == '':
            raise Http404

        return redirect(ADMIN_LOG_MANAGEMENT_FRAME)
