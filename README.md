# Python 3 Demo API

Python 3 Demo API is a JSON/REST API written in Python using the
[Flask](https://palletsprojects.com/p/flask/) web application framework with
[Marshmallow](https://marshmallow.readthedocs.io/en/latest/) for JSON marshaling
and [SQLAlchemy](https://www.sqlalchemy.org/) with
[Alembic](https://alembic.sqlalchemy.org/en/latest/) for database access and
management. The API was tested with [MariaDB](https://mariadb.org/) and
[SQLite](https://www.sqlite.org/index.html).

## Login

The API has a minimal [OAuth2](https://oauth.net/2/)/
[OpenID Connect](https://openid.net/connect/)
implementation based on
[Flask-JWT-Extended](https://github.com/vimalloc/flask-jwt-extended). It does
email verification using [AWS SES](https://aws.amazon.com/ses/) and the email
must be verified before the user can authentication to get an `access_token`.
Phone numbers are optional when adding a user and they are validated using the
[phonenumbers Python Library](https://github.com/daviddrysdale/python-phonenumbers)
but they are not verified. In addition to getting a token and verifying an
email, callers can reset passwords and get user information about themselves and
other public users.

## Functionality

The API itself has REST methods to get, set and list "thingy" types.

## Development and testing environments

Install [Python](https://www.python.org/downloads/) 3.7 and
[pip](https://pypi.org/project/pip/) before you start.

The API uses [Pipenv](https://github.com/pypa/pipenv) so setting up
a (venv-based) environment is quick and easy:

1. Install or upgrade Pipenv

    ```bash
    pip install --user --upgrade pipenv
    ```

2. Clone the repo and setup the virtual environment:

    ```bash
    git clone git@github.com:amigus/python3-demo-app.git
    cd python3-demo-app
    pipenv install -d
    ```

3. Create an `instance` folder, `settings.py`, `test_settings.py`:

    Linux/UN*X shell:

    ```bash
    mkdir -p instance
    cd instance
    cat <<EOF>>settings.py
    import os

    base_dir = os.path.dirname(os.path.abspath(__file__))

    SECRET_KEY = "arandomsecret"
    CLIENT_ID = "arandomstring"

    RATELIMIT_ENABLED = False

    SQLALCHEMY_DATABASE_URI = os.environ.get(
        "SQLALCHEMY_DATABASE_URI", f"sqlite:///{os.path.sep.join([base_dir, 'db.sqlite3'])}"
    )

    # DEBUG and testing features
    # SQLAlchemy will log all of the queries it execute
    SQLALCHEMY_ECHO = True
    # Flask will propagate exceptions; extensions test and use the setting too
    TESTING = True
    EOF
    cat <<EOF>>test_settings.py
    SECRET_KEY = "arandomsecret"
    CLIENT_ID = "arandomstring"
    RATELIMIT_ENABLED = False
    SQLALCHEMY_DATABASE_URI = "sqlite:///:memory:"
    TESTING = True
    EOF
    cd ..
    ```

    Windows `Powershell`:

    ```powershell
    mkdir "instance"
    cd "instance"
    New-Item "settings.py" -Value @"
    import os

    base_dir = os.path.dirname(os.path.abspath(__file__))

    SECRET_KEY = "arandomsecret"
    CLIENT_ID = "arandomstring"

    RATELIMIT_ENABLED = False

    SQLALCHEMY_DATABASE_URI = os.environ.get(
        "SQLALCHEMY_DATABASE_URI", f"sqlite:///{os.path.sep.join([base_dir, 'db.sqlite3'])}"
    )

    # DEBUG and testing features
    # SQLAlchemy will log all of the queries it execute
    SQLALCHEMY_ECHO = True
    # Flask will propagate exceptions; extensions test and use the setting too
    TESTING = True
    "@

    New-Item "test_settings.py" -Value @"
    SECRET_KEY = "arandomsecret"
    CLIENT_ID = "arandomstring"
    RATELIMIT_ENABLED = False
    SQLALCHEMY_DATABASE_URI = "sqlite:///:memory:"
    TESTING = True
    "@
    cd ..
    ```

4. Create a `logging.yml` (required when `app.testing != True`):

    Add `LOGGING_YAML` to `settings.py`:

    ```python
    LOGGING_YAML = os.path.sep.join([base_dir, "logging.yml"])
    ```

    Create `instance/logging.yml`:

    Linux/UN*X shell:

    ```bash
    cat <<EOF>>instance/logging.yml
    version: 1
    formatters:
        detailed:
            format: "[%(asctime)s] [%(process)d] [%(levelname)s] [%(filename)s:%(lineno)d] [%(funcName)s] %(message)s"
    handlers:
        stdout:
            class: logging.StreamHandler
            formatter: detailed
            stream: ext://sys.stdout
    root:
        handlers: [stdout]
        level: INFO
    loggers:
        app:
            level: DEBUG
        db:
            level: DEBUG
        emailer:
            level: DEBUG
    EOF
    ```

    Windows `Powershell`:

    ```powershell
    New-Item .\instance\logging.yml -Value @"
    version: 1
    formatters:
        detailed:
            format: "[%(asctime)s] [%(process)d] [%(levelname)s] [%(filename)s:%(lineno)d] [%(funcName)s] %(message)s"
    handlers:
        stdout:
            class: logging.StreamHandler
            formatter: detailed
            stream: ext://sys.stdout
    root:
        handlers: [stdout]
        level: INFO
    loggers:
        app:
            level: DEBUG
        db:
            level: DEBUG
        emailer:
            level: DEBUG
    "@
    ```

5. Start the pipenv shell:

    ```bash
   pipenv shell
   ```

6. Create the [SQLite](https://www.sqlite.org/index.html) development database:

    ```bash
    flask db upgrade
   ```

   NOTE: the database will now exist as `db.sqlite3` in the `instance` folder.

7. Run the server:

    ```bash
    flask run --no-reload
    ```

## Note when pulling

If the changes include changes to the
[Alembic](https://alembic.sqlalchemy.org/en/latest/index.html) migrations, be
sure to run `flask db upgrade` within the virtual environment.

If the changes include changes to the Pipfile or Pipfile.lock, be sure to run
`pipenv sync`.
