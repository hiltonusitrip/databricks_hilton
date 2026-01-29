
from pyspark import pipelines as dp
from pyspark.sql.functions import col
import dlt

@dp.table(
  name="bronze_customers",
  comment="Raw customer data from source system"
)
def bronze():
    return spark.readStream.format("cloudFiles") \
        .option("cloudFiles.format", "csv") \
        .option("header", True) \
        .option("inferSchema", "true") \
        .load("/Volumes/hilton_catalog/bronze/dataset/customer/")

        
dlt.create_streaming_table("customer_dim")

dlt.apply_changes(
  target="customer_dim",
  source="bronze_customers",
  keys=["id"],
  sequence_by=col("event_date"),
  stored_as_scd_type=2,
  track_history_column_list=["name"],
  ignore_null_updates=True
)

