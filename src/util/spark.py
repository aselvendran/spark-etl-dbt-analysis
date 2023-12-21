from pyspark.sql import SparkSession
from pathlib import Path


def spark_build():
    spark_builder = SparkSession.builder
    application_name = Path(__file__).parent.name
    return spark_builder.appName(application_name).getOrCreate()
