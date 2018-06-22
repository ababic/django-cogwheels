import sys
from apputils.app_settings import BaseAppSettingsHelper, DeprecatedAppSetting


class TestAppSettingsHelper(BaseAppSettingsHelper):
    prefix = 'TEST_'
    defaults_path = 'apputils.tests.conf.defaults'

sys.modules[__name__] = TestAppSettingsHelper()
