from flask import jsonify


class Base():
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
                if hasattr(value, "__call__"):
                    fields_dict[public_key] = value()
                else:
                    fields_dict[public_key] = value
        return fields_dict
