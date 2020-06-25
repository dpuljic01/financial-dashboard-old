# Masters Thesis - Financial Dashboard

Insert some description here :)

### Migrations

Whenever a database migration needs to be made. Run the following commands

```bash
docker-compose run --rm manage db migrate
flask db migrate # If running locally without Docker
```

This will generate a new migration script. Then run

```bash
docker-compose run --rm manage db upgrade
flask db upgrade # If running locally without Docker
```

To apply the migration.

If you will deploy your application remotely (e.g on Heroku) you should add the `migrations` folder to version control.
You can do this after `flask db migrate` by running the following commands

```bash
git add migrations/*
git commit -m "Add migrations"
```

Make sure folder `migrations/versions` is not empty.


### Heroku

* Set environmental variables (change `SECRET_KEY` value)

    ```bash
    heroku config:set SECRET_KEY=not-so-secret
    heroku config:set FLASK_APP=autoapp.py
    ```

* Deploy on Heroku by pushing to the `heroku` branch or some other branch you created

    ```bash
    git push <heroku|staging|production> master
    ```
  
* Running the app

    - *locally* -> `python app.py`
    - *staging* -> `heroku run python app.py --app financial-dashboard-stage`
    - *production* -> `heroku run python app.py --app financial-dashboard-prod`
