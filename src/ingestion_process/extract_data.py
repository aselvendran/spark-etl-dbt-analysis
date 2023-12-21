import os
import json
import re

from util.spark import spark_build
from util.logging import LoggerSpark
from pyspark.sql import DataFrame
from pyspark.sql import functions as SparkFunc


class ExtractData:
    def __init__(self):
        self.spark = spark_build()
        self.logging = LoggerSpark().get_logger()

    def get_data_from_storage(self, directory_to_file: str, file_type="json") -> DataFrame:
        """
        Load data from an arbitrary location into a Spark DF. The file types that are supported are json and any other
        file type supported by the pyspark read api.

        :param directory_to_file: directory path.
        :param file_type: type fo file.
        :return: Spark DataFrame
        """
        if file_type == 'json':
            return self.spark.read.option("mode", "PERMISSIVE").option("columnNameOfCorruptRecord",
                                                                       "_corrupt_record").json(
                directory_to_file)
        else:
            return self.spark.read.option("mode", "PERMISSIVE").option("columnNameOfCorruptRecord",
                                                                       "_corrupt_record").load(
                directory_to_file)

    def get_corrupt_data(self, df: DataFrame):
        """
        This method brings in corrupt data in memory and into a json format. Then we remove the cache to free up some
        space.

        :param df: Spark DataFrame containing corrupt record.
        :return: json containing corrupt records.
        """
        corrupt_data = df.filter(SparkFunc.col('_corrupt_record').isNotNull())
        corrupt_data.cache()
        corrupt_data_collected = corrupt_data.select("_corrupt_record").toJSON().collect()
        corrupt_data.unpersist()

        return corrupt_data_collected

    def log_corrupt_data(self, df: DataFrame, file_name: str):
        corrupt_data = self.get_corrupt_data(df)
        for corrupt_record in corrupt_data:
            corrupt_record_formatted = (json.loads(corrupt_record)['_corrupt_record'])
            error_position = re.findall('(?<=stream-position":")(.*)(?=","table-name")', corrupt_record_formatted)

            self.logging.warn({
                "filename": file_name,
                "row_number": error_position[0] if error_position else "",
                "error_reason": "Bad Parsing",
                "raw_line": corrupt_record
            })

    def log_error_for_bad_data_pull(self, df: DataFrame):
        """
        Log error if the percentage of bad data is about the threshold given by the user.
        :param df: DataFrame
        :return: None
        """
        corrupt_data = len(self.get_corrupt_data(df))
        total_data_length = df.count()
        error_threshold = os.environ.get('LOG_CORRUPT_ERROR', 10)

        if (corrupt_data / total_data_length) * 100 >= error_threshold:
            error_message = f"Bad Data loaded; exceeds threshold of {error_threshold}"
            self.logging.error(error_message)
            return error_message
