from http import HTTPStatus

from flask import make_response, jsonify


def response_not_found():
    response = make_response("", HTTPStatus.NOT_FOUND)
    response.headers["Content-Type"] = "application/json"

    return response


def response_ok(data=""):
    response = make_response(data, HTTPStatus.OK)
    response.headers["Content-Type"] = "application/json"

    return response


def response_no_content():
    response = make_response("", HTTPStatus.NO_CONTENT)
    response.headers["Content-Type"] = "application/json"

    return response


def response_created(data=""):
    response = make_response(data, HTTPStatus.CREATED)
    response.headers["Content-Type"] = "application/json"

    return response


def response_bad_request(data=""):
    response = make_response(data, HTTPStatus.BAD_REQUEST)
    response.headers["Content-Type"] = "application/json"

    return response


def response_listing(paginate, data=None):
    response = {
        "total": paginate.total,
        "per_page": paginate.per_page,
        "total_pages": paginate.pages,
        "prev_page": paginate.prev_num,
        "next_page": paginate.next_num,
        "current_page": paginate.page,
        "results": data.json or [],
    }

    return response_ok(jsonify(response))
