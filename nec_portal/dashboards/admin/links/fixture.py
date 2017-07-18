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

ROLES = [u'_member_', u'admin', u'heat_stack_owner']
GET_LINKS = [
    {
        'name': 'A',
        'description': 'xxxxxxxxxxxxxxxxxxxxxx',
        'url': 'http://xx.xx.xx.xx',
        'role': ''
    },
    {
        'name': 'B',
        'description': 'xxxxxxxxxxxxxxxxxxxxxx',
        'url': 'http://xx.xx.xx.xx',
        'role': 'test,_member_'
    },
    {
        'name': 'repository',
        'description': 'xxxxxxxxxxxxxxxxxxxxxx',
        'url': 'https://xx.xx.xx.xx',
        'role': 'test'
    },
    {
        'name': 'D',
        'description': 'xxxxxxxxxxxxxxxxxxxxxx',
        'url': 'http://xx.xx.xx.xx',
        'role': '_member_'
    },
    {
        'description': 'xxxxxxxxxxxxxxxxxxxxxx',
        'url': 'http://xx.xx.xx.xx',
        'role': ''
    },
    {
        'name': 'F',
        'url': 'https://xx.xx.xx.xx',
        'role': ''
    },
    {
        'name': 'G',
        'description': 'xxxxxxxxxxxxxxxxxxxxxx',
        'role': ''
    },
    {
        'name': 'H',
        'description': 'xxxxxxxxxxxxxxxxxxxxxx',
        'url': 'http://xx.xx.xx.xx',
    },
    {
        'name': '',
        'description': 'xxxxxxxxxxxxxxxxxxxxxx',
        'url': 'http://xx.xx.xx.xx',
        'role': ''
    },
    {
        'name': 'J',
        'description': '',
        'url': 'http://xx.xx.xx.xx',
        'role': ''
    },
    {
        'name': 'K',
        'description': 'xxxxxxxxxxxxxxxxxxxxxx',
        'url': '',
        'role': ''
    },
    {
        'name': None,
        'description': 'xxxxxxxxxxxxxxxxxxxxxx',
        'url': 'http://xx.xx.xx.xx',
    },
    {
        'name': 'M',
        'description': None,
        'url': 'http://xx.xx.xx.xx',
        'role': ''
    },
    {
        'name': 'N',
        'description': 'xxxxxxxxxxxxxxxxxxxxxx',
        'url': None,
        'role': ''
    },
    {
        'name': 'O',
        'description': 'xxxxxxxxxxxxxxxxxxxxxx',
        'url': '',
        'role': None
    },
]

RESULT_LINKS = [
    {
        'name': 'A',
        'description': 'xxxxxxxxxxxxxxxxxxxxxx',
        'url': 'http://xx.xx.xx.xx',
    },
    {
        'name': 'B',
        'description': 'xxxxxxxxxxxxxxxxxxxxxx',
        'url': 'http://xx.xx.xx.xx',
    },
    {
        'name': 'D',
        'description': 'xxxxxxxxxxxxxxxxxxxxxx',
        'url': 'http://xx.xx.xx.xx',
    },
    {
        'description': 'xxxxxxxxxxxxxxxxxxxxxx',
        'url': 'http://xx.xx.xx.xx',
    },
    {
        'name': 'F',
        'url': 'https://xx.xx.xx.xx',
    },
    {
        'name': 'G',
        'description': 'xxxxxxxxxxxxxxxxxxxxxx',
    },
    {
        'name': 'H',
        'description': 'xxxxxxxxxxxxxxxxxxxxxx',
        'url': 'http://xx.xx.xx.xx',
    },
    {
        'name': '',
        'description': 'xxxxxxxxxxxxxxxxxxxxxx',
        'url': 'http://xx.xx.xx.xx',
    },
    {
        'name': 'J',
        'description': '',
        'url': 'http://xx.xx.xx.xx',
    },
    {
        'name': 'K',
        'description': 'xxxxxxxxxxxxxxxxxxxxxx',
        'url': '',
    },
    {
        'name': '',
        'description': 'xxxxxxxxxxxxxxxxxxxxxx',
        'url': 'http://xx.xx.xx.xx',
    },
    {
        'name': 'M',
        'description': '',
        'url': 'http://xx.xx.xx.xx',
    },
    {
        'name': 'N',
        'description': 'xxxxxxxxxxxxxxxxxxxxxx',
        'url': '',
    },
    {
        'name': 'O',
        'description': 'xxxxxxxxxxxxxxxxxxxxxx',
        'url': '',
    },
]
