from flask import Flask
from controllers.event import diary
import sqlite3

app = Flask(__name__)
app.register_blueprint(diary)

if __name__ == '__main__':
    # connection = sqlite3.connect('data.db')
    # with open('schema.sql') as f:
    #     connection.executescript(f.read().decode('utf8'))
    #
    # connection.commit()
    # connection.close()

    app.run(port=5000,debug=True)
