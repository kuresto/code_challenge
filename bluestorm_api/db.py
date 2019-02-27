from flask_sqlalchemy import SQLAlchemy

from .common.mixins import CRUDMixin

db = SQLAlchemy(model_class=CRUDMixin)
