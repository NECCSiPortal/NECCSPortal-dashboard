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

from django.core.urlresolvers import reverse

from mox3.mox import IsA  # noqa

from openstack_dashboard.test import helpers as test

from nec_portal.dashboards.project.links import fixture

from nec_portal.dashboards.project.links import views

INDEX_URL = reverse('horizon:project:links:index')


class LinksViewTests(test.TestCase):
    """A test of the screen of links's index.
    CheckPoint 1. A expected template is used.
    CheckPoint 2. A expected context is returned.
    """
    @test.create_stubs({views.IndexView: ('_get_project_links',)})
    @test.create_stubs({views.IndexView: ('_get_user_roles',)})
    def test_links(self):

        views.IndexView._get_user_roles().AndReturn(fixture.ROLES)
        views.IndexView._get_project_links().AndReturn(fixture.GET_LINKS)

        self.mox.ReplayAll()
        res = self.client.get(INDEX_URL)
        self.assertTemplateUsed(res, 'project/links/_index.html')
        self.assertEqual(res.context['link_list'], fixture.RESULT_LINKS)
