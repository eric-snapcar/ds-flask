from flask import Flask
from flask import Flask, render_template, request
from .main import getRecommendation
from .main_clustering import getRecommendation_ as getRecommendation_clustering
from .main_dmatrix import getRecommendation__ as getRecommendation_distance
from .main_clustering_v2 import getRecommendation as getRecommendation_clustering_v2
from .main_dmatrix_v2 import getRecommendation as getRecommendation_distance_v2
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
    """
    recommendation1 =  getRecommendation(int(film_id))
    movie2, recommendations2 = getRecommendation_clustering_v2(int(film_id))
    recommendation2 =   display(movie2, recommendations2 ) #getRecommendation_clustering(int(film_id))
    """
    movie, recommendations = getRecommendation_distance_v2(int(film_id))
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
