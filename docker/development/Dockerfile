FROM python:3.6.1

RUN apt-get update && apt-get install mysql-client gettext libgettextpo-dev libyaml-dev libcurl4-openssl-dev libssl-dev -y

ENV DOCKERIZE_VERSION v0.6.1
RUN wget https://github.com/jwilder/dockerize/releases/download/$DOCKERIZE_VERSION/dockerize-linux-amd64-$DOCKERIZE_VERSION.tar.gz \
    && tar -C /usr/local/bin -xzvf dockerize-linux-amd64-$DOCKERIZE_VERSION.tar.gz \
    && rm dockerize-linux-amd64-$DOCKERIZE_VERSION.tar.gz

RUN wget https://dl.minio.io/client/mc/release/linux-amd64/mc --output-document=/usr/local/bin/mc
RUN chmod +x /usr/local/bin/mc

RUN mkdir /code/
WORKDIR /code/

ADD ./.keys/id_rsa /etc/id_rsa

RUN mkdir -p ${HOME}/.ssh/
RUN cp /etc/id_rsa ${HOME}/.ssh/id_rsa
RUN chmod 400 ${HOME}/.ssh/id_rsa
RUN echo "Host github.com\n\tStrictHostKeyChecking no\n" >> ${HOME}/.ssh/config

RUN mkdir -p /code/requirements/

ADD ./requirements/base.txt /code/requirements/base.txt
RUN pip install -r /code/requirements/base.txt

ADD ./requirements/development.txt /code/requirements/development.txt
RUN pip install -r /code/requirements/development.txt

ADD ./setup.py /code/setup.py
ADD ./README.md /code/README.md
RUN mkdir src

RUN pip install -e .

ADD ./docker/docker-entrypoint.sh /tmp/docker-entrypoint.sh

ENTRYPOINT ["bash", "/tmp/docker-entrypoint.sh"]
