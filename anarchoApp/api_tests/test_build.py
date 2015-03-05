import anarcho
from anarcho.models.build import Build
from api_tests import AnarchoTestCase
from flask import json


class BuildTest(AnarchoTestCase):
    def setUp(self):
        AnarchoTestCase.setUp(self)
        self.register()
        self.login()
        self.create_app()
        self.app_key = self.created_app.app_key

    def create_build(self, app_type='andr', package='com.test.test'):
        # TODO: replace with real build uploading

        build = Build(self.created_app.app_key, '1', '1')

        anarcho.db.session.add(build)
        anarcho.db.session.commit()

        build.app.app_type = app_type
        build.app.package = package
        anarcho.db.session.commit()

        return build

    def test_build_get(self):
        build = self.create_build()
        r = self.do_get('/api/apps/{app_key}/{build_id}'.format(app_key=self.app_key,
                                                                build_id=build.id))
        build = json.loads(r.data)
        self.assert_status_code(r)
        self.assertTrue('version_name' in build, 'Build should contain "version_name"')
        self.assertTrue('version_code' in build, 'Build should contain "version_code"')
        self.assertTrue('created_on' in build, 'Build should contain "created_on"')
        self.assertTrue('build_url' in build, 'Build should contain "build_url"')
        self.assertTrue('id' in build, 'Build should contain "id"')
        self.assertIs(len(build), 5, 'Added new  unchecked fields')

    def test_build_delete(self):
        build1 = self.create_build()
        build2 = self.create_build()
        ids = [build1.id, build2.id]
        self.assertIs(Build.query.filter(Build.id.in_(ids)).count(), 2, 'Builds was added incorrectly')
        r = self.do_delete('/api/apps/{app_key}/builds'.format(app_key=self.app_key),
                           {"ids": ids})
        self.assert_status_code(r)
        self.assertIs(Build.query.filter(Build.id.in_(ids)).count(), 0, 'Builds aren\'t deleted')

    def test_builds_list(self):
        build1 = self.create_build()
        build2 = self.create_build()
        ids = [build1.id, build2.id]
        r = self.do_get('/api/apps/{app_key}/builds'.format(app_key=self.app_key))
        self.assert_status_code(r)
        builds = json.loads(r.data)['list']
        self.assertIs(len(builds), 2, 'Wrong build count in list')
        for b in builds:
            self.assertTrue(b['id'] in ids, 'Build {0} isn\'t in list'.format(b['id']))

    def test_build_notes_update(self):
        build = self.create_build()
        r = self.do_post('/api/apps/{app_key}/{build_id}/notes'.format(app_key=self.app_key,
                                                                       build_id=build.id),
                         {'release_notes': 'new notes'})
        self.assert_status_code(r)
        updated_build = Build.query.filter_by(app_key=self.app_key, id=build.id).first()
        self.assertEqual(updated_build.release_notes, 'new notes', 'Wrong release notes after update')