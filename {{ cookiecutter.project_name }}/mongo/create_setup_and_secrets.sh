#!/usr/bin/bash
# 
# This file creates a .env file and a mongo-init.js file in the current directory
# from the environment variables currently present in the shell running the script
# This is helpful to generate these required files when instancing the docker for
# the first time.
# 

set -e

function usage(){
    cat << "EOF"
this script needs the environment variables $MONGO_INITDB_ROOT_USERNAME, $MONGO_INITDB_ROOT_PASSWORD, $MONGO_INITDB_DATABASE
to create the database.
please refer to the README for more informations.
EOF
    exit 1
}

MONGO_INIT_FILE=mongo-init.js

# if the database was never initialized and the init script does not exist, create it
if [[ ( ! -d 'mongo' ) ]]; then
    echo "creating "$MONGO_INIT_FILE" ..."
    [ -z "$MONGO_INITDB_ROOT_USERNAME" ] && usage
    [ -z "$MONGO_INITDB_ROOT_PASSWORD" ] && usage
    [ -z "$MONGO_INITDB_USER_USERNAME" ] && usage
    [ -z "$MONGO_INITDB_USER_PASSWORD" ] && usage
    [ -z "$MONGO_INITDB_DATABASE" ] && usage
    [ -z "$MONGO_HOST" ] && usage
    
    cat <<EOF > "$MONGO_INIT_FILE"
db.createUser(
	{
		user: "$MONGO_INITDB_ROOT_USERNAME",
		pwd: "$MONGO_INITDB_ROOT_PASSWORD",
		roles: [{
			role: "dbAdmin",
			db: "$MONGO_INITDB_DATABASE"
		},
        {
			role: "readWrite",
			db: "$MONGO_INITDB_DATABASE"
        }
        ]
	}
)

db.createUser({
    user: "$MONGO_INITDB_USER_USERNAME",
    pwd: "$MONGO_INITDB_USER_PASSWORD",
    roles: [
        {
            role: "userAdminAnyDatabase",
            db: "admin",
        },
        {
            role: "dbAdminAnyDatabase",
            db: "admin",
        },
        {
            role: "readWriteAnyDatabase",
            db: "admin",
        },
    ]
})

EOF

    
fi
