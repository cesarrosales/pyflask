# pyflask
Minimal Flask API project deployable to AWS Lambda as a container image, using a clean, layered architecture (routes, services, repositories, models).

## Setup

### Set up environment
```sh
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt

```

### Run locally with Docker
```sh
# running on 5001 for docker
docker build -t pyflask .  
docker run --rm -p 5001:5000 --env-file .env.docker.lcl pyflask
```

### Deploy to AWS Lambda from Local (or use GitHub Action)
```sh
# Build + push Lambda-compatible image to ECR (required: buildx)
export AWS_REGION=us-west-2
export ACCOUNT_ID=$(aws sts get-caller-identity --query Account --output text)
export IMAGE_URI="$ACCOUNT_ID.dkr.ecr.$AWS_REGION.amazonaws.com/pyflask:lambda"

docker buildx build \
  --platform linux/amd64 \
  -f Dockerfile.lambda \
  -t "$IMAGE_URI" \
  --push \
  --provenance=false \
  --sbom=false \
  --output type=registry,oci-mediatypes=false \
  .

# Update the Lambda function to the new image
aws lambda update-function-code \
  --function-name pyflask \
  --image-uri "$IMAGE_URI" \
  --region "$AWS_REGION"

# Lambda Web Adapter env vars (required to avoid init timeouts)
aws lambda update-function-configuration \
  --function-name pyflask \
  --region "$AWS_REGION" \
  --environment "Variables={AWS_LWA_ASYNC_INIT=true,AWS_LWA_PORT=8080,AWS_LWA_READINESS_CHECK_PATH=/health,AWS_LWA_INVOKE_MODE=buffered}"
```

### Monitor AWS Lambda logs
```sh
aws logs tail /aws/lambda/pyflask --follow
```

### Notes

- Endpoints use Auth0 provider
- If using VS Code, select the `.venv` interpreter 
- `AWS_LWA_INVOKE_MODE` should be `buffered` instead of `response_stream` when not using API Gateway