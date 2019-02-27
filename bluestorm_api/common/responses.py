from http import HTTPStatus


def response_not_found():
    return "", HTTPStatus.NOT_FOUND


def response_ok(data=""):
    return data, HTTPStatus.OK


def response_no_content():
    return "", HTTPStatus.NO_CONTENT


def response_created(data=""):
    return data, HTTPStatus.CREATED


def response_bad_request(data=""):
    return data, HTTPStatus.BAD_REQUEST
