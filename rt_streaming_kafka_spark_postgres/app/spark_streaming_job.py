import os
from pyspark.sql import SparkSession
from pyspark.sql.functions import from_json, col, to_timestamp, window
from pyspark.sql.types import StructType, StructField, StringType

KAFKA_BOOTSTRAP = os.getenv("KAFKA_BOOTSTRAP_SERVERS", "kafka:9092")
TOPIC = os.getenv("TOPIC_NAME", "clickstream")

PG_URL = f"jdbc:postgresql://{os.getenv('PG_HOST','postgres')}:{os.getenv('PG_PORT','5432')}/{os.getenv('PG_DB','analytics')}"
PG_USER = os.getenv("PG_USER", "postgres")
PG_PASSWORD = os.getenv("PG_PASSWORD", "postgres")
PG_PROPS = {"user": PG_USER, "password": PG_PASSWORD, "driver": "org.postgresql.Driver"}

spark = (
    SparkSession.builder
    .appName("KafkaToPostgresClickstream")
    .getOrCreate()
)
spark.sparkContext.setLogLevel("WARN")

raw_df = (
    spark.readStream
         .format("kafka")
         .option("kafka.bootstrap.servers", KAFKA_BOOTSTRAP)
         .option("subscribe", TOPIC)
         .option("startingOffsets", "earliest")
         .load()
)

schema = StructType([
    StructField("event_id", StringType()),
    StructField("user_id", StringType()),
    StructField("ts", StringType()),
    StructField("url", StringType()),
    StructField("referrer", StringType()),
    StructField("ua", StringType()),
    StructField("ip", StringType()),
])

json_df = raw_df.selectExpr("CAST(value AS STRING) as json_str")
parsed = json_df.select(from_json(col("json_str"), schema).alias("d")).select("d.*")

events = (
    parsed
    .withColumn("event_ts", to_timestamp(col("ts")))
    .drop("ts")
    .dropna(subset=["event_id","event_ts","url"])
    .dropDuplicates(["event_id"])
)

def write_raw_to_pg(batch_df, batch_id):
    (batch_df
        .select("event_id","user_id","event_ts","url","referrer","ua","ip")
        .write
        .mode("append")
        .jdbc(PG_URL, "clickstream_events", properties=PG_PROPS))

raw_query = (
    events.writeStream
          .outputMode("update")
          .foreachBatch(write_raw_to_pg)
          .option("checkpointLocation", "/tmp/chk_raw")
          .start()
)

agg = (
    events
    .withWatermark("event_ts", "2 minutes")
    .groupBy(
        window(col("event_ts"), "1 minute"),
        col("url")
    )
    .count()
    .withColumnRenamed("count", "hits")
)

def write_agg_to_pg(batch_df, batch_id):
    (batch_df
        .select(
            col("window.start").alias("window_start"),
            col("window.end").alias("window_end"),
            col("url"),
            col("hits")
        )
        .write
        .mode("append")
        .jdbc(PG_URL, "clickstream_agg_minute", properties=PG_PROPS))

agg_query = (
    agg.writeStream
       .outputMode("update")
       .foreachBatch(write_agg_to_pg)
       .option("checkpointLocation", "/tmp/chk_agg")
       .start()
)

raw_query.awaitTermination()
agg_query.awaitTermination()
