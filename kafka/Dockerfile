FROM ubuntu:xenial

RUN apt-get update
RUN apt-get install default-jre -y
ADD . /kafka
WORKDIR /kafka
RUN tar -xvzf ./kafka.tgz --strip 1
CMD ["./bin/kafka-server-start.sh", "./server.properties"]
