## Install dependencies
```
$ pip install -r requirements.txt
```

## Run locally

```
$ env FLASK_APP=app/app.py flask run
```

The app will be available at `http://127.0.0.1:5000/classifier`.

## Run locally with uWSGI
Run from inside the `app` directory
```
$ uwsgi -s /tmp/objclf.sock -w wsgi:app --mount /=app:app --virtualenv ../venv --socket 0.0.0.0:5000 --protocol=http
```
