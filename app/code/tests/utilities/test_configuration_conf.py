import unittest
from project.DependencyContainer import DependencyContainer


class TestConfigurationCONF(unittest.TestCase):
    def setUp(self):
        super().setUp()
        self.app = DependencyContainer()
        self.config = self.app.config_conf()  # ConfigurationCONF

    def test_get_configuration_CONF(self):
        app_name = self.config.get("APP", "name")
        static_path = self.config.get("STATIC", "path")

        self.assertEqual(app_name, "Kubernetes Flash")
        self.assertEqual(static_path, "static")


if __name__ == '__main__':
    unittest.main()
