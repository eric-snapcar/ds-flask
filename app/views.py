from flask import Flask
from flask import Flask, render_template, request
from . import models
# Init
app = Flask(__name__)
app.config.from_object('config')
# App
@app.route('/')
def index():
    return render_template('index.html')
@app.route('/result')
def result():
    gender = request.args.get('gender')
    user_name = request.args.get('user_name') or "None"
    description = request.args.get('description') or "None"
    return render_template('result.html', user_name=user_name, description = description , blur = True)


@app.route('/recommend')
def recommend():
    film_id = request.args.get('film_id') or "None"
    return render_template('recommend.html', film_id=film_id, recommendation = models.recommend())
# http://localhost:5000/result?description=DescriptionBis&user_name=Eric
# Main
if __name__ == "__main__":
    app.run()
