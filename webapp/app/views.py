from flask import Flask
from flask import Flask, render_template, request
from .main import predict
app = Flask(__name__)
app.config.from_object('config')

@app.route('/')
@app.route('/airdata')
@app.route('/predict')
def index():
    origin = request.args.get('origin') or 'ATL'
    destination = request.args.get('destination') or 'BOS'
    carrier = request.args.get('carrier') or 'DL'
    day = request.args.get('day') or '12'
    month = request.args.get('month') or '12'
    hour = request.args.get('hour') or '16'
    return render_template('index.html', prediction = predict(origin,destination,carrier,day,month,hour))


if __name__ == "__main__":
    app.run()
