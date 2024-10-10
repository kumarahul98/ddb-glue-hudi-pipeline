# AWS SAM Template for Streaming Data Pipeline

## Introduction

This AWS Serverless Application Model (SAM) template sets up a streaming data pipeline that integrates AWS DynamoDB, Kinesis, and AWS Glue. The pipeline captures data changes in DynamoDB using Kinesis Data Streams, processes the data in real-time with AWS Glue, and writes the transformed data into a Hudi table in Amazon S3. This serverless architecture enables scalable, cost-effective data processing without managing any infrastructure.

## Resources Deployed

This SAM template deploys the following resources:

- **S3 Bucket**: Stores data and checkpoints for the Glue job.
- **DynamoDB Table**: Captures application data with a primary key and sort key.
- **DynamoDB Stream**: Streams changes from the DynamoDB table to Kinesis.
- **Kinesis Stream**: Handles the streaming data from DynamoDB.
- **AWS Glue Database**: Organizes the metadata for the Glue jobs.
- **AWS Glue Table**: Defines the structure of the data to be processed by Glue.
- **AWS Glue Job**: Executes the data transformation and writing to the Hudi table.
- **IAM Role**: Grants the necessary permissions for the Glue job to access other AWS resources.

## Prerequisites

Before deploying this SAM template, ensure you have the following:

- An AWS account with permissions to create the specified resources.
- AWS CLI configured with appropriate IAM user credentials.
- AWS SAM CLI installed.

## Deployment Instructions

1. **Clone the Repository**: Clone the repository containing the SAM template to your local machine.

   ```bash
   git clone <repository-url>
   cd <repository-directory>/aws-sam-template
   ```

2. Build and Deploy the SAM Application: Run the following command to build your application:

   ```bash
   sam build && sam deploy --guided
   ```
