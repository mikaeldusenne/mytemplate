#!/bin/sh

CMD="$1"
shift

case "$CMD" in
    ""|prod*)
        docker-compose -f docker-compose.yml -f production.yml up --abort-on-container-exit $@
        ;;
    dev)
        docker-compose -f docker-compose.yml  -f development.yml -f front-end.yml up --abort-on-container-exit $@
        ;;
    update*)
        docker-compose -f front-end.yml -f update_frontend.yml up --abort-on-container-exit $@
        ;;
    build*)
        docker-compose -f front-end.yml -f build-front-end.yml up --abort-on-container-exit $@
        ;;
    lint*)
        docker exec -it {{ cookiecutter.project_name }}_vuecli_1 npm run lint
        ;;
    purge-db)
        docker exec -it {{ cookiecutter.project_name }}_app_1 python -m backend.src.mock
        ;;
    connect-db)
        . ./mongo/.env
        case "$1" in
            admin)
                user=$MONGO_INITDB_ADMIN_USERNAME
                pass=$MONGO_INITDB_ADMIN_PASSWORD
            ;;
            user)
                user=$MONGO_INITDB_ROOT_USERNAME
                pass=$MONGO_INITDB_ROOT_PASSWORD
            ;;
        esac
        docker exec -it {{ cookiecutter.project_name }}_mongo_docker mongo --username $user --password $pass --authenticationDatabase $MONGO_INITDB_DATABASE
        ;;
    dev-venv-create)
        python -m venv venv && . ./venv/bin/activate \
            && pip install -r backend/requirements.txt \
            ;;
    init)
        docker-compose -f docker-compose.yml -f front-end.yml build --no-cache && \
            ./run.sh update && \
            ./run.sh build --build && \
            ./run.sh 
        ;;
    stop)
        docker-compose down
        ;;
    *)
        echo "unknown argument"
        exit 1
        ;;
esac

