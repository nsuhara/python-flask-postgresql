"""app/run.py
"""

import os

from flask import Flask
from flask_migrate import Migrate

from feedback.common.utility import err_response
from feedback.models import db
from feedback.views.feedback import feedback

app = Flask(__name__, instance_relative_config=True)
app.config.from_pyfile('config.py')

app.register_blueprint(feedback)

db.init_app(app)
Migrate(app, db)


@app.errorhandler(404)
@app.errorhandler(500)
def errorhandler(error):
    """errorhandler
    """
    return err_response(error=error), error.code


def main():
    """main
    """
    host = os.getenv('HOST', '0.0.0.0')
    port = int(os.getenv('PORT', '5000'))
    app.run(host=host, port=port)


if __name__ == '__main__':
    main()
