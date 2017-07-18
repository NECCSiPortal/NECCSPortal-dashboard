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

from django.conf.urls import patterns
from django.conf.urls import url

from nec_portal.dashboards.admin.capacity import views

urlpatterns = patterns(
    'nec_portal.dashboards.admin.capacity.views',
    url(r'^$', views.IndexView.as_view(), name='index'),
    url(r'^capacity/detail',
        views.CapacityDetailView.as_view(), name='capacity_detail'),
    url(r'^capacity/',
        views.CapacityView.as_view(), name='capacity'),
    url(r'^capacity_az/detail',
        views.CapacityAZDetailView.as_view(), name='capacity_az_detail'),
    url(r'^capacity_az/',
        views.CapacityAZView.as_view(), name='capacity_az'),
    url(r'^capacity_host/detail',
        views.CapacityHostDetailView.as_view(), name='capacity_host_detail'),
    url(r'^capacity_host/',
        views.CapacityHostView.as_view(), name='capacity_host'),
)
