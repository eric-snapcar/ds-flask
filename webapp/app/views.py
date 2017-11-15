from flask import Flask
from flask import Flask, render_template, request
from .main import getRecommendation
app = Flask(__name__)
app.config.from_object('config')


def display_movie(movie,recommendations ):
    if movie is None or recommendations is None:
        res = 'Sorry, we are not able to recommend you a movie based on the selected movie'
    else:
        res = movie.to_html()
        res += ' ------------------ '
        res += recommendations.to_html()
    return recommendations
def render(film_id):
    movie, recommendations = getRecommendation(int(film_id))
    if movie is None or recommendations is None:
        return render_template('recommend.html',movie = None, recommendation = None, available = False)
    else :
        return render_template('recommend.html',movie = movie.to_html(index=False), recommendation = recommendations.to_html(index=False), available = True)
@app.route('/')
def index():
    film_id = request.args.get('film_id') or 3
    return render(film_id)
@app.route('/recommend')
def recommend():
    film_id = request.args.get('film_id') or 3
    return render(film_id)

if __name__ == "__main__":
    app.run()
