FROM centos:7

# Environment
ENV LANGUAGE en_US.UTF-8
ENV LANG en_US.UTF-8
ENV LC_ALL en_US.UTF-8
ENV LC_CTYPE en_US.UTF-8
ENV LC_MESSAGES en_US.UTF-8
ENV LC_ALL en_US.UTF-8

# Install packages
RUN yum -y update \
  && yum -y install epel-release \
  && yum -y install yum-utils \
    git wget \
    gcc make \
    libssl-dev \
    python3-devel \
    mariadb-libs \
    mariadb-devel \
    zlib-dev \
    openssl-devel \
  && yum -y groupinstall "Development Tools" \
  && yum clean all

# Python settings
RUN yum install -y https://centos7.iuscommunity.org/ius-release.rpm
RUN yum install -y python36u python36u-libs python36u-devel python36u-pip
RUN ln -s /bin/python3.6 /bin/python3
RUN unlink /bin/python
RUN ln -s /bin/python3 /bin/python
RUN ln -s /bin/pip3.6 /bin/pip

# Airflow settings
ARG AIRFLOW_VERSION=1.9.0
ENV AIRFLOW_HOME=/opt/airflow
ENV AWS_DEFAULT_REGION=ap-northeast-2

RUN mkdir -p ${AIRFLOW_HOME}/logs \
    && mkdir -p ${AIRFLOW_HOME}/dags

ADD airflow.cfg ${AIRFLOW_HOME}/airflow.cfg
ADD /script/entrypoint.sh ${AIRFLOW_HOME}/entrypoint.sh

RUN chmod +x ${AIRFLOW_HOME}/entrypoint.sh
RUN pip install -U pip setuptools wheel \
  && pip install slackclient==1.1.3 \
  && pip install boto3==1.6.6 \
  && pip install PyMySQL==0.7.11 \
  && pip install apache-airflow[crypto,password,s3,slack,mysql]==$AIRFLOW_VERSION

EXPOSE 8080

# Run webserver
USER root
WORKDIR ${AIRFLOW_HOME}
ENTRYPOINT ["./entrypoint.sh"]