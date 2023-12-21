import pytest
from src.ingestion_process.extract_data import ExtractData


@pytest.mark.usefixtures("spark")
def test_sample_transform(spark):
    extraction = ExtractData()
    bad_json = """
     {
      "Hello:"
      "World":

   }
    """
    df = spark.read.json(spark.sparkContext.parallelize([bad_json]), multiLine=True)

    error_message = extraction.log_error_for_bad_data_pull(df)

    assert 'Bad Data loaded; exceeds threshold of 10' == error_message
