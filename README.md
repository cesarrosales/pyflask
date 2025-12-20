# pyflask
Minimal Flask API project using a clean, layered architecture (routes, services, repositories, models).

## Setup

### Set up environment
```sh
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt

```

### Flask Commands
```sh
# list routes
flask --app app.wsgi routes
```

### Run with Docker
```ssh
# running on 5001 for docker
docker build -t pyflask .  
pyflask % docker run --rm -p 5001:5000 --env-file .env.docker.lcl pyflask
```

### Notes

- If using VS Code, select the `.venv` interpreter  