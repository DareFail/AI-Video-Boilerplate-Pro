# AI-Video-Boilerplate-Pro

Welcome to AI Video Boilerplate Pro! A free template to run scalable, cheap AI websites.

Hosted on Heroku for a live demo here: [https://proAI.darefail.com
](https://proAI.darefail.com)

## Live Demos
**A single VPS running this codebase has so far proven to handle over 10,000 concurrent users, 1,000,000 views and 50 websites without issue.**

**[RateLoaf.com](https://rateloaf.com)** - 
Rate how well cats sit like bread with OpenAI GPT4v, Roboflow workflows, and images uploaded to Amazon S3 in a celery task.

**[HandLand.lol](https://handland.lol)** - 
Create live AI multiplayer games using WebRTC, Websockets, and Roboflow for AI vision models.


## Other Repos

**AI Video Boilerplate Simple** (quick frontend apps): [https://github.com/DareFail/AI-Video-Boilerplate-Simple/](https://github.com/DareFail/AI-Video-Boilerplate-Simple)

**AI Video Boilerplate for Chrome Extensions**: [https://github.com/DareFail/AI-Video-Boilerplate-Chrome/](https://github.com/DareFail/AI-Video-Boilerplate-Chrome)

## Django models setup out of the box

<img width="6224" alt="django_models" src="https://github.com/user-attachments/assets/6b794671-d1d8-425d-a0ef-5838147cc854">


## Features

- **Frontend**: minimal HTML and javascript, roll your own
- **Backend**: Django, Docker, Postgres Database, Redis caching, Celery background tasks, Celery Beat scheduled tasks Django
- **Preconfigured Libraries**: Django Allauth authentication, AWS storage, Slack alerts and slack bots, Twilio texting, Sendgrid Email, Captcha spam detection, Sesame Magic Link passwordless signin, Hijack user impersonation
- **Multiplayer**: WebRTC and native Websockets with daphne and channels
- **AI**: Integrated with Roboflow (sponsored project), includes Stable diffusion, Flux, Roboflow installed.
- **Scalable and Cheap to Host**: Run hundreds of websites and millions of users into a heroku, digital ocean, or a VPS of your choice

## Getting Started

This is a template for putting multiple django websites into a single codebase that can be deployed to any VPS for cheap. It is full of full deployed projects and templates for you to copy and modify.

- **XXXXX_basic** - 
    Simple django webpage with shared components like favicons, navigation bar, footer, etc
- **XXXXX_signedin** - 
    Flexible User to Group Sign up flow with django allauth, with teams, administrators, invitations, changing passwords, magic links, and a backend dashboard
- **XXXXX_websockets** - 
    Live multiplayer django apps. This is a chatroom example.

### Installation

1. Clone the repo
   ```sh
   git clone https://github.com/yourusername/AI-Video-Boilerplate-Pro.git
   cd AI-Video-Boilerplate-Pro
   ```
2. Install Docker
    The easiest way to get up and running is with [Docker](https://www.docker.com/).

    Just [install Docker](https://www.docker.com/get-started) and
    [Docker Compose](https://docs.docker.com/compose/install/)
    and then run:
3. Create .env
    Copy .env.example and rename the file .env
    Fill out the uncommented values 
    Uncomment and fill out the other values if you want to use them
4. Build the container and run locally
    ```
    docker compose up
    docker compose exec web python manage.py makemigrations
    docker compose exec web python manage.py migrate
    ```
5. Go to [localhost:8000](http://localhost:8000/)
6. Make a superuser (optional)

    ```
    docker compose exec web python manage.py createsuperuser
    ```
    Check everything works by going to [localhost:8000/admin](http://localhost:8000/admin/) and logging in


## Development

##### Open Visual Studio in Docker
On a Mac: fn + f1
```
Dev Containers Reopen in Container
```

##### To Run Locally

```
docker compose up
```

##### Migrate database
```
docker compose exec web python manage.py makemigrations
docker compose exec web python manage.py migrate

# sometimes have to run
docker compose exec web python manage.py makemigrations [app name]
```

##### Update pip

```
docker compose exec web pip3 install --upgrade pip-tools
docker compose exec web pip3 install --upgrade pip setuptools wheel twine check-wheel-contents
docker compose exec web pip-compile requirements.in
docker compose build
docker compose up
```

##### Linters

```
# Simple python formatting
black .

# Python errors
flake8 .

# Django Templates / Javascript / HTML
djlint .

# Django Templates / Javascript / HTML formatting
djlint . --reformat
```



## Deployment

### Vercel

1. [Sign up](https://vercel.com/signup) or log in to Vercel.
2. Create a new project from the Vercel dashboard.
3. Connect your GitHub repository.
4. Click "Deploy".


### Heroku

1. [Sign up](https://signup.heroku.com) or log in to Heroku.
2. Create a new app from the Heroku dashboard.
3. Fill out all the environment variables from .env. 

In production:

DJANGO_SETTINGS_MODULE=main.settings.heroku


4. Add Heroku Data for Redis and Heroku Postgres in the Add-ons

5. Connect your GitHub repository.
6. Click "Deploy Branch".
7. Set the heroku settings
```
heroku stack:set container
heroku run python manage.py createsuperuser
```

8. Under settings, Configure SSL and set to Automatic Certificate Management (ACM)

9. If an external domain and using cloudflare, point to heroku and change the SSL to Full
```
(If you don't, the url will have an infinite redirect)
```







## Adding a New Website - Localhost

##### 1. Copy XXXXX project folder and rename

##### 2. Rename app_directory in XXXXX/utils.py
```
app_directory = 'XXXXX'
```

##### 3. Rename AppConfig, name, and label in XXXXX/apps.py
```
XxxxxConfig
name = XXXXX
```

##### 4. Add new project name to end of PROJECT_APPS in main/settings.py
```
'XXXXX.apps.XxxxxConfig',
```

##### 5. Rename templates folder path to project name: templates/XXXXX

##### 6. Rename static folder path to project name: static/XXXXX

##### 7. Delete the original migrations folder XXXXX/migrations

##### 8. Add any new app specific models 
```
docker compose exec web python manage.py makemigrations XXXXX
docker compose exec web python manage.py migrate
```

##### 9. Add new logo files from https://realfavicongenerator.net into static/favicons





## Adding a New Website - Production

##### 1. Handle context variables as needed in common/web/context_processors.py

##### 2. Add new domain to VIRTUAL_DOMAINS_X (1, 2, 3, etc)
```
XXXXX.com
```

##### 3. Add new project urls path to VIRTUAL_APPS_X (1, 2, 3, etc)
```
XXXXX.urls
```

##### 4. Increase NUMBER_OF_DOMAINS by +1 (2 -> 3)

##### 5. Add new analytics code (or just a comma ,) to VIRTUAL_GOOGLE_ANALYTICS_X (1, 2, 3, etc)

##### 6. In cloudflare change the SSL to Full
```
(If you don't, the url will have an infinite redirect)
```


## Troubleshooting

Pre commit hooks for linters is not working
```
pre-commit install
```

Ignore precommmit hook
```
git commit --no-verify -m ""
```

List all docker containers
```
docker ps
```

Log into docker database
```
docker exec -it main-db-1 psql -U postgres
```

Inside database - (\l show schema, \c connect to schema, \dt list all tables)
```
\l
\c main
\dt
```

Run Python in Heroku Shell
```
heroku run python

#when loaded

import django
django.setup()
```

Useful repeatable code changer
```
https://pinetools.com/add-text-each-line
```

Static files not found
```
docker compose exec web python manage.py collectstatic
```


## Acknowledgements

Thanks to Roboflow for sponsoring this project. Get your free API key at: [Roboflow](https://roboflow.com/)

## License

Distributed under the APACHE 2.0 License. See `LICENSE` for more information.

## Contact

Twitter: [@darefailed](https://twitter.com/darefailed)

Youtube: [How to Video coming soon](https://www.youtube.com/@darefail)

Project Link: [https://github.com/darefail/AI-Video-Boilerplate-Pro](https://github.com/darefail/AI-Video-Boilerplate-Pro)



