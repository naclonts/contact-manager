# Contact Manager

This is a lightweight SPA to record contacts, made with Flask and Vue.

## Install
This app requires PostgreSQL, Webpack, and NPM.

```
cp .env.example .env
pip install -r requirements.txt
npm install
npm run build-dev
```

Create a database in Postgres and update the `.env` file with the appropriate URI.

Finally, start up the development server with `python run.py`.
