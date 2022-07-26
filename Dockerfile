FROM ubuntu

COPY ./app /app/
WORKDIR /app/

RUN apt-get update && apt-get install -y python3-pip python3-dev build-essential libssl-dev libffi-dev python3-setuptools libmysqlclient-dev
RUN pip3 install flask flask-mysqldb

CMD python3 app.py
