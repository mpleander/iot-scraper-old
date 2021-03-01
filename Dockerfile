FROM ubuntu:20.04

# LABEL about the custom image
LABEL maintainer="mpleander@gmail.com"
LABEL version="0.1"
LABEL description="Docker service for scraping data of particle.io."


# Disable Prompt During Packages Installation
ARG DEBIAN_FRONTEND=noninteractive

# Update Ubuntu Software repository
RUN apt-get update -y &&\
apt-get -y install python3.9&&apt-get -y install python3-pip &&\
apt-get install -y libmariadb-dev

RUN mkdir app
COPY . /app/.
WORKDIR /app

# If you do not have the driver file the run below command.
# RUN wget https://downloads.mariadb.com/Connectors/odbc/connector-odbc-3.1.7/mariadb-connector-odbc-3.1.7-ga-rhel7-x86_64.tar.gz

# Copy mariadb drivers to catalogue
RUN tar -xvzf lib/mariadb-connector-odbc-3.1.7-ga-rhel7-x86_64.tar.gz &&\
install lib64/libmaodbc.so /usr/lib64/ &&\
install -d /usr/lib64/mariadb/ &&\
install -d /usr/lib64/mariadb/plugin/ &&\
install lib64/mariadb/plugin/auth_gssapi_client.so /usr/lib64/mariadb/plugin/ &&\
install lib64/mariadb/plugin/caching_sha2_password.so /usr/lib64/mariadb/plugin/ &&\
install lib64/mariadb/plugin/client_ed25519.so /usr/lib64/mariadb/plugin/ &&\
install lib64/mariadb/plugin/dialog.so /usr/lib64/mariadb/plugin/ &&\
install lib64/mariadb/plugin/mysql_clear_password.so /usr/lib64/mariadb/plugin/ &&\
install lib64/mariadb/plugin/sha256_password.so /usr/lib64/mariadb/plugin/

RUN pip3 install -r requirements.txt

ENV PYTHONPATH /app/
EXPOSE 3307
EXPOSE 80

CMD python3 src/app.py
