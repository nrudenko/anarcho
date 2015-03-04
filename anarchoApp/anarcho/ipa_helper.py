from anarcho.models.build import Build
from pyipa import IPAparser


def parse_ipa(ipa_path, app_key):
    ipa_parser = IPAparser(ipa_path)

    info = ipa_parser.parseInfo()

    bundle_id = info['CFBundleIdentifier']
    version_name = info['CFBundleShortVersionString']
    version_code = info['CFBundleVersion']

    icon_keys = filter(lambda i: 'CFBundleIcon' in i, info.keys())
    if len(icon_keys):
        print info[icon_keys[0]]
    #TODO: implement icons parsing
    icon_dest = None
    # icon_dest = os.path.join(os.path.dirname(ipa_path), "%s_icon.png" % app_key)
    # ipa_parser.saveFileTo(icon_zip_path, icon_dest)

    build = Build(app_key, version_code, version_name)

    return {"build": build, "icon_path": icon_dest, "package": bundle_id}