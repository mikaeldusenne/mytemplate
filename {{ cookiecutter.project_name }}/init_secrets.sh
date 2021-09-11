#!/bin/sh

function pwd(){
    < /dev/urandom tr -dc A-Za-z0-9 | head -c${1:-64};echo;
}

########
cd backend
echo "generating flask secret key..."
echo "FLASK_SECRET_KEY=$(pwd)" >> .env


########
cd ../mongo
echo "generating mongo user credentials..."

cat <<EOF > .env
export MONGO_PORT=27017
export MONGO_INITDB_DATABASE=thedb
export MONGO_HOST=wikimesh_mongo_docker

export MONGO_INITDB_ROOT_USERNAME=mongo_root
export MONGO_INITDB_ROOT_PASSWORD=$(pwd)

export MONGO_INITDB_USER_USERNAME=mongo_user
export MONGO_INITDB_USER_PASSWORD=$(pwd)

EOF

source ./.env
./create_setup_and_secrets.sh

