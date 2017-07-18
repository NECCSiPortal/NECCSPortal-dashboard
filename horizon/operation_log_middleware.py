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

import django
import json
import logging
import re
import urllib

from django.conf import settings
from django.contrib import messages as django_messages


LOG = logging.getLogger(__name__)


class OperationLogMiddleware(object):
    """This middleware output operation log."""

    OPERATION_LOG = None
    ENABLED = getattr(settings, "OPENSTACK_HORIZON_OPERATION_ENABLED", True)
    MASK_TARGETS = getattr(settings,
                           "OPENSTACK_HORIZON_OPERATION_MASK_TARGETS",
                           ['password'])
    MASKING_LENGTH = 8
    METHOD_TARGETS = getattr(settings,
                             "OPENSTACK_HORIZON_OPERATION_METHOD_TARGETS",
                             ['POST'])
    EMPTY_DATA = 'none'
    STATIC_RULE = [
        '/js/',
        '/scss/',
        '/static/',
    ]
    SCHEME_TO_HOST = '://'
    USER_ID = 'user_id'
    SYSTEM_ERROR_MESSAGE = 'System error occurred'
    EXCEPTION_STATUS_CODE = '-'
    MESSAGE_SEPARATOR = ': '
    LOGSTASH_SEPARATOR = ','
    LOGSTASH_REPLACE = '.'

    def _get_unicode(self, param_object):
        try:
            return unicode(param_object, 'utf_8')
        except Exception:
            return str(param_object)

    def _get_json_param(self, request):
        """Change POST data to JSON data and mask data
        request: HttpRequest
        """

        # json parameter
        param = json.dumps(request.POST.items())
        try:
            post_datas = request.POST.iteritems()
        except Exception:
            post_datas = request.POST.items()

        for key, value in post_datas:
            for mask_word in self.MASK_TARGETS:
                if self._get_unicode(mask_word) in key:
                    post_key = re.sub(r"\'$", "", re.sub(r"^u\'", "", key))
                    post_value = re.sub(r"\'$", "", re.sub(r"^u\'", "", value))
                    param = param.replace(
                        '"' + post_key + '", "' + post_value + '"',
                        '"' + post_key + '", "' + '*' * self.MASKING_LENGTH
                        + '"')

        files = request.FILES
        if len(files) > 0:
            file_name = ''
            separator = ''
            for key in files.keys():
                file_name += separator + str(files.get(key))
                separator = ', '

            param = param.replace('[[', '["POST", [[') \
                .replace(']]', ']], ["file_name", "' + file_name + '"]]')

        return param

    def get_log_format(self, request, param_method=''):
        """Get operation log format."""

        request_log = ''

        if not self.ENABLED:
            return request_log

        request_url = urllib.unquote(request.path)
        method = request.method

        if method == 'GET':
            for rule in self.STATIC_RULE:
                if rule in request_url:
                    return request_log

        if self.OPERATION_LOG is None:
            self.OPERATION_LOG = \
                logging.getLogger(__name__ + '.' + self.__class__.__name__)

        if method in self.METHOD_TARGETS:
            if not param_method == '':
                method = param_method

            user = request.user

            if django.VERSION >= (1, 7, 0):
                host = request.scheme
            else:
                host = request.META.get('REQUEST_SCHEME')
            host += self.SCHEME_TO_HOST + request.META.get('HTTP_HOST')
            referer_url = (urllib.unquote(request.META.get('HTTP_REFERER')
                                          .replace(str(host), ''))
                           if not request.META.get('HTTP_REFERER') is None
                           else self.EMPTY_DATA)
            project_name = self.EMPTY_DATA
            project_id = self.EMPTY_DATA
            user_name = self.EMPTY_DATA
            if user.is_authenticated():
                project_name = user.project_name
                if self.LOGSTASH_SEPARATOR in project_name:
                    project_name = \
                        project_name.replace(self.LOGSTASH_SEPARATOR,
                                             self.LOGSTASH_REPLACE)
                project_id = user.project_id
                user_name = user.username
                if self.LOGSTASH_SEPARATOR in user_name:
                    user_name = \
                        user_name.replace(self.LOGSTASH_SEPARATOR,
                                          self.LOGSTASH_REPLACE)
            user_id = self.EMPTY_DATA
            if self.USER_ID in request.session.keys():
                user_id = request.session.get(self.USER_ID)
            param = self._get_json_param(request).replace('%', '%%')
            request_log = ' '.join([project_name, project_id, user_name,
                                    user_id, referer_url, request_url, '%s',
                                    method, '%s', param])
            request_log = \
                request_log.replace(project_name + ' ' + project_id + ' ' +
                                    user_name + ' ' + user_id,
                                    project_name + self.LOGSTASH_SEPARATOR +
                                    project_id + ' ' + user_name +
                                    self.LOGSTASH_SEPARATOR + user_id)

        return request_log

    def process_response(self, request, response):
        """Response log is made by information of HttpRequest and HttpResponse.
        And Response log is output.
        """

        log = self.get_log_format(request)

        if not log == '':

            # Get result message
            message_array = django_messages.get_messages(request)
            result_message = '['
            separator = ''
            if request.method == 'POST':
                try:
                    post_keys = request.POST.iterkeys()
                except Exception:
                    post_keys = request.POST.keys()
                if len(message_array) > 0:
                    for message in message_array:
                        result_message += (separator + str(message.tags) +
                                           self.MESSAGE_SEPARATOR +
                                           str(message))
                        separator = ', '
                elif 'action' in post_keys:
                    result_message += str(request.POST.get('action'))

            result_message += ']'

            log = log % (self._get_unicode(result_message),
                         str(response.status_code))
            try:
                self.OPERATION_LOG.info(log)
            except Exception as errors:
                LOG.error(self.SYSTEM_ERROR_MESSAGE +
                          self.MESSAGE_SEPARATOR + errors)

        return response

    def process_exception(self, request, exception):
        """Exception log is made by information of HttpRequest and Exception.
        And Exception log is output.
        """

        log = self.get_log_format(request, 'ERROR')

        if not log == '':

            result_message = '['
            if exception.message == '':
                result_message += self.SYSTEM_ERROR_MESSAGE
            else:
                result_message += exception.message
            result_message += ']'

            log = log % (result_message, self.EXCEPTION_STATUS_CODE)

            try:
                self.OPERATION_LOG.info(log)
            except Exception as errors:
                LOG.error(self.SYSTEM_ERROR_MESSAGE +
                          self.MESSAGE_SEPARATOR + errors)
