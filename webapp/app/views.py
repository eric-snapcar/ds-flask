from flask import Flask
from flask import Flask, render_template, request
from .main import getRecommendation
from .main_clustering import getRecommendation_ as getRecommendation_clustering
from .main_dmatrix import getRecommendation__ as getRecommendation_distance

app = Flask(__name__)
app.config.from_object('config')


def display(movie, recommendations ):
    if movie is None or recommendations is None:
        res = 'Sorry, we are not able to recommend you a movie based on the selected movie'
    else:
        selected_columns_display = ['movie_title', 'genres','director_name','title_year']
        res = movie[selected_columns_display].to_string(index=False,header=False)
        res += ' ------------------ '
        res += recommendations[selected_columns_display].to_string(index=False,header=False)
    return res
def render(film_id):
    recommendation1 =  getRecommendation(int(film_id))
    recommendation2 =  getRecommendation_clustering(int(film_id))
    recommendation3 =  getRecommendation_distance(int(film_id))
    return render_template('recommend.html', film_id=film_id, recommendation1 = recommendation1, recommendation2 = recommendation2, recommendation3 = recommendation3)

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
