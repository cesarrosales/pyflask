docker build -t pyflask .  
docker run --rm -p 5001:5000 --env-file .env.docker.lcl pyflask