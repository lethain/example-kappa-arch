FROM python:3.4-alpine
#RUN wget -qO - https://packages.confluent.io/deb/4.0/archive.key | sudo apt-key add -
#RUN add-apt-repository "deb [arch=amd64] https://packages.confluent.io/deb/4.0 stable main"
#RUN apk add --update --no-cache build-base gcc libc-dev linux-headers librdkafka-dev
ADD . /web
WORKDIR /web
RUN pip install -r /web/requirements.txt
CMD ["python", "web.py"]

