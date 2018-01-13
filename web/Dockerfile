FROM python:3.4-alpine
ADD . /code
WORKDIR /code
RUN PIP install -r requirements.txt
CMD ["python", "web.py"]
