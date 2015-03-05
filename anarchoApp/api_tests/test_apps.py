import json

from api_tests import AnarchoTestCase


class AppsTest(AnarchoTestCase):
    def setUp(self):
        AnarchoTestCase.setUp(self)
        self.register()
        self.login()

    def test_apps_list(self):
        self.create_app()

        r = self.do_get('/api/apps')
        self.assert_status_code(r)
        response = json.loads(r.data)
        self.assertTrue('list' in response, 'apps list response should contain array "list"')
        apps_list = response['list']
        self.assertTrue(len(apps_list) == 1, 'apps list should contain one app')

    def test_create_app(self):
        app_name = 'sing_app_test'
        r = self.create_app(app_name=app_name)
        self.assert_status_code(r)
        app = json.loads(r.data)
        self.assertTrue(app['name'] == app_name, 'apps name should be {0}'.format(app_name))

    def test_plugin_config(self):
        r = self.create_app()
        app = json.loads(r.data)
        r = self.do_get('/api/apps/' + app['app_key'] + '/plugin')
        self.assert_status_code(r)
        config = json.loads(r.data)
        self.assertTrue('apiToken' in config, 'Plugin config should contain "apiToken"')
        self.assertTrue('uploadUrl' in config, 'Plugin config should contain "uploadUrl"')

    def test_get_app_info(self):
        self.create_app()
        app_key = self.created_app.app_key
        r = self.do_get('api/apps/' + app_key)
        response_data = json.loads(r.data)
        self.assertTrue('app_key' in response_data, 'App info should contain "app_key"')
        self.assertTrue('created_on' in response_data, 'App info should contain "created_on"')
        self.assertTrue('name' in response_data, 'App info should contain "name"')
        self.assertTrue('permission' in response_data, 'App info should contain "permission"')
