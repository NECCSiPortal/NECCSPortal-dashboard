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

from django.core.urlresolvers import reverse_lazy
from django import shortcuts
from django.utils.translation import ugettext_lazy as _

from horizon import forms
from horizon import messages


class HistoryForm(forms.SelfHandlingForm):
    search = forms.CharField(label=_('Keyword'),
                             required=False,
                             max_length=255,
                             help_text=_(
                                 '[1]Regular expression is available.'
                                 '(Ex.)&quot;user_name:demo*&quot; '
                                 'returns all the logs of users whose '
                                 'name beginning with &quot;demo&quot;. '
                                 '[2]All columns are searched when no '
                                 'columns are selected. '
                                 '[3]AND/OR/NOT search operators are '
                                 'supported.(Ex.)&quot;user_name:demo '
                                 'AND POST&quot; returns POST logs of '
                                 'user &quot;demo&quot;.'))
    start = forms.DateField(label=_('From:'),
                            input_formats=("%Y-%m-%d",))
    end = forms.DateField(label=_('To:'),
                          input_formats=("%Y-%m-%d",))

    def __init__(self, *args, **kwargs):
        super(HistoryForm, self).__init__(*args, **kwargs)
        self.fields['start'].widget.attrs['data-date-format'] = "yyyy-mm-dd"
        self.fields['end'].widget.attrs['data-date-format'] = "yyyy-mm-dd"

    def clean(self):
        cleaned_data = self.cleaned_data
        start_date = cleaned_data.get('start', None)
        end_date = cleaned_data.get('end', None)
        if start_date and end_date and start_date > end_date:
            messages.error(self.request,
                           _('Invalid time period. The end date should be '
                             'more recent than the start date.'))
        return cleaned_data

    def handle(self, request, data):
        response = shortcuts.redirect(
            reverse_lazy("horizon:project:history:index"))
        return response
