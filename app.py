from flask import Flask, render_template, request, jsonify, url_for,redirect
from yhf import YOLO_ClassCountPlot
import plotly
import json
import plotly.express as px
from collections import deque
import os
import time

class_count = {}
random_images = deque(maxlen=5)
def calculate_class_count(path):
   global class_count
   global random_images
    # Calculate class count using YOLO_ClassCountPlot.count(path)
   random_images, class_count = YOLO_ClassCountPlot.count(path)
   return random_images, class_count

app = Flask(__name__)
@app.route('/')
def home():
   return render_template("index.html")

@app.route("/sample")
def showSamples():
   print(random_images)
   return render_template("samples.html", img_list = list(random_images))

# @app.route("/dash_count")
# def dash_count();
#    return render_template("dash")

@app.route("/get_count", methods=["POST", "GET"])
def get_count():
   if request.method == "POST":
      try:
         path = request.get_json()["value"]
         if not class_count:
               calculate_class_count(path)
         return jsonify(class_count)
      except Exception as e:
         return jsonify({"error": "Error processing the request"}), 500
   elif request.method == "GET":
      return jsonify(class_count)


@app.route("/dash")
def dash():
   global class_count
   graphJSON = {}
   class_count_d = {"Classes": list(class_count.keys()), "Count": list(class_count.values())}
   fig = px.bar(class_count_d, x="Classes", y="Count")
   graphJSON = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)
   return render_template('dash.html', graphJSON=graphJSON)

if __name__ == "__main__":
   app.run(debug=True)