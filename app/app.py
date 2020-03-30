from flask import Flask, render_template, request
from PIL import Image
import io
from keras.preprocessing.image import img_to_array, array_to_img
import urllib.request
from socket import timeout
from urllib.error import HTTPError, URLError

import classifier as C
import base64

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
      print('image is uploaded!')
      img = f.read()
      img = Image.open(io.BytesIO(img))
      img = img.convert('RGB')
    elif imgUrl:
      print('image url is given!')
      try:
        img = Image.open(urllib.request.urlopen(imgUrl, timeout=10))
        img = img.convert('RGB')
      except (HTTPError, URLError) as error:
        errorMessage = error
      except timeout:
        errorMessage = 'Oops, Timed out, while retrieving the image. Try with a diffrent image!'
      else:
        print('Image read successfully!')
      
    else:
      return render_template('index.html', data={ 'message': 'No files were given!' })
    
    if (errorMessage is not None):
      return render_template('index.html', data={'message': errorMessage })
    else:
      img = img_to_array(img)
      result = C.predict(img)
      # build the image
      img_object = io.BytesIO()
      array_to_img(result['new_image']).save(img_object, 'JPEG')
      # img_object.seek(0)
      img_64 = base64.b64encode(img_object.getvalue())
      img_encoded = u'data:img/jpeg;base64,'+img_64.decode('utf-8')

      data = {
        'result': result['res'],
        'image': img_encoded,
        'errors': []
      }

      return render_template('index.html', data=data)
      