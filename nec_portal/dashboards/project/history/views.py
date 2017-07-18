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

from datetime import date
from datetime import datetime

try:
    import urllib2
except Exception:
    import urllib.request as urllib2

from django.core.urlresolvers import reverse_lazy
from django.http import Http404
from django.http import HttpResponseForbidden
from django.shortcuts import redirect
from django.utils.translation import ugettext_lazy as _

from horizon import forms
from nec_portal.dashboards.project.history import forms as history_forms

from nec_portal.local import nec_portal_settings

# iframe src for project/history
PROJECT_HISTORY_FRAME = \
    getattr(nec_portal_settings, 'PROJECT_HISTORY_FRAME', '')

DATE_FORMAT = '%Y-%m-%d'
DATETIME_FORMAT = '%Y-%m-%d %H:%M:%S'
START_TIME = ' 00:00:00'
END_TIME = ' 23:59:59'

QUERY_ADD_START = 'AND ('
QUERY_ADD_END = ')'
QUERY_START_MILISEC = '.000Z'
QUERY_END_MILISEC = '.999Z'
# Dictionary for query format
QUERY_DICTIONARY = {
    'project_id': '',
    'search': '',
    'start': '',
    'end': '',
}

SESSION_HISTORY_KEY = 'project_history'
# Dictionary for session
SESSION_DICTIONARY = {
    'search': '',
    'start': '',
    'end': '',
}


class IndexView(forms.ModalFormView):
    form_class = history_forms.HistoryForm
    form_id = "history_modal"
    modal_header = ""
    modal_id = "history_modal"
    page_title = _("Operation Log")
    submit_label = _("Filter")
    submit_url = reverse_lazy("horizon:project:history:index")
    template_name = 'project/history/index.html'

    def get_initial(self):
        request = self.request

        # Initialize value
        search_value = ''
        default_term = get_default_term()
        start_value = default_term[0]
        end_value = default_term[1]

        referer_url = request.META.get('HTTP_REFERER')

        if SESSION_HISTORY_KEY not in request.session.keys():
            SESSION_DICTIONARY['search'] = search_value
            SESSION_DICTIONARY['start'] = start_value
            SESSION_DICTIONARY['end'] = end_value

            request.session[SESSION_HISTORY_KEY] = SESSION_DICTIONARY

        session = request.session.get(SESSION_HISTORY_KEY, SESSION_DICTIONARY)

        if request.method == 'POST':
            # When request's method is POST, value get from POST data.
            if 'search' in request.POST.keys():
                search_value = request.POST['search'].encode('utf-8')
            else:
                search_value = session.get('search', search_value)

            if 'start' in request.POST.keys():
                start_value = request.POST['start'] + (
                    START_TIME if str(request.POST['start']) else '')
            else:
                start_value = session.get('start', start_value)

            if 'end' in request.POST.keys():
                end_value = request.POST['end'] + (
                    END_TIME if str(request.POST['end']) else '')
            else:
                end_value = session.get('end', end_value)

            SESSION_DICTIONARY['search'] = search_value
            if start_value == '' or end_value == '':
                start_value = default_term[0]
                end_value = default_term[1]
            SESSION_DICTIONARY['start'] = start_value
            SESSION_DICTIONARY['end'] = end_value
            request.session[SESSION_HISTORY_KEY] = SESSION_DICTIONARY

        elif referer_url is not None and request.path in referer_url:
            # When reload screen, value get from session data.
            search_value = session.get('search', search_value)
            start_value = session.get('start', start_value)
            end_value = session.get('end', end_value)

        if (not start_value) or (not end_value):
            start_value = default_term[0] + DATETIME_FORMAT
            end_value = default_term[1] + DATETIME_FORMAT

        return {
            'search': search_value,
            'start': datetime.strptime(start_value, DATETIME_FORMAT).date(),
            'end': datetime.strptime(end_value, DATETIME_FORMAT).date(),
        }

    def form_valid(self, form):
        return form.handle(self.request, form.cleaned_data)


class DetailView(forms.ModalFormView):
    form_class = history_forms.HistoryForm
    form_id = "history_modal"
    modal_header = ""
    modal_id = "history_modal"
    page_title = _("Operation Log")
    submit_label = _("Filter")
    submit_url = reverse_lazy("horizon:project:history:index")
    template_name = 'project/history/index.html'

    def dispatch(self, request, *args, **kwargs):
        if request.META.get('HTTP_REFERER') is None:
            raise Http404
        if not request.user.is_authenticated():
            return HttpResponseForbidden()
        if PROJECT_HISTORY_FRAME == '':
            raise Http404

        project_id = 'None'
        if request.user.is_authenticated():
            project_id = request.user.project_id

        # Initialize dictionary
        QUERY_DICTIONARY['project_id'] = \
            urllib2.quote(str('project_id:"' + project_id + '"'))
        QUERY_DICTIONARY['search'] = ''
        QUERY_DICTIONARY['start'] = ''
        QUERY_DICTIONARY['end'] = ''

        session = request.session.get(SESSION_HISTORY_KEY,
                                      SESSION_DICTIONARY)

        if not session['search'] == '':
            QUERY_DICTIONARY['search'] = \
                urllib2.quote(
                    QUERY_ADD_START + session['search'] + QUERY_ADD_END)

        if session['start'] == '' or session['end'] == '':
            default_term = get_default_term()
            start_datetime = datetime.strptime(default_term[0],
                                               DATETIME_FORMAT)
            end_datetime = datetime.strptime(default_term[1],
                                             DATETIME_FORMAT)
            session['start'] = default_term[0]
            session['end'] = default_term[1]
        else:
            start_datetime = datetime.strptime(
                session['start'],
                DATETIME_FORMAT
            )
            end_datetime = datetime.strptime(session['end'], DATETIME_FORMAT)

        if start_datetime > end_datetime:
            default_term = get_default_term()
            start_datetime = datetime.strptime(default_term[0],
                                               DATETIME_FORMAT)
            end_datetime = datetime.strptime(default_term[1],
                                             DATETIME_FORMAT)
            session['start'] = default_term[0]
            session['end'] = default_term[1]

        QUERY_DICTIONARY['start'] = \
            urllib2.quote(
                start_datetime.strftime(DATETIME_FORMAT).replace(' ', 'T')
                + QUERY_START_MILISEC)
        QUERY_DICTIONARY['end'] = \
            urllib2.quote(
                end_datetime.strftime(DATETIME_FORMAT).replace(' ', 'T')
                + QUERY_END_MILISEC)

        return redirect(PROJECT_HISTORY_FRAME % QUERY_DICTIONARY)


def char_to_int(value):
    try:
        # Try whether it can be converted into an integer
        return int(value)
    except ValueError:
        return 0


def get_default_term():
    today = date.today()
    year = today.year
    month = today.month
    months = char_to_int(getattr(nec_portal_settings, 'DEFAULT_PERIOD', '13'))
    while True:
        if month - months <= 0:
            year -= 1
            month += 12
        else:
            month -= months
            break

    start_value = datetime.strftime(
        datetime(year, month, 1).date(),
        DATE_FORMAT) + START_TIME
    end_value = datetime.strftime(today, DATE_FORMAT) + END_TIME

    return [start_value, end_value]
