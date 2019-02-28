from http import HTTPStatus

from flask import jsonify

from .responses import response_bad_request, response_unauthorized


def bad_request_handler(error):
    return response_bad_request(jsonify({"error": error.description}))


def unauthorized_handler(error):
    return response_unauthorized(jsonify({"error": error.description}))
