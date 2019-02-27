from http import HTTPStatus

import pytest

from bluestorm_api.common.responses import (
    response_bad_request,
    response_created,
    response_no_content,
    response_not_found,
    response_ok,
)


def test_response_ok():
    assert response_ok() == ("", HTTPStatus.OK)


def test_response_created():
    assert response_created() == ("", HTTPStatus.CREATED)


def test_response_no_content():
    assert response_no_content() == ("", HTTPStatus.NO_CONTENT)


def test_response_not_found():
    assert response_not_found() == ("", HTTPStatus.NOT_FOUND)


def test_response_bad_request():
    assert response_bad_request() == ("", HTTPStatus.BAD_REQUEST)
