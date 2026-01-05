# Three-Tier Serverless Web Application on AWS

A complete three-tier serverless web application built with AWS services, following cloud architecture best practices.

<img width="946" height="568" alt="diagram" src="https://github.com/user-attachments/assets/0c399aa3-282f-4e9d-8347-934ef514f8c4" />

https://github.com/user-attachments/assets/88643cdb-4152-41b8-8e15-2cafea487b62

---

## 🏗 Architecture Overview

This application uses a clean separation of concerns across three layers:

- **Presentation Layer** – Amazon S3 hosts static files, CloudFront delivers content globally  
- **Logic Layer** – API Gateway exposes REST endpoints, Lambda functions handle business logic  
- **Data Layer** – DynamoDB stores user data in a NoSQL database  

The data flows from the user to CloudFront, through the S3 frontend, to API Gateway, Lambda functions, and finally DynamoDB.

---

## 🧰 Technology Stack

The application leverages AWS serverless services:

- **S3** for storage  
- **CloudFront** for CDN  
- **Lambda** for compute  
- **API Gateway** for REST APIs  
- **DynamoDB** for data persistence  

---

## 📋 Prerequisites

You’ll need:

- An active **AWS account** with configured credentials  
- **AWS CLI** installed  
- Appropriate **IAM permissions**  
- **Git**  
- A **code editor**  

Basic familiarity with AWS services is helpful.

---

## 🚀 Quick Deployment

### 1️⃣ Database Setup
Create a DynamoDB table called **`UsersTable`** and populate it with sample user data using the AWS CLI.

### 2️⃣ Backend Configuration
Deploy a Lambda function using the **Python 3.12** runtime.  
Attach the **DynamoDB read-only** policy to the execution role so Lambda can query the database.

### 3️⃣ API Creation
Build a REST API in API Gateway with a **`/users`** resource and **GET** method.  
Enable **CORS** and deploy to a **production stage**.  
Copy the **Invoke URL** for frontend integration.

### 4️⃣ Frontend Deployment
Create an **S3 bucket** for static files and configure a **CloudFront distribution** as the CDN.  
Update the bucket policy to allow CloudFront access.  
Set **`index.html`** as the default root object.

### 5️⃣ Integration
Update the frontend JavaScript with your **API Gateway URL**, then sync the files to S3.  
Invalidate the **CloudFront cache** to see changes immediately.

---

## 🧪 Testing Your Application

- Test the API endpoint directly using **curl** with a `userId` parameter  
- Open your **CloudFront URL** in a browser to interact with the full application  

The interface should load user data dynamically through API calls.

---

## ⚠️ Common Issues

- **403 errors**  
  Usually indicate bucket permission problems or cache issues.  
  Check your bucket policy and invalidate the CloudFront cache.

- **CORS errors**  
  Verify headers in your Lambda function and ensure CORS is enabled in API Gateway.

- **User not found errors**  
  Check that the data exists in DynamoDB and that Lambda has the correct permissions.

---

## 💰 Cost Estimate

This architecture is extremely cost-effective for development and low-traffic applications.  
Most services fall within the **AWS Free Tier**, with estimated costs **under $1 per month** for typical usage.

---

## 🧹 Cleanup

To avoid ongoing charges, delete resources in this order:

1. CloudFront distribution  
2. S3 bucket  
3. API Gateway  
4. Lambda function  
5. DynamoDB table  
6. IAM roles  

---

## Final Notes

This project demonstrates **modern serverless architecture patterns on AWS**, making it ideal for learning cloud development or building scalable web applications without managing servers.

