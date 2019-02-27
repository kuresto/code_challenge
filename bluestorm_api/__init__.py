from flask_marshmallow import Marshmallow

from .app import create_app

app = create_app()
marshmallow = Marshmallow(app)

if __name__ == "__main__":
    app.run()
