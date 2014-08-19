from app import db
from app.models.build import Build
from APKParser.apk import APK


def save_file_from_apk(apk_file, file_name, dest):
    f = apk_file.get_file(file_name)
    out = open(dest, 'wb')
    out.write(f)
    out.close()


def save_build(apk_path, app_key):
    apk_file = APK(apk_path)

    package = apk_file.get_package()
    version_code = apk_file.get_androidversion_code()
    version_name = apk_file.get_androidversion_name()

    build = Build(app_key, version_code, version_name, package, 'http://')
    db.session.add(build)
    db.session.commit()

    icon_hex_id = apk_file.get_element("application", "android:icon")
    icon_id = int(icon_hex_id.replace("@", ""), 16)
    icon_name = apk_file.get_android_resources().get_id(package, icon_id)[1]
    icons = apk_file.get_android_resources().get_drawable(package, icon_name)
    if len(icons) > 0:
        save_file_from_apk(apk_file, icons[-1][1], "%s_icon.png" % (build.app_key))
    return build