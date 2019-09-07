FROM alpine:latest as build

RUN apk update && apk upgrade && apk add python3
RUN apk add python3-dev mariadb-dev build-base libjpeg-turbo-dev\
 tiff-dev libffi-dev
RUN pip3 install --upgrade pip pipenv

RUN mkdir -p /build

WORKDIR /build

# The package is versioned according to the current Pipfile and setup.py
COPY Pipfile Pipfile.lock setup.py ./
COPY app ./app/
COPY db ./db/
COPY emailer ./emailer/
COPY oauth2 ./oauth2/

# Some software builds require this
ENV LANG C.UTF-8

# Install everything into site-packages
RUN pipenv install --deploy --system
RUN pip3 install .

ARG logging_yaml=instance/logging.yaml
ARG settings_py=instance/settings.py

RUN mkdir -p /instance

COPY ${logging_yaml} /instance/logging.yaml
COPY ${settings_py} /instance/settings.py

# Start fresh, copy the install over and run the application using gunicorn
FROM alpine:latest

RUN apk update && apk upgrade && apk add python3
RUN apk add py3-gunicorn py3-flask
RUN apk add mariadb-connector-c

# Copy commands and site-packages from the builder
COPY --from=build /usr/lib/python3.7/site-packages\
 /usr/lib/python3.7/site-packages
COPY --from=build /instance /usr/var/app-instance

ENV APP_SETTINGS=settings.py
ENV FLASK_APP=app
ENV FLASK_ENV=production
ENV PYTHONUNBUFFERED 1

EXPOSE 8000

ENTRYPOINT [ "/usr/bin/gunicorn", "-b", "0.0.0.0:8000", "-w", "3", "app.run" ]
