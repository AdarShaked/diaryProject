from flask import Flask
import os
import db
from controllers.event import diary
import sqlite3


def create_app(test_config=None):
    app = Flask(__name__)
    app.register_blueprint(diary)

    app.config.from_mapping(
        DATABASE=os.path.join(app.instance_path, "data.db")
    )

    if test_config:
        # load the test config if passed in
        app.config.update(test_config)

    db.init_app(app)
    return app


if __name__ == '__main__':
    print("not here")
    app.run(port=5000, debug=False)
