from flask import Flask
from flask import Flask, render_template, request
from .main import getRecommendation
# Init
app = Flask(__name__)
app.config.from_object('config')
# App
@app.route('/')
def index():
    return render_template('recommend.html', film_id=film_id, recommendation = getRecommendation(int(film_id)))
@app.route('/recommend')
def recommend():
    film_id = request.args.get('film_id') or 3
    return render_template('recommend.html', film_id=film_id, recommendation = getRecommendation(int(film_id)))
# Main
if __name__ == "__main__":
    app.run()
