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

"""Test 'Link'.
Please operate setting.
  Step1. Create Projects
    - admin
  Step2. Create Users
    - admin
  Step3. Create Roles
    - admin
      Grant: [admin] project - [admin] user
    - C__Global__ProjectAdmin
      Grant: [admin] project - [admin] user
  Step4. Change Selenium Parameters
    - SET_BASE_URL
  Step5. Change Link Settings
    - nec_portal_settings.py
      - ADMIN_LINKS: Display a link of all user
                     Display a link of valid user
                       (has a [C__Global__ProjectAdmin] role)
                     Display a link of invalid user
      - Project_LINKS: Display a link of all user
                       Display a link of valid user
                         (has a [C__Global__ProjectAdmin] role)
                       Display a link of invalid user
"""

import datetime
import os
import time
import traceback

from horizon.test import helpers as test

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support.ui import WebDriverWait


# Command executor. Hub URL of Jenkins.
SET_COMMAND_EXECUTOR = 'http://127.0.0.1:4444/wd/hub'
# Base URL. Environment for testing.
SET_BASE_URL = 'http://127.0.0.1/dashboard'
# Login user.
SET_USER = {
    'admin': {
        'USERNM': 'admin',
        'PASSWORD': 'xxxx'
    },
}
# Width of the window
SET_WIDTH = 1280
# Height of the window
SET_HEIGHT = 1024
# Implicitly wait
SET_IMPLICITLY_WAIT = 90
SET_TIMEOUT = 5
# Capture of location
SET_CAPPATH = 'openstack_dashboard/test/tests/screenshots/'
# They are arranged sequentially by setting the execution target
SET_METHOD_LIST = [
    'sign_in',
    'change_setting',
    'project_links',
    'admin_links',
    'sign_out',
]
# They are arranged sequentially by setting the browser target
SET_BROWSER_LIST = {
    'firefox': {
        'browserName': 'firefox',
        'version': '',
        'platform': 'ANY',
        'javascriptEnabled': True,
    },
    'chrome': {
        'browserName': 'chrome',
        'version': '',
        'platform': 'ANY',
        'javascriptEnabled': True,
    },
    'ie11': {
        'browserName': 'internet explorer',
        'version': '11',
        'platform': 'WINDOWS',
        'javascriptEnabled': True,
    }
}

# Take the capture
SET_CAPFLG = True
# Test language pattern.
SET_TEST_LANGUAGE = {
    'en': True,
    'ja': True,
}
# Test browser pattern.
SET_TEST_BROWSER = {
    'firefox': True,
    'chrome': True,
    'ie11': True,
}


class BrowserTests(test.SeleniumTestCase):
    """This test will output the capture of Links list service."""

    def setUp(self):
        """Set the Remote instance of WebDriver."""

        super(BrowserTests, self).setUp()

        for key, value in SET_BROWSER_LIST.items():
            self.caps = key
            self.selenium = webdriver.Remote(
                command_executor=SET_COMMAND_EXECUTOR,
                desired_capabilities=value)

            self.selenium.implicitly_wait(SET_IMPLICITLY_WAIT)
            break

    def initialize(self):
        """Initializing process."""

        # Capture count.
        self.cap_count = 1

        # Method name
        self.method = ''

    def test_main(self):
        """Main execution method."""

        try:
            # Datetime
            self.datetime = datetime.datetime.today().strftime('%Y%m%d%H%M%S')

            # Browser order definition
            for key, value in SET_BROWSER_LIST.items():
                if key not in SET_TEST_BROWSER or (not SET_TEST_BROWSER[key]):
                    continue

                if not self.caps == key:
                    self.caps = key
                    self.selenium = webdriver.Remote(
                        command_executor=SET_COMMAND_EXECUTOR,
                        desired_capabilities=value)

                    self.selenium.implicitly_wait(SET_IMPLICITLY_WAIT)

                # Browser display waiting time
                self.selenium.implicitly_wait(SET_IMPLICITLY_WAIT)
                # Set the size of the window
                self.selenium.set_window_size(SET_WIDTH, SET_HEIGHT)

                for language, flg in SET_TEST_LANGUAGE.items():
                    if not flg:
                        continue

                    print ('Test language = [' + language + ']')

                    # Initializing process
                    self.initialize()
                    # Object language
                    self.multiple_languages = language
                    # Call execution method
                    self.execution()

            print('Test has been completed')

        except Exception:
            print('Test failed')

    def execution(self):
        """Method execution order definition."""

        for self.method in SET_METHOD_LIST:
            try:
                method = getattr(self, self.method)
                method()

                print(' Success:' + self.caps + ':' + self.method)
            except Exception as e:
                print(' Failure:' + self.caps + ':' + self.method +
                      ':' + e.message)
                print(traceback.print_exc())

    def save_screenshot(self):
        """Save a screenshot"""
        if SET_CAPFLG:
            filepath = SET_CAPPATH + self.datetime + '/' + \
                self.multiple_languages + '/' + self.caps + '/'
            filename = str(self.cap_count).zfill(4) + \
                '_' + self.method + '.png'
            # Make directory.
            if not os.path.isdir(filepath):
                os.makedirs(filepath)

            time.sleep(SET_TIMEOUT)
            self.selenium.get_screenshot_as_file(filepath + filename)
            self.cap_count = self.cap_count + 1

    def trans(self, urlpath, timeout=SET_TIMEOUT):
        """Transition to function. No wait."""

        time.sleep(timeout)
        self.selenium.get(SET_BASE_URL + urlpath)

    def trans_and_wait(self, nextId, urlpath, timeout=SET_TIMEOUT):
        """Transition to function."""

        time.sleep(timeout)
        self.selenium.get(SET_BASE_URL + urlpath)

        if nextId:
            self.wait_id(nextId, timeout)

    def fill_field(self, field_id, value):
        """Enter a value to the field."""

        self.fill_field_clear(field_id)
        if type(value) in (int, long):
            value = str(value)
        while 0 < len(value):
            split_value = value[0:10]
            self.selenium.find_element_by_id(field_id).send_keys(split_value)
            value = value[10:]

    def fill_field_clear(self, field_id):
        """Clear to the field."""

        time.sleep(SET_TIMEOUT)
        self.selenium.find_element_by_id(field_id).clear()

    def click_and_wait(self, id, nextId, timeout=SET_TIMEOUT):
        """Click on the button."""

        time.sleep(timeout)
        element = self.selenium.find_element_by_id(id)
        element.click()
        self.wait_id(nextId, timeout)

    def click_id(self, id, timeout=SET_TIMEOUT):
        """Click on the button."""

        time.sleep(timeout)
        element = self.selenium.find_element_by_id(id)
        element.click()

    def click_css(self, css, timeout=SET_TIMEOUT):
        """Click on the button css. (no wait)"""
        time.sleep(timeout)
        element = self.selenium.find_element_by_css_selector(css)
        element.click()

    def set_select_value(self, id, value):
        """Set of pull-down menu by value."""
        time.sleep(SET_TIMEOUT)
        Select(self.selenium.find_element_by_id(id)).select_by_value(value)

    def wait_id(self, nextId, timeout=SET_TIMEOUT):
        """Wait until the ID that you want to schedule is displayed."""

        WebDriverWait(self.selenium, timeout).until(
            EC.visibility_of_element_located((By.ID, nextId)))

    def change_setting(self):
        """Change Language"""
        self.trans_and_wait('user_settings_modal', '/settings/')
        self.set_select_value('id_language', self.multiple_languages)
        self.click_css('input[type=submit]')

    def sign_in(self, username='admin'):
        """Sign In."""
        # Run a sign-in
        self.trans_and_wait('loginBtn', '')

        self.fill_field('id_username', SET_USER.get(username).get('USERNM'))
        self.fill_field('id_password', SET_USER.get(username).get('PASSWORD'))

        self.click_id('loginBtn')

    def sign_out(self):
        """Sign Out."""

        # Run to sign out
        self.trans_and_wait('loginBtn', '/auth/logout/')

    def project_links(self):
        """Project Links."""

        # Capture the initial display
        self.trans('/project/links/')
        self.save_screenshot()

    def admin_links(self):
        """Admin Links."""

        # Capture the initial display
        self.trans('/admin/links/')
        self.save_screenshot()
