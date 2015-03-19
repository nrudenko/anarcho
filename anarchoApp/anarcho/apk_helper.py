from uuid import uuid4

from androguard.core.bytecodes.apk import APK
import os


def save_file_from_apk(apk_file, file_name, dest):
    f = apk_file.get_file(file_name)
    out = open(dest, 'wb')
    out.write(f)
    out.close()


def save_icon(apk, package):
    icon_hex_id = apk.get_element("application", "icon")
    icon_id = int(icon_hex_id.replace("@", ""), 16)
    icon_name = apk.get_android_resources().get_id(package, icon_id)[1]
    icons = [x for x in apk.files if icon_name in x]

    tmp_icon_path = os.path.join(os.path.dirname(apk.filename), "%s_icon.png" % str(uuid4()))

    if len(icons) > 0:
        save_file_from_apk(apk, icons[-1], tmp_icon_path)
    else:
        tmp_icon_path = None

    return tmp_icon_path


def parse_apk(apk_path):
    apk = APK(apk_path)

    package = apk.get_package()
    version_code = apk.get_androidversion_code()
    version_name = apk.get_androidversion_name()
    tmp_icon = save_icon(apk, package)

    return {"version_code": version_code,
            "version_name": version_name,
            "tmp_icon": tmp_icon,
            "package": package}