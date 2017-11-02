from flask import Flask
from flask import Flask, render_template, request
from .main import getRecommendation
from .main_clustering import getRecommendation_
from .main_dmatrix import getRecommendation__

app = Flask(__name__)
app.config.from_object('config')

@app.route('/')
def index():
    film_id = request.args.get('film_id') or 3
    return render_template('recommend.html', film_id=film_id, recommendation = getRecommendation(int(film_id)))
@app.route('/recommend')
def recommend():
    film_id = request.args.get('film_id') or 3
    return render_template('recommend.html', film_id=film_id, recommendation = getRecommendation(int(film_id)),recommendation_ = getRecommendation_(int(film_id)),recommendation__ = getRecommendation__(int(film_id)))

if __name__ == "__main__":
    app.run()
