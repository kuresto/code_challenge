from http import HTTPStatus

import pytest

from flask import make_response

from bluestorm_api.common.responses import (
    response_bad_request,
    response_created,
    response_no_content,
    response_not_found,
    response_ok,
)


def test_response_ok():
    response = response_ok()
    assert response.status_code == HTTPStatus.OK
    assert response.data == b""


def test_response_created():
    response = response_created()
    assert response.status_code == HTTPStatus.CREATED
    assert response.data == b""


def test_response_no_content():
    response = response_no_content()
    assert response.status_code == HTTPStatus.NO_CONTENT
    assert response.data == b""


def test_response_not_found():
    response = response_not_found()
    assert response.status_code == HTTPStatus.NOT_FOUND
    assert response.data == b""


def test_response_bad_request():
    response = response_bad_request()
    assert response.status_code == HTTPStatus.BAD_REQUEST
    assert response.data == b""
