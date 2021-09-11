
#!/bin/sh

CMD="$1"
shift

case "$CMD" in
    ""|prod*)
        docker-compose -f docker-compose.yml -f production.yml up --abort-on-container-exit $@
        ;;
    dev)
        docker-compose -f docker-compose.yml  -f development.yml -f frontend.yml up --abort-on-container-exit $@
        ;;
    init)
        echo "setting secrets..."
        ./init_secrets.sh
        echo "initializing frontend dependencies..."
        docker-compose -f frontend.yml -f init_frontend.yml up --build --abort-on-container-exit $@
        ;;
    update-frontend)
        docker-compose -f frontend.yml -f update_frontend.yml up --build --abort-on-container-exit $@
        ;;
    build*)
        docker-compose -f frontend.yml -f build-frontend.yml up --abort-on-container-exit $@
        ;;
    lint*)
        docker exec -it {{ cookiecutter.project_name }}_vuecli_1 npm run lint
        ;;
    dump-db)
        docker exec -it {{ cookiecutter.project_name }}_mongo_docker sh -c "mongodump --username $MONGO_INITDB_ROOT_USERNAME --password $MONGO_INITDB_ROOT_PASSWORD --db thedb --out /dumps/dump_$(date +'%Y-%m-%d_%H-%M-%S')"
        ;;
    restore-db)
        docker exec -i {{ cookiecutter.project_name }}_mongo_docker sh -c "mongorestore --username $MONGO_INITDB_ROOT_USERNAME --password $MONGO_INITDB_ROOT_PASSWORD /dumps/$1"
        ;;
    connect-db)
        . ./mongo/.env
        case "$1" in
            user)
                user=$MONGO_INITDB_USER_USERNAME
                pass=$MONGO_INITDB_USER_PASSWORD
            ;;
            root)
                user=$MONGO_INITDB_ROOT_USERNAME
                pass=$MONGO_INITDB_ROOT_PASSWORD
            ;;
        esac
        docker exec -it {{ cookiecutter.project_name }}_mongo_docker mongo --username $user --password $pass
        ;;
    dev-venv-create)
        python -m venv venv && . ./venv/bin/activate \
            && pip install -r backend/requirements.txt \
            ;;
    init)
        docker-compose -f docker-compose.yml -f frontend.yml build --no-cache && \
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

