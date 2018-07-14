# Headline

Headline API example for Python/Django.

## Setup

Create virtualenv and install dependencies:

```sh
virtualenv --python=python3 venv
. venv/bin/activate
pip install -r requirements.txt
```

Create a `.env` file in the base directory containing `GRIP_URL`, e.g.:

```
GRIP_URL=http://localhost:5561
```

Run the server:

```sh
python manage.py runserver
```
