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

from datetime import datetime
from datetime import timedelta

from django.core.urlresolvers import reverse
from django import http

from horizon.test.dummy_auth import backend

from openstack_dashboard.test import helpers as test

from nec_portal.dashboards.admin.history import views

INDEX_URL = reverse("horizon:admin:history:index")


class HistoryTest(test.BaseAdminViewTests):

    # A test which history index is existed.
    def test_display_index(self):
        self.mox.ReplayAll()
        res = self.client.get(INDEX_URL)

        self.assertTrue(400 > res.status_code)

    # A test which history's post execute.
    def test_search(self):
        self.mox.ReplayAll()
        res = self.client.get(INDEX_URL)

        search = 'portal_keyword_test'
        now = datetime.now()
        past_date = now - timedelta(days=30)

        start = past_date.strftime("%Y-%m-%d")
        end = now.strftime("%Y-%m-%d")

        formData = {
            'search': search,
            'start': start,
            'end': end,
        }

        res = self.client.post(INDEX_URL, formData)
        self.assertNoFormErrors(res)
        self.assertRedirectsNoFollow(res, INDEX_URL)

    # A test which history's post execute to dispatch.
    def test_search_dispatch(self):
        view = views.DetailView()
        view.ADMIN_HISTORY_FRAME = "ADMIN_HISTORY_FRAME"

        request = http.HttpRequest
        request.META = {'HTTP_REFERER': 'HTTP_REFERER'}
        request.user = backend.DummyBackend().get_user('0')
        request.session = {
            'admin_history': {
                'search': '',
                'start': '',
                'end': ''
            }
        }

        self.assertNoFormErrors(
            view.dispatch(request, None, None))
