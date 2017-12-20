from flask import Flask
from flask import Flask, render_template, request
#from .main import getRecommendation
app = Flask(__name__)
app.config.from_object('config')
def render(film_id):
    movie, recommendations = getRecommendation(int(film_id))
    if movie is None or recommendations is None:
        return render_template('recommend.html',movie = None, recommendation = None, available = False)
    else :
        return render_template('recommend.html',movie = movie.to_html(index=False), recommendation = recommendations.to_html(index=False), available = True)
@app.route('/')
def index():
    return render_template('index.html')


if __name__ == "__main__":
    app.run()
