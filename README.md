# BoxedWithLove

BoxedWithLove is a Flask + Jinja + Tailwind CSS MVP for a gift basket storefront.

## Setup

```bash
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
npm install
npm run build:css
```

## Run the app

```bash
flask --app run.py run
```

The app will be available at `http://127.0.0.1:5000`.

## Project structure

```
boxedwithlove/
  __init__.py
  config.py
  api/
  routes/
  services/
  templates/
  static/
    css/
    js/
run.py
requirements.txt
```

## Notes

- Data is stored in-memory via mock services.
- API endpoints are available under `/api` and return JSON.
