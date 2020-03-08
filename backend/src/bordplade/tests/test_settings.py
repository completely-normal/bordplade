from django.conf import Settings
from django.test import TestCase
from unittest.mock import patch


class DevEnvironmentSettingsTest(TestCase):
    def _load_settings(self):
        """
        Helper function, which ensures that the settings module is reloaded
        cleanly. This allows us to modify the environment, files or other data
        sources, which are loaded inside the settings module, then run multiple
        tests in a row. Without clean reloads, the settings module would be
        cached and changes may not apply properly.
        """
        from importlib import reload, import_module
        settings_module_name = "bordplade.settings.dev"
        settings_module = import_module(settings_module_name)
        reload(settings_module)
        return Settings(settings_module_name)

    def test_secret_key(self):
        """
        Verifies that, when `DJANGO_SECRET_KEY` is available in the process
        environment, it is used as the `SECRET_KEY` setting.
        """
        with patch.dict("os.environ", {'DJANGO_SECRET_KEY': "1234"}):
            settings = self._load_settings()
            self.assertEqual(settings.SECRET_KEY, "1234")

    def test_secret_key_not_set(self):
        """
        Verifies that, when `DJANGO_SECRET_KEY` is absent in the process
        environment, `SECRET_KEY` is assigned a random value. Also we expect a
        warning to be raised.
        """
        with self.assertWarns(UserWarning, msg="DJANGO_SECRET_KEY not set in environment"), \
             patch.dict("os.environ", {'DJANGO_SECRET_KEY': ""}):
            settings = self._load_settings()
            self.assertNotEqual(settings.SECRET_KEY, "")


class ProdEnvironmentSettingsTest(TestCase):
    def test_secret_key(self):
        self.fail("Not implemented")
