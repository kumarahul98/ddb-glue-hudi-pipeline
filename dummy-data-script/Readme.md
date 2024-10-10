# DynamoDB Sample e-commerce Data Insertion Script

## Overview

This Python script generates and inserts sample data into an AWS DynamoDB table. It creates records for products, customers, and transactions, allowing you to populate your DynamoDB table with realistic data for testing or demonstration purposes. The script utilizes the `boto3` library to interact with AWS services and `names` for generating random customer names.

## Prerequisites

Before running the script, ensure you have the following:

- **AWS Account**: You need access to an AWS account with permissions to use DynamoDB.
- **AWS CLI Configured**: The AWS CLI should be configured with your credentials and region.
- **Python Environment**: Ensure Python is installed, along with the required libraries.

### Required Libraries

You need to install the following Python libraries:

```bash
pip3 install -r requirements.txt
```

### File config

#! config - Update these variable
table_name = "dynamodb-glue-hudi-pipeline-DynamoDBTable" # Name of your DynamoDB table
record_count = 1 # Number of records to generate for each entity type

### Run the script

You need to install the following Python libraries:

```bash
python3 ecom-dummy-data.py
```

### Functionality

The script includes a list of predefined products, each with attributes like name, price, and description. It generates the following types of sample data:

1. Product: Creates product records with a primary key (PK), sort key (SK), product name, price, and description.
2. Customer: Generates customer records with a primary key, sort key, full name, and email address.
3. Transaction: Creates transaction records with a primary key, sort key, transaction date, total amount, and a list of purchased products.
