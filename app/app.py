from flask import Flask, render_template, request
from PIL import Image
import io
from keras.preprocessing.image import img_to_array

import classifier as C

app = Flask(__name__)

@app.route("/api/v0.1")
def hello():
  return "You are at v0.1 of the API"

@app.route("/api/v0.1/predict")
def predict():
  pass

@app.route("/classifier", methods=["POST", "GET"])
def index():
  if request.method == "GET":
    return render_template('index.html')

  elif request.method == "POST":

    f = request.files['file']
    img = f.read()
    img = Image.open(io.BytesIO(img))
    img = img_to_array(img)

    results = C.predict(img)

    data = {
      'results': results,
      'errors': []
    }

    return render_template('index.html', data=data)