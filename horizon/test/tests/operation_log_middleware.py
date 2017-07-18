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

from django.http import HttpResponseRedirect  # noqa
from django.test.utils import override_settings

from horizon import exceptions
from horizon import messages
from horizon import operation_log_middleware as middleware
from horizon.test import helpers as test


class OperationLogMiddlewareTests(test.TestCase):

    def set_default_request(self, request, authenticated=True):
        request.META['REQUEST_SCHEME'] = 'http'
        request.META['HTTP_HOST'] = 'xx.xx.xx.xx'
        request.session = {}
        if authenticated:
            request.user.username = 'test_user_name'
            request.user.project_id = 'test_project_id'
            request.user.project_name = 'test_project_name'
            request.session = {u'user_id': 'test_user_id'}
        return request

    @override_settings(
        OPENSTACK_HORIZON_OPERATION_ENABLED=True,
        OPENSTACK_HORIZON_OPERATION_METHOD_TARGETS=['GET', 'POST'])
    def test_get_operation(self):
        url = '/dashboard/identity/users/'

        request = self.factory.get(url)
        request = self.set_default_request(request)

        messages.success(request, 'A test of GET method')

        mw = middleware.OperationLogMiddleware()
        response = HttpResponseRedirect(url)
        response.client = self.client

        resp = mw.process_response(request, response)

        self.assertEqual(302, resp.status_code)

    @override_settings(
        OPENSTACK_HORIZON_OPERATION_ENABLED=True,
        OPENSTACK_HORIZON_OPERATION_METHOD_TARGETS=['GET', 'POST'])
    def test_post_operation(self):
        url = '/dashboard/identity/users/create/'

        request = self.factory.post(url)
        request = self.set_default_request(request)

        request.POST = {
            u'text': u'A test of POST data', u'password': '1234567890'
        }

        messages.success(request, 'A test of POST method')

        mw = middleware.OperationLogMiddleware()
        response = HttpResponseRedirect(url)
        response.client = self.client

        resp = mw.process_response(request, response)

        self.assertEqual(302, resp.status_code)

    @override_settings(
        OPENSTACK_HORIZON_OPERATION_ENABLED=True,
        OPENSTACK_HORIZON_OPERATION_METHOD_TARGETS=['GET', 'POST'])
    def test_exception_operation(self):
        url = '/dashboard/identity/users/'

        request = self.factory.post(url)
        request = self.set_default_request(request)

        request.POST = {
            u'text': u'A test of POST data', u'password': '1234567890'
        }

        messages.error(request, 'A test of exception')

        mw = middleware.OperationLogMiddleware()

        resp = mw.process_exception(request, exceptions.NotAuthorized())

        self.assertIsNone(resp)

    @override_settings(OPENSTACK_HORIZON_OPERATION_ENABLED=False)
    def test_disabled_operation(self):
        url = '/dashboard/identity/users/'

        request = self.factory.get(url)
        request = self.set_default_request(request)

        messages.success(request, 'A test of GET method')

        mw = middleware.OperationLogMiddleware()
        response = HttpResponseRedirect(url)
        response.client = self.client

        resp = mw.process_response(request, response)

        self.assertEqual(302, resp.status_code)

    @override_settings(OPENSTACK_HORIZON_OPERATION_ENABLED=False)
    def test_not_output(self):
        url = '/dashboard/identity/users/'

        request = self.factory.get(url)
        request = self.set_default_request(request)

        messages.success(request, 'A test of GET method')

        mw = middleware.OperationLogMiddleware()
        response = HttpResponseRedirect(url)
        response.client = self.client

        resp = mw.process_response(request, response)

        self.assertEqual(302, resp.status_code)
