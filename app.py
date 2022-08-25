from flask import Flask,render_template,request,redirect
from numpy import dtype, mod
import pandas as pd
import pickle

with open('model.pkl','rb') as f:
    model = pickle.load(f)

with open('scaler.pkl','rb') as f:
    scaler = pickle.load(f)


app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/predictor', methods=['GET', 'POST'])
def contact():
    pred=0
    weather = ''
    if request.method == 'POST':
        precip = request.form.get('precip')
        humidity = request.form.get('humidity')
        winds = request.form.get('winds')
        windb = request.form.get('windb')
        visibility = request.form.get('visibility')
        pressure = request.form.get('pressure')
        print(type(precip))
        if(precip=='snow'):
            precip = 0
            print(0)
        else:
            precip = 1
            print(1)

        df = pd.DataFrame([[precip,humidity,winds,windb,visibility,pressure]],columns=['Precip Type','Humidity','Wind Speed (km/h)','Wind Bearing (degrees)','Visibility (km)','Pressure (millibars)'])
        df = pd.DataFrame(scaler.transform(df))
        pred = model.predict(df)
        if(pred<15 and pred>7):
            weather = 'weather will be cold today.grab your swetar'
        elif(pred > 15 and pred<30):
            weather = 'weather will be very normal today.Good day to hang out'
        elif(pred<7):
            weather = 'weather will be very cold today.Can expect thunderstorm'
        elif(pred>30):
            weather = 'Too hot outside.more time outside can even cause sunstroke'
        return render_template('contact.html',pred=pred[0],weather=weather)
    return render_template('contact.html',pred=0)

if __name__ == '__main__':
    app.run(debug=True)