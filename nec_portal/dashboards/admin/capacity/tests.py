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
import mock

from django.core.urlresolvers import reverse

from mox3.mox import IsA  # noqa

from openstack_dashboard.api import nova
from openstack_dashboard.test import helpers as test
from openstack_dashboard.test.test_data import utils as test_utils

from nec_portal.dashboards.admin.capacity import panel  # noqa

INDEX_URL = reverse('horizon:admin:capacity:index')


class CapacityViewTests(test.BaseAdminViewTests):
    """A test of the screen of capacity's index.
    CheckPoint 1. A expected template is used.
    """
    def test_capacity(self):
        self.mox.ReplayAll()
        res = self.client.get(INDEX_URL)
        self.assertTemplateUsed(res, 'admin/capacity/capacity/_index.html')


class CapacityAZTabTests(test.BaseAdminViewTests):
    """A test of the screen of capacity's az tab.
    CheckPoint 1. A expected template is used.
    CheckPoint 2. A expected context is returned.
    """

    TEST_GROUP = 'test_az_group'
    TEST_NAME = 'test.az:name'
    CONTEXT_GROUP = 'az'

    def setUp(self):
        test.BaseAdminViewTests.setUp(self)
        self.testdata = test_utils.TestData()
        test_utils.load_test_data(self.testdata)

    @mock.patch('novaclient.v2.client.Client')
    @test.create_stubs({nova: ('availability_zone_list',), })
    def test_capacity_az(self, request):
        self.mox.ReplayAll()
        url_param = '?group=' + self.TEST_GROUP + '&name=' + self.TEST_NAME

        nova.novaclient(self.request).availability_zones = \
            self.availability_zones

        availability_zone_list = self.availability_zones.list()
        for az in availability_zone_list:
            if not az.zoneName == 'internal':
                context_name = az.zoneName
                break

        context_url = './capacity_az/detail?group=' + self.CONTEXT_GROUP + \
                      '&name=' + context_name

        res = self.client.get(INDEX_URL + url_param +
                              '&tab=capacity_group_tabs__capacity_az')

        self.assertTemplateUsed(res, 'admin/capacity/capacity_az/_index.html')
        self.assertEqual(res.context['detail_url'], context_url)


class CapacityHostTabTests(test.BaseAdminViewTests):
    """A test of the screen of capacity's host tab.
    CheckPoint 1. A expected template is used.
    CheckPoint 2. A expected context is returned.
    """

    TEST_GROUP = 'test_host_group'
    TEST_NAME = 'test_host,name'
    CONTEXT_GROUP = 'host'

    def setUp(self):
        test.BaseAdminViewTests.setUp(self)
        self.testdata = test_utils.TestData()
        test_utils.load_test_data(self.testdata)

    @mock.patch('novaclient.v2.client.Client')
    @test.create_stubs({nova: ('hypervisor_list',), })
    def test_capacity_host(self, request):
        self.mox.ReplayAll()
        url_param = '?group=' + self.TEST_GROUP + '&name=' + self.TEST_NAME

        nova.novaclient(self.request).hypervisors = self.hypervisors

        hypervisor_list = self.hypervisors.list()
        context_name = hypervisor_list[0].hypervisor_hostname

        context_url = './capacity_host/detail?group=' + self.CONTEXT_GROUP + \
                      '&name=' + context_name

        res = self.client.get(INDEX_URL + url_param +
                              '&tab=capacity_group_tabs__capacity_host')

        self.assertTemplateUsed(res,
                                'admin/capacity/capacity_host/_index.html')
        self.assertEqual(res.context['detail_url'], context_url)
