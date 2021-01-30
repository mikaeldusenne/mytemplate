#!/bin/bash
set -e

mkdir -p results

# ssh-keyscan github.com >> ~/.ssh/known_hosts


mv id_rsa_github.pub ~/.ssh/id_rsa.pub
mv id_rsa_github ~/.ssh/id_rsa

# HOMEDIR="/home/ec2-user"
# mv id_rsa_github.pub $HOMEDIR/.ssh/id_rsa.pub
# mv id_rsa_github $HOMEDIR/.ssh/id_rsa

git clone git@github.com:halfcrunchy/saturn.git

mv mongo.env saturn/mongo/.env

cd saturn

git checkout dev

# ln -s $(pwd)/mongo/ ../results/mongo

cd mongo
source .env
./create_setup_and_secrets.sh
cd ..

./run.sh build --build         | tee ../results/build.log
(sleep 60 && ./run.sh purge-db | tee ../results/filldb.log) &
./run.sh prod                  | tee ../results/prod.log

cp -Ri mongo/ ../results/mongo/
