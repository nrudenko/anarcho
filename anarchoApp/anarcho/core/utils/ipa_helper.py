from uuid import uuid4
import os

from pyipa import IPAparser

from anarcho.app.ipin import update_png


def get_icon(info, ipa_parser, ipa_path):
    icon_bundle = next(x for x in info.keys() if 'CFBundleIcon' in x)
    icon_names = info.get(icon_bundle)['CFBundlePrimaryIcon']['CFBundleIconFiles']

    def _check(name):
        for i in icon_names:
            if i in name:
                return True
        return False

    # find all files in ipa with names from icon_names
    icons_zip_files = filter(lambda zf: _check(os.path.basename(zf.filename)), ipa_parser.zip_obj.filelist)

    # sort zip files by size
    sorted_icons_zip_files = sorted(icons_zip_files, key=lambda zf: zf.file_size)

    # find and extract largest icon
    if len(sorted_icons_zip_files) > 0:
        largest_icon = sorted_icons_zip_files[-1]
        tmp_icon_path = os.path.join(os.path.dirname(ipa_path), "%s_icon.png" % str(uuid4()))
        ipa_parser.saveFileTo(largest_icon, tmp_icon_path)
        update_png(tmp_icon_path)
    else:
        tmp_icon_path = None

    return tmp_icon_path


def parse_ipa(ipa_path):
    ipa_parser = IPAparser(ipa_path)
    info = ipa_parser.parseInfo()

    bundle_id = info['CFBundleIdentifier']
    version_name = info['CFBundleShortVersionString']
    version_code = info['CFBundleVersion']
    tmp_icon = get_icon(info, ipa_parser, ipa_path)

    return {"version_code": version_code,
            "version_name": version_name,
            "tmp_icon": tmp_icon,
            "package": bundle_id}
