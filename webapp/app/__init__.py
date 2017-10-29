from flask import Flask
from .views import app
from . import models
from . import main
main.init()
models.db.init_app(app)
@app.cli.command()
def test_command():
    models.test_command()
