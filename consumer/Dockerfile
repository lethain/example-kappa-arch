FROM python:3.4-alpine
ADD . /consumer
WORKDIR /consumer
RUN pip install -r /consumer/requirements.txt
CMD ["python", "consumer.py"]

