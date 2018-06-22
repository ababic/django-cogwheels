import sys
from apputils import BaseAppSettingsHelper


class TestAppSettingsHelper(BaseAppSettingsHelper):
    prefix = 'TEST_'
    defaults_path = 'apputils.tests.conf.defaults'

sys.modules[__name__] = TestAppSettingsHelper()
