from flask import Flask
from flask import Flask, render_template, request
from .main import test
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
    origin = request.args.get('origin')
    destination = request.args.get('destination')
    carrier = request.args.get('carrier')
    day = request.args.get('day')
    month = request.args.get('month')
    hour = request.args.get('hour')
    return render_template('index.html', test = test())


if __name__ == "__main__":
    app.run()
