import json
from test import AnarchoTestCase


class AppsTest(AnarchoTestCase):
    def setUp(self):
        AnarchoTestCase.setUp(self)
        self.make_auth()

    def create_app(self, app_name='test_app'):
        params = {'name': app_name}
        return self.post_json('/api/apps', params)

    def test_apps_list(self):
        self.create_app()

        r = self.get_json('/api/apps')
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
        r = self.get_json('/api/apps/' + app['app_key'] + '/plugin')
        self.assert_status_code(r)
        config = json.loads(r.data)
        self.assertTrue('apiToken' in config, 'Plugin config should contain "apiToken"')
        self.assertTrue('uploadUrl' in config, 'Plugin config should contain "uploadUrl"')