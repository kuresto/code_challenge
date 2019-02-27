from unittest import mock

import pytest

from flask.app import Flask

from bluestorm_api import app


def test_app():
    assert type(app) is Flask
