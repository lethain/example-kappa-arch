FROM python:3.4-alpine
ADD . /web
WORKDIR /web
RUN pip install -r /web/requirements.txt
CMD ["python", "web.py"]

