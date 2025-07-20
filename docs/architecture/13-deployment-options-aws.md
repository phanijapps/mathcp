# 13. Deployment Options (AWS)

## Option 1: AWS Lambda (Serverless) - Updated
- **Best for:** Stateless, scalable, pay-per-use math API with vector search
- **How:**
  - Package the `math_genius` library with ChromaDB as a Lambda Layer
  - Use Amazon EFS for persistent ChromaDB storage across Lambda invocations
  - Expose via AWS API Gateway (REST or HTTP API)
  - Use AWS SAM or Serverless Framework for deployment

## Option 2: AWS ECS (Fargate) - Recommended
- **Best for:** Containerized service with persistent vector search index
- **How:**
  - Build Docker image with math_genius + ChromaDB + vector index
  - Deploy to AWS ECS with Fargate (serverless containers)
  - Use EFS or EBS for persistent ChromaDB storage
  - Application Load Balancer for API exposure

## Option 3: AWS EC2 (Traditional VM)
- **Best for:** Custom environments with full control over vector search performance
- **How:**
  - Provision EC2 instance(s) with Python 3.12
  - Install ChromaDB and build vector index on local storage
  - Deploy as a service with optimal performance tuning

---
