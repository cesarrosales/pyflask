# pyflask
Minimal Flask API project using a clean, layered architecture (routes, services, repositories, models).

## Setup

### Set up environment
```sh
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt

```

### Run with Docker
```sh
# running on 5001 for docker
docker build -t pyflask .  
pyflask % docker run --rm -p 5001:5000 --env-file .env.docker.lcl pyflask
```

### Notes

- Endpoints use Auth0 provider
- If using VS Code, select the `.venv` interpreter 