
*** iot-scraper *** 
Purpose:
The repo is aimed at loading data from iot devices to MariaDB.

Prerequisites:
1) Ubuntu environment for executing python code.
2) Particle photon device that is publishing data to particle.io
3) Available MariaDb database accessible.


Installation Guidelines:
1) Obtain Ubuntu 
2) Set up virtual environment
3) Run pip install -r requirements.txt
4) Install MariaDB drivers on Ubuntu Operating system (see Instructions: Install MariaDB drivers)

Instructions:
*** conf_copy.sh (optional) ***
If you add a shell script called conf_copy.sh containing containing bash scripts copying 
the config file to the repo, the config.py will execute that before failing

*** Install MariaDB drivers ***
To install MariaDB sql drivers follow below instructions.

mkdir odbc_package
cd odbc_package
wget https://downloads.mariadb.com/Connectors/odbc/connector-odbc-3.1.7/mariadb-connector-odbc-3.1.7-ga-debian-x86_64.tar.gz
tar -xvzf mariadb-connector-odbc-3.1.7-ga-debian-x86_64.tar.gz
sudo install lib64/libmaodbc.so /usr/lib/
sudo install -d /usr/lib/mariadb/
sudo install -d /usr/lib/mariadb/plugin/
sudo install lib/mariadb/plugin/auth_gssapi_client.so /usr/lib/mariadb/plugin/
sudo install lib/mariadb/plugin/caching_sha2_password.so /usr/lib/mariadb/plugin/
sudo install lib/mariadb/plugin/client_ed25519.so /usr/lib/mariadb/plugin/
sudo install lib/mariadb/plugin/dialog.so /usr/lib/mariadb/plugin/
sudo install lib/mariadb/plugin/mysql_clear_password.so /usr/lib/mariadb/plugin/
sudo install lib/mariadb/plugin/sha256_password.so /usr/lib/mariadb/plugin/

