# AWS Glue Streaming Job Script

## Introduction

This script is designed to run as an AWS Glue job that processes streaming data from a Kinesis stream. It extracts relevant information from DynamoDB records, transforms the data, and writes it to an Hudi table stored in Amazon S3. This solution leverages the serverless capabilities of AWS Glue for real-time data processing.

## Overview of the Code

The script performs the following key operations:

1. **Import Required Libraries**: It imports necessary libraries from AWS Glue and PySpark to manage data frames and dynamic frames.
2. **Read Data from Kinesis**: Creates a data frame from the specified Kinesis stream table.
3. **Process Data in Batches**: Processes each batch of records, transforming the data and writing it to an Hudi table in S3.

## Hudi Properties Explained

The script uses several Hudi properties to define how data should be written to the Hudi table:

- **`hoodie.table.name`**: Specifies the name of the Hudi table to which data will be written. This should match the output table name defined in the script.

- **`hoodie.datasource.write.storage.type`**: Defines the storage type for the Hudi table. The script uses `MERGE_ON_READ`, which allows for a flexible querying approach where data is merged on read rather than during the write operation.

- **`hoodie.datasource.write.recordkey.field`**: Indicates the field to be used as the record key. This property is essential for uniquely identifying records in the Hudi table.

- **`hoodie.datasource.write.table.name`**: Sets the table name for the Hudi data source, which should also align with `hoodie.table.name`.

- **`hoodie.datasource.write.operation`**: Determines the write operation type. The script uses `upsert`, which allows for inserting new records or updating existing ones based on the record key.

- **`hoodie.datasource.write.precombine.field`**: Specifies the field to be used for resolving conflicts during upserts. This property ensures that the latest version of a record is retained.

- **`hoodie.datasource.hive_sync.enable`**: When set to `true`, it enables the synchronization of Hudi tables with Hive, making it easier to query the data using Hive or Presto.

- **`hoodie.datasource.hive_sync.database`**: Indicates the database in Hive where the Hudi table should be synced.

- **`hoodie.datasource.hive_sync.table`**: Defines the name of the table in Hive that corresponds to the Hudi table.

- **`hoodie.datasource.hive_sync.use_jdbc`**: When set to `false`, it specifies not to use JDBC for syncing with Hive.

- **`hoodie.datasource.hive_sync.partition_extractor_class`**: Specifies the class responsible for extracting partition information for Hive.

- **`hoodie.datasource.write.hive_style_partitioning`**: When set to `true`, it enables Hive-style partitioning for better organization and access of data.

## Conclusion

This AWS Glue script serves as a solid foundation for building a streaming data pipeline using Kinesis and Hudi. By configuring the appropriate Hudi properties, you can efficiently manage and query your streaming data while leveraging the scalability of AWS services.
