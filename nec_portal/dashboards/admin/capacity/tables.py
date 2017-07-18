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

from horizon import tables


class CapacityTable(tables.DataTable):
    def get_object_display(self, obj):
        return obj.name

    class Meta(object):
        name = 'capacity'
        table_actions = ()
        row_actions = ()


class CapacityAZTable(tables.DataTable):
    def get_object_display(self, obj):
        return obj.name

    class Meta(object):
        name = 'capacity_az'
        table_actions = ()
        row_actions = ()


class CapacityHostTable(tables.DataTable):
    def get_object_display(self, obj):
        return obj.name

    class Meta(object):
        name = 'capacity_host'
        table_actions = ()
        row_actions = ()
