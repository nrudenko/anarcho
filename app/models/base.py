from flask import jsonify


class Base():
    __json_fields__ = None

    def to_json(self):
        dict = {}
        print self.__dict__
        for public_key in self.__json_fields__:
            value = getattr(self, public_key)
            if value:
                dict[public_key] = value
        return jsonify(dict)

    def to_dict(self):
        dict = {}
        print self.__dict__
        for public_key in self.__json_fields__:
            value = getattr(self, public_key)
            if value:
                dict[public_key] = value
        return dict
