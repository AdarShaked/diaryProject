from flask import Flask

import db
from controllers.event import diary
import sqlite3


def create_app(db_name="data.db"):
    app = Flask(__name__)

    app.register_blueprint(diary)
    app.config["DATABASE"] = db_name

    db.init_app(app)

    return app


if __name__ == '__main__':
    print("not here")
    # connection = sqlite3.connect('data.db')
    # with open('schema.sql') as f:
    #     connection.executescript(f.read().decode('utf8'))
    #
    # connection.commit()
    # connection.close()

    app.run(port=5000, debug=True)
