from flask import Flask, render_template, redirect, url_for, request, session, Response
import pandas as pd
import numpy as np
import logging
import datetime
import os.path
from flask import Markup
import os
import cv2
import mediapipe as mp

# from flask import Flask
from flask_cors import CORS

# def gen_frames():  
#     camera = cv2.VideoCapture(0)
#     while True:
#         success, frame = camera.read()  # read the camera frame
#         if not success:
#             break
#         else:
#             ret, buffer = cv2.imencode('.jpg', frame)
#             frame = buffer.tobytes()
#             yield (b'--frame\r\n'
#                    b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')  # concat frame one by one and show result


app=Flask(__name__)
app.config["DEBUG"]= True
CORS(app)

@app.route('/',methods=["POST","GET"])
def home():

    return render_template("index.html")

@app.route('/squats',methods=["POST","GET"])
def squats():
    count=0
    calories=0
    from squats import squats
    if request.method=="POST":
        data = request.get_json()
        count_input = int(data['count'])
        print("input count : ", count_input)
        count, calories = squats(count_input)

    return {'count':count,'calories':calories}

# @app.route('/video_feed')
# def video_feed():
#     return Response(gen_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/pushup',methods=["POST","GET"])
def pushups():
    count=0
    calories=0
    if request.method=="POST":
        from push_up import pushup
        print("started")
        data = request.get_json()
        count_input = int(data['count'])
        print("input count : ", count_input)
        count, calories = pushup(count_input)

    return {'count': count, 'calories': calories}

@app.route('/pullup',methods=["POST","GET"])
def pullup():
    count=0
    calories=1

    if request.method=="POST":
        from pull_up import pullup
        print("started")
        data = request.get_json()
        count_input = int(data['count'])
        print("input count : ",count_input)
        count,calories = pullup(count_input)

    # return render_template('pullup.html',count = count,calories = calories)
    return {'count':count,'calories':calories}

@app.route('/biceps',methods=["POST","GET"])
def biceps():
    count=0
    calories=0
    if request.method=="POST":
        from weight_lifting import biceps
        print("started")
        data = request.get_json()
        count_input = int(data['count'])
        print("input count : ", count_input)
        count, calories = biceps(count_input)

    return {'count': count, 'calories': calories}

@app.route('/crunches',methods=["POST","GET"])
def crunches():
    
    count=0
    calories=0
    if request.method=="POST":
        from crunches import crunches
        print("started")
        data = request.get_json()
        count_input = int(data['count'])
        print("input count : ", count_input)
        count, calories = crunches(count_input)

    return {'count': count, 'calories': calories}

@app.route('/count',methods=["POST","GET"])
def count():
    return render_template('count.html')

if __name__ == '__main__': 

    app.run()
