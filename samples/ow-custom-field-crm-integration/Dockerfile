FROM python:3.10.0

# set working directory
RUN mkdir -p /usr/src/app
WORKDIR /usr/src/app

# install environment dependencies
RUN apt-get update -yqq \
  && apt-get install -yqq --no-install-recommends \
  openssl \
  && apt-get -q clean

# add requirements (to leverage Docker cache)
COPY requirements.txt ./

# install requirements
RUN pip install -r requirements.txt

COPY ./app/ /usr/src/app/app

CMD uvicorn app.main:app --host 0.0.0.0 --port 5000 reload