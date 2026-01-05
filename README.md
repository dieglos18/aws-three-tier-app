# Three-Tier Serverless Web Application on AWS

A complete three-tier serverless web application built with AWS services, following cloud architecture best practices.

<img width="946" height="568" alt="diagram" src="https://github.com/user-attachments/assets/0c399aa3-282f-4e9d-8347-934ef514f8c4" />

https://github.com/user-attachments/assets/88643cdb-4152-41b8-8e15-2cafea487b62



## 🏗️ Architecture

This application implements a serverless three-tier architecture:

### Tier 1: Presentation Layer (Frontend)
- **Amazon S3**: Stores static files (HTML, CSS, JavaScript)
- **CloudFront**: CDN for global distribution and caching

### Tier 2: Logic Layer (Backend)
- **AWS Lambda**: Executes serverless functions
- **API Gateway**: Exposes REST API for the frontend

### Tier 3: Data Layer (Database)
- **DynamoDB**: NoSQL database for user data storage

### Data Flow
```
User → CloudFront → S3 (Frontend) → API Gateway → Lambda → DynamoDB
```

## 🛠️ Technologies

- **AWS S3** - Object storage
- **AWS CloudFront** - Content Delivery Network
- **AWS Lambda** - Serverless compute
- **AWS API Gateway** - REST API
- **AWS DynamoDB** - NoSQL database
- **Python 3.x** - Lambda runtime
- **JavaScript (Vanilla)** - Frontend
- **HTML5 & CSS3** - User interface

## 📋 Prerequisites

Before you begin, ensure you have:

- ✔️ Active AWS account ([Create account](https://aws.amazon.com))
- ✔️ AWS CLI installed ([Installation guide](https://docs.aws.amazon.com/cli/latest/userguide/getting-started-install.html))
- ✔️ AWS credentials configured (`aws configure`)
- ✔️ IAM permissions to create resources (S3, Lambda, DynamoDB, etc.)
- ✔️ Git installed
- ✔️ Code editor (VS Code recommended)

## 🚀 Deployment

### Step 1: Create DynamoDB Table
```bash
# Create the table
aws dynamodb create-table \
    --cli-input-json file://infrastructure/dynamodb-setup.json \
    --region us-east-1

# Wait for the table to become active
aws dynamodb wait table-exists --table-name UsersTable --region us-east-1

# Insert sample data
aws dynamodb put-item \
    --table-name UsersTable \
    --item '{"userId": {"S": "1"}, "name": {"S": "Diego Losada"}, "email": {"S": "diego@example.com"}, "role": {"S": "Student"}}' \
    --region us-east-1

aws dynamodb put-item \
    --table-name UsersTable \
    --item '{"userId": {"S": "2"}, "name": {"S": "Jane Smith"}, "email": {"S": "jane@example.com"}, "role": {"S": "Developer"}}' \
    --region us-east-1
```

### Step 2: Create Lambda Function

#### Option A: Using AWS Console

1. Go to [AWS Lambda Console](https://console.aws.amazon.com/lambda)
2. Click **"Create function"**
3. Select **"Author from scratch"**
4. Configuration:
   - **Function name**: `GetUserFunction`
   - **Runtime**: Python 3.12
   - **Architecture**: x86_64
5. Click **"Create function"**
6. Copy the content from `backend/lambda_function.py` into the editor
7. Click **"Deploy"**

#### Configure Permissions:

1. In the Lambda function, go to **Configuration** → **Permissions**
2. Click on the execution role
3. Click **"Add permissions"** → **"Attach policies"**
4. Search and add: `AmazonDynamoDBReadOnlyAccess`
5. Save

### Step 3: Create API Gateway

1. Go to [API Gateway Console](https://console.aws.amazon.com/apigateway)
2. Click **"Create API"** → **"REST API"** → **"Build"**
3. Configuration:
   - **API name**: `UsersAPI`
   - **Endpoint Type**: Regional
4. Click **"Create API"**

#### Create Resource:

5. Click **"Actions"** → **"Create Resource"**
   - **Resource Name**: `users`
   - **Resource Path**: `/users`
6. Click **"Create Resource"**

#### Create GET Method:

7. Select the `/users` resource
8. Click **"Actions"** → **"Create Method"** → Select **"GET"**
9. Configuration:
   - **Integration type**: Lambda Function
   - **Lambda Function**: `GetUserFunction`
   - Check: **Use Lambda Proxy integration**
10. Click **"Save"** → **"OK"**

#### Enable CORS:

11. Select the `/users` resource
12. Click **"Actions"** → **"Enable CORS"**
13. Leave default values
14. Click **"Enable CORS and replace existing CORS headers"**

#### Deploy API:

15. Click **"Actions"** → **"Deploy API"**
16. **Deployment stage**: `[New Stage]`
17. **Stage name**: `prod`
18. Click **"Deploy"**

19. **Copy the Invoke URL** (something like):
```
    https://abc123xyz.execute-api.us-east-1.amazonaws.com/prod
```

### Step 4: Test the API
```bash
# Replace with your API URL
curl "https://YOUR-API-ID.execute-api.us-east-1.amazonaws.com/prod/users?userId=1"
```

You should see:
```json
{
  "userId": "1",
  "name": "Diego Losada",
  "email": "diego@example.com",
  "role": "Student"
}
```

### Step 5: Configure S3 and CloudFront

#### Create S3 Bucket:
```bash
# Create bucket (name must be globally unique)
aws s3 mb s3://my-three-tier-app-12345 --region us-east-1

# Upload frontend files
aws s3 sync frontend/ s3://my-three-tier-app-12345/ --acl private
```

#### Create CloudFront Distribution:

1. Go to [CloudFront Console](https://console.aws.amazon.com/cloudfront)
2. Click **"Create Distribution"**
3. **Origin domain**: Select your S3 bucket
4. **Origin access**: **Origin access control settings (recommended)**
5. Click **"Create control setting"** → **"Create"**
6. **Default root object**: `index.html`
7. Click **"Create distribution"**

8. **Update bucket permissions**:
   - CloudFront will show you a policy
   - Copy it
   - Go to your S3 bucket → **Permissions** → **Bucket policy**
   - Paste the policy
   - Click **"Save"**

9. Wait 10-15 minutes for the distribution to deploy

10. **Copy the CloudFront URL**:
```
    https://d123abc456def.cloudfront.net
```

### Step 6: Update Frontend with API URL
```bash
# Edit script.js
nano frontend/script.js
```

Replace the line:
```javascript
const API_URL = 'https://YOUR-API-ID.execute-api.YOUR-REGION.amazonaws.com/prod/users';
```

With your real URL:
```javascript
const API_URL = 'https://abc123xyz.execute-api.us-east-1.amazonaws.com/prod/users';
```
```bash
# Re-upload updated files
aws s3 sync frontend/ s3://my-three-tier-app-12345/ --acl private

# Invalidate CloudFront cache
aws cloudfront create-invalidation \
    --distribution-id YOUR-DISTRIBUTION-ID \
    --paths "/*"
```

## 🧪 Testing

### Test API Locally
```bash
curl "https://YOUR-API.execute-api.us-east-1.amazonaws.com/prod/users?userId=1"
```

### Test Web Application

1. Open your browser
2. Go to your CloudFront URL
3. You should see user data loaded
4. Test the buttons to load different users
5. Open **DevTools** (F12) → **Console** to see logs
6. Check the **Network** tab to see API calls

## 🔧 Troubleshooting

### ❌ Error 403 in CloudFront

**Problem**: Page won't load

**Solutions**:
```bash
# 1. Check bucket permissions
aws s3api get-bucket-policy --bucket my-three-tier-app-12345

# 2. Invalidate cache
aws cloudfront create-invalidation --distribution-id YOUR-ID --paths "/*"

# 3. Clear browser cache (Ctrl + Shift + Delete)
```

### ❌ CORS Error

**Problem**: "CORS policy: No 'Access-Control-Allow-Origin' header"

**Solutions**:
1. Verify headers are in `lambda_function.py`
2. Verify CORS is enabled in API Gateway
3. Redeploy the API in API Gateway

### ❌ User Not Found

**Problem**: 404 User not found

**Solutions**:
```bash
# Verify data exists in DynamoDB
aws dynamodb scan --table-name UsersTable --region us-east-1

# Insert data if missing
aws dynamodb put-item \
    --table-name UsersTable \
    --item '{"userId": {"S": "1"}, "name": {"S": "Diego"}, "email": {"S": "diego@test.com"}}' \
    --region us-east-1
```

### ❌ Lambda Without Permissions

**Problem**: "AccessDeniedException" in Lambda logs

**Solution**:
1. Go to Lambda → Configuration → Permissions
2. Ensure the role has `AmazonDynamoDBReadOnlyAccess`

## 📊 Estimated Costs

For a test application with low traffic:

- **S3**: ~$0.02/month
- **CloudFront**: ~$0.50/month
- **Lambda**: Free (free tier: 1M requests/month)
- **API Gateway**: Free (free tier: 1M calls/month)
- **DynamoDB**: Free (free tier: 25 GB)

**Estimated total**: < $1/month

## 🧹 Resource Cleanup

To avoid charges, delete all resources:
```bash
# 1. Delete CloudFront distribution (from console)
# 2. Delete S3 bucket
aws s3 rb s3://my-three-tier-app-12345 --force

# 3. Delete API Gateway
aws apigateway delete-rest-api --rest-api-id YOUR-API-ID

# 4. Delete Lambda function
aws lambda delete-function --function-name GetUserFunction

# 5. Delete DynamoDB table
aws dynamodb delete-table --table-name UsersTable

# 6. Delete IAM role
aws iam detach-role-policy \
    --role-name lambda-dynamodb-role \
    --policy-arn arn:aws:iam::aws:policy/AmazonDynamoDBReadOnlyAccess

aws iam delete-role --role-name lambda-dynamodb-role
```

## 📚 Additional Resources

- [AWS Lambda Documentation](https://docs.aws.amazon.com/lambda/)
- [API Gateway Documentation](https://docs.aws.amazon.com/apigateway/)
- [DynamoDB Documentation](https://docs.aws.amazon.com/dynamodb/)
- [NextWork Projects](https://nextwork.org)

## 👨‍💻 Author

**Diego Losada** - NextWork Student

⭐ If this project was helpful, give it a star on GitHub!
