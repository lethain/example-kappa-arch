FROM ubuntu:xenial

RUN apt-get update
RUN apt-get install default-jre -y
RUN apt-get install zookeeper -y
ADD . /zk
WORKDIR /zk
RUN mkdir -p /var/lib/zookeeper
RUN chown -R zookeeper /var/lib/zookeeper

EXPOSE 2181 2888 3888

CMD ["/usr/share/zookeeper/bin/zkServer.sh", "start-foreground"]
