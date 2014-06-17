from app import db
from app.models.build import Build
from APKParser.apk import APK


def save_build(apk_path, app_key):
    apk_file = APK(apk_path)

    package = apk_file.get_package()
    version_code = apk_file.get_androidversion_code()
    version_name = apk_file.get_androidversion_name()

    _build = Build(app_key, version_code, version_name, '', 'http://')
    db.session.add(_build)
    db.session.commit()