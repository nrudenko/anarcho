from collections import Iterable

from anarcho import storage_worker
from anarcho.app.models.application import Application
from anarcho.app.models.token import Token
from anarcho.app.models.user import User
from anarcho.app.models.user_app import UserApp


class Serializer(object):
    __json_fields__ = None

    def __init__(self):
        pass

    def to_json(self):
        return jsonify(self.to_dict())

    def to_dict(self):
        fields_dict = {}
        for public_key in self.__json_fields__:
            value = getattr(self, public_key)
            if value:
                if isinstance(value, Serializer):
                    fields_dict[public_key] = value.to_dict()
                elif hasattr(value, "__call__"):
                    fields_dict[public_key] = value()
                else:
                    fields_dict[public_key] = value
        return fields_dict

    def __repr__(self):
        return self.to_json()


class BuildSerializer(Serializer):
    __json_fields__ = ["id",
                       'version_code',
                       'version_name',
                       'release_notes',
                       'created_on']

    def __init__(self, build):
        self.id = build.id
        self.version_code = build.version_code
        self.version_name = build.version_name
        self.release_notes = build.release_notes
        self.created_on = build.created_on


class PermissionSerializer(Serializer):
    __json_fields__ = {"username", "email", "permission"}

    def __init__(self, user_app):
        if user_app.user:
            self.username = user_app.user.name
            self.email = user_app.user.email
        self.permission = user_app.permission



class TrackApi(Serializer):
    __json_fields__ = ['id',
                       'track_log',
                       'track_time',
                       'created_on']


serializerMap = {
    UserApp: AppSerializer,
    Build: BuildSerializer,
}


def serialize(obj, serializer=None):
    if serializer is None:
        if isinstance(obj, Iterable):
            if len(obj) > 0:
                serializer = serializerMap.get(type(obj[0]))
        else:
            serializer = serializerMap.get(type(obj))
    if isinstance(obj, Iterable):
        if len(obj) > 0:
            return jsonify(list=[serializer(i).to_dict() for i in obj])
        else:
            return '{"list":[]}'
    else:
        return serializer(obj).to_json()
