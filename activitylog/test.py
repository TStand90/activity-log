import os
# import activitylog
import unittest

from selenium import webdriver
from selenium.webdriver.common.keys import Keys


class ActivityLogTestCase(unittest.TestCase):

    def setUp(self):
    	self.browser = webdriver.Firefox()

    def tearDown(self):
    	self.browser.close()

    def test_home_page(self):
    	self.browser.get('http://localhost:5000')

    	assert 'Activity Log' in self.browser.title
    	assert 'Home' not in self.browser.title

    def test_about_page(self):
    	self.browser.get('http://localhost:5000/about')

    	assert 'About' in self.browser.title


if __name__ == '__main__':
	unittest.main()