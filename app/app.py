from flask import Flask, render_template, request
from PIL import Image
import io
from keras.preprocessing.image import img_to_array
import urllib.request
from socket import timeout
from urllib.error import HTTPError, URLError

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
    errorMessage = None
    imgUrl = request.form.get('imgUrl')
    if f:
      print('file is uploaded!')
      img = f.read()
      img = Image.open(io.BytesIO(img))
    elif imgUrl:
      print('image url is given!')
      try:
        img = Image.open(urllib.request.urlopen(imgUrl, timeout=15))
      except (HTTPError, URLError) as error:
        errorMessage = error
      except timeout:
        errorMessage = 'Timed out while reading the image!'
      else:
        print('Image read successfully!')
      
    else:
      return render_template('index.html', data={ 'message': 'No files were given!' })
    
    if (errorMessage is not None):
      return render_template('index.html', data={'message': errorMessage })
    else:
      img = img_to_array(img)
      results = C.predict(img)

      data = {
        'results': results,
        'errors': []
      }

      return render_template('index.html', data=data)
      