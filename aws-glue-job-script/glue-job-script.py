try:
    from awsglue.transforms import *
    from pyspark.sql.session import SparkSession
    from awsglue.context import GlueContext
    from awsglue.utils import getResolvedOptions
    from pyspark.sql.functions import *
    import pyspark.sql.functions as F
    from awsglue import DynamicFrame
    import sys

except Exception as e:
    print("ERROR IMPORTS ", e)


def create_spark_session():
    spark = SparkSession.builder.config(
        "spark.serializer", "org.apache.spark.serializer.KryoSerializer"
    ).getOrCreate()
    return spark


args = getResolvedOptions(sys.argv, ["S3_BUCKET_NAME"])

spark = create_spark_session()
sc = spark.sparkContext
glueContext = GlueContext(sc)

# ====================== Configuration ============================================


db_name = "ddb_streaming_glue_database"
kinesis_table_name = "ddb_streaming_glue_table"

output_table_name = "ecom_ddb_data"

record_key = "PK_SK"
precomb = "PK_SK"
s3_bucket = args["S3_BUCKET_NAME"]
s3_path_hudi = f"s3a://{s3_bucket}/{output_table_name}/"
s3_path_spark = f"s3://{s3_bucket}/spark_checkpoints/{output_table_name}/"

print("output_table_name ", output_table_name)

method = "upsert"
table_type = "MERGE_ON_READ"

window_size = "10 seconds"
starting_position_of_kinesis_iterator = "trim_horizon"

connection_options = {
    "hoodie.table.name": output_table_name,
    "hoodie.datasource.write.storage.type": table_type,
    "hoodie.datasource.write.recordkey.field": record_key,
    "hoodie.datasource.write.table.name": output_table_name,
    "hoodie.datasource.write.operation": method,
    "hoodie.datasource.write.precombine.field": precomb,
    "hoodie.datasource.hive_sync.enable": "true",
    "hoodie.datasource.hive_sync.mode": "hms",
    "hoodie.datasource.hive_sync.sync_as_datasource": "false",
    "hoodie.datasource.hive_sync.database": db_name,
    "hoodie.datasource.hive_sync.table": output_table_name,
    "hoodie.datasource.hive_sync.use_jdbc": "false",
    "hoodie.datasource.hive_sync.partition_extractor_class": "org.apache.hudi.hive.MultiPartKeysValueExtractor",
    "hoodie.datasource.write.hive_style_partitioning": "true",
}

# ====================== Reading data from glue ============================================
data_frame_DataSource0 = glueContext.create_data_frame.from_catalog(
    database=db_name,
    table_name=kinesis_table_name,
    transformation_ctx="DataSource0",
    additional_options={
        "inferSchema": "true",
        "startingPosition": starting_position_of_kinesis_iterator,
    },
)


# ====================== Business Logic ============================================
def process_batch(data_frame, batch_id):
    row_count = data_frame.count()
    print("row_count ", row_count)
    if row_count > 0:
        kinesis_dynamic_frame = DynamicFrame.fromDF(
            data_frame, glueContext, "from_kinesis_data_frame"
        )

        kinesis_spark_df = kinesis_dynamic_frame.toDF()
        # Remove top level nesting from event
        selected_fields = kinesis_spark_df.selectExpr("dynamodb.NewImage")

        ecom_dynamic_frame = DynamicFrame.fromDF(selected_fields, glueContext, "dyf")

        # remove Dynamodb Nesting
        unnest_ddb_json_df = ecom_dynamic_frame.unnest_ddb_json()

        kinesis_spark_df = unnest_ddb_json_df.toDF()

        # concat pk and sk to get unique id column
        df = kinesis_spark_df.withColumn(record_key, F.concat(F.col("PK"), F.col("SK")))

        print("##########")
        print("\n")
        print(df.show(3))
        print(df.printSchema())
        print("\n")

        try:
            df.write.format("hudi").options(**connection_options).mode("append").save(
                s3_path_hudi
            )
        except Exception as e:
            pass


# ====================== start data processing ============================================
glueContext.forEachBatch(
    frame=data_frame_DataSource0,
    batch_function=process_batch,
    options={"windowSize": window_size, "checkpointLocation": s3_path_spark},
)
