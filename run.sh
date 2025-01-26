git pull origin master

docker build -t korotkova-admin-python-3.11:latest .

docker compose up -d admin bot celery

# Removing all dangling build cache
docker builder prune --force

# Removing all dangling images
docker rmi $(docker images --filter "dangling=true" -q --no-trunc)
