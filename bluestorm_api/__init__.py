from flask import redirect
from .app import create_app

app = create_app()


@app.route("/")
def start():
    return redirect("/apidocs/", code=302)


if __name__ == "__main__":
    app.run(host="0.0.0.0")
