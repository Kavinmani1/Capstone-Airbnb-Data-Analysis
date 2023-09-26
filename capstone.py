from pyspark.sql import SparkSession
from pyspark.sql.functions import col, lit, coalesce, regexp_replace, when
from pyspark.sql.functions import trim
from pyspark.sql.functions import lower
from pyspark.sql import functions as F
from pyspark.sql.functions import concat_ws, lit
from pyspark.sql.functions import udf
from pyspark.sql.types import StringType
if __name__ == "__main__":
    # Create a SparkSession
    spark = SparkSession.builder \
        .appName("Market Analysis") \
        .config("spark.sql.shuffle.partitions", 3) \
        .enableHiveSupport() \
        .getOrCreate()

    # Access Hive table
    df = spark.read.table("capstone.listings_airbnb")
    df.show(5)

    PriceNew = df.withColumn("price", regexp_replace(col("price"), "[$,]", "").cast("double"))

    # Fill missing values in reviews_per_month with 0
    convert1 = convert.withColumn("reviews_per_month", coalesce(col("reviews_per_month"), lit(0.0)))

    # Handling missing values in neighbourhood_group_cleansed column
    convert2 = convert1.withColumn("neighbourhood_group_cleansed", coalesce(col("neighbourhood_group_cleansed"), lit("Unknown")))

    # Handling missing values in calculated_host_listings_count column
    dataProcessed = convert2.withColumn("calculated_host_listings_count", when(col("calculated_host_listings_count").isNull(), 0).otherwise(col("calculated_host_listings_count")))

 df = dataProcessed.withColumn("city", trim(df["city"]))

    df = df.withColumn("city", lower(df["city"]))

    df = df.fillna({"reviews_per_month": 0.0, "last_review": "N/A"})


    def custom_transform(amenities):
    # Implement your custom logic here
    # For example, you can split the amenities string and count the number of amenities
        return str(amenities).count('&')

    # Register the UDF
        custom_udf = udf(custom_transform, StringType())
    
    # Apply the UDF to create a new column
        df = df.withColumn("num_amenities", custom_udf(col("amenities")))

    # Show the first few rows of the processed DataFrame
    df.show(20)

    # Create a DataFrame from the previously processed data
    airbnb_data = df

    # Run a Spark SQL query to count the number of listings per city
    query1 = airbnb_data.groupBy("city").count().withColumnRenamed("count", "listing_count")
    query1.show()

    # Run a Spark SQL query to calculate the average price per night for listings in each city
    query2 = airbnb_data.select("city", "price") \
        .withColumn("price", regexp_replace(col("price"), "[$,]", "").cast("decimal(10,2)")) \
        .groupBy("city") \
        .agg({"price": "avg"}) \
        .withColumnRenamed("avg(price)", "avg_price_per_night") \
        .orderBy("city")
    query2.show()


     # Additional analysis: Calculate maximum and minimum prices for each neighborhood and room type combination
    query3 = airbnb_data.groupBy("host_name", "neighbourhood", "room_type") \
            .agg(F.min("price").alias("min_price"), F.max("price").alias("max_price"), F.first("host_id").alias("host_id")) \
            .show()


    # Analyze room type trends using SQL queries
    query4 = airbnb_data.groupBy("room_type") \
        .agg({"price": "avg", "price": "max", "price": "min", "room_type": "count"}) \
        .withColumnRenamed("avg(price)", "avg_price") \
        .withColumnRenamed("max(price)", "max_price") \
        .withColumnRenamed("min(price)", "min_price") \
        .withColumnRenamed("count(room_type)", "listing_count") \
        .orderBy("room_type")
    query4.show()


    #  Number of listings by room type
    query5 = airbnb_data.groupBy("room_type").count().orderBy(col("count").desc())
    query5.show()

    #  Average minimum nights by neighborhood and room type
    query6 = airbnb_data.groupBy("neighbourhood", "room_type") \
        .agg({"minimum_nights": "avg"}) \
        .withColumnRenamed("avg(minimum_nights)", "avg_min_nights") \
        .orderBy("neighbourhood" )
    query6.show()


    query7 = airbnb_data.groupBy("host_name").count().orderBy(col("count").desc()).limit(10)
    query7.show()


    df.write.mode("overwrite").option("header", "true").saveAsTable("capstone.airbnb_transform")

    # Stop the SparkSessio
    spark.stop()
                  
