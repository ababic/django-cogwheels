from django.test import TestCase

from apputils.tests.conf import settings


class AppSettingTestCase(TestCase):

    def setUp(self):
        self.appsettingshelper = settings
        self.settings_prefix = settings._prefix
