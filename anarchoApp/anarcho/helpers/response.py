from flask import make_response
import json


class Response(object):
    """
    Response wrapper helper.
    """

    @staticmethod
    def success(body, code=200):
        """
        Returns success ful response.

        :param str body:
        :param int code:
        :return:
        """
        return make_response(body, code)

    @staticmethod
    def failure(reason, code=403):
        """
        Returns response with serialized json string about error reason.

        :param str reason:
        :param int code:
        :return:
        """
        return make_response(json.dumps({
            "error": reason
        }), code)
