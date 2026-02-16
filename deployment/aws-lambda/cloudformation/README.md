# FastAPI Serverless on AWS Lambda

Complete serverless FastAPI deployment using Lambda + API Gateway + CloudFront.

## Architecture
```
User → CloudFront (CDN) → API Gateway → Lambda (FastAPI)
```

## Cost (Low Traffic)

| Requests/Month | Cost |
|----------------|------|
| 10,000 | **~$0.20** |
| 100,000 | **~$2** |
| 1,000,000 | **~$20** |

Much cheaper than ECS for low traffic!

## Deployment
```bash
# Make scripts executable
chmod +x *.sh

# Deploy infrastructure
./deploy-lambda.sh

# Update Lambda code only
./package-lambda.sh
```

## Destroy
```bash
./destroy-lambda.sh
```

## Local Testing
```bash
# Install dependencies
pip install -r requirements.txt

# Run locally
uvicorn app.main:app --reload

# Test Lambda handler locally
python -c "from handler import handler; print(handler({'httpMethod': 'GET', 'path': '/'}, {}))"
```

## Limitations

- ⏱️ **15 minute** max execution time
- 💾 **10 GB** max memory
- 📦 **50 MB** deployment package (250 MB unzipped)
- ❄️ **Cold starts** (1-3 seconds first request)

## When to Use Lambda vs ECS

**Use Lambda if:**
- ✅ Low/variable traffic
- ✅ Cost-sensitive
- ✅ Simple stateless API
- ✅ Don't need persistent connections

**Use ECS if:**
- ✅ High consistent traffic
- ✅ Need WebSockets
- ✅ Long-running requests (>15min)
- ✅ Need persistent connections