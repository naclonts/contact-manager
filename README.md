# Contact Manager

This is a lightweight demo SPA to record contacts, made with Flask and Vue.

Data is only saved to sessions (no logins required), so this is only intended for demonstration purposes.

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
