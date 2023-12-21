from pyspark.sql import DataFrame
import pyspark.sql.functions as sparkFunc


class Transformations:
    def __init__(self, df):
        self.df = df

    def retrieve_data(self, primary_key, column_selections) -> DataFrame:
        """
        Simple filtering method that ensures only data that contains the primary key is part of the dataframe;
        with corrupt records getting pulled into the DataFrame, it best to ensure that this information does not
        get shared downstream.

        :param primary_key: primary key of the DataFrame.
        :param column_selections: columns to segment.
        :return: Spark DataFrame.
        """
        return self.df.select(*column_selections).filter(sparkFunc.col(primary_key).isNotNull())

    def segment_user_data(self) -> DataFrame: return self.retrieve_data("data.user_id", ["data.user_id",
                                                                                         "data.id",
                                                                                         "data.first_name",
                                                                                         "data.last_name",
                                                                                         "data.phone_verified",
                                                                                         "data.profile_finished",
                                                                                         "data.spam_opt_in",
                                                                                         "data.text_opt_in",
                                                                                         "data.user_flag",
                                                                                         "data.user_onboarded",
                                                                                         "data.username"])

    def segment_application_data(self) -> DataFrame: return self.retrieve_data("data.user_id",
                                                                               ["data.user_id",
                                                                                "data.application_approved",
                                                                                "data.application_complete",
                                                                                "data.application_received",
                                                                                "data.application_rejected",
                                                                                "data.application_reviewed",
                                                                                "data.application_submitted"
                                                                                ])

    def segment_click_data(self) -> DataFrame: return self.retrieve_data("data.user_id",
                                                                         ["data.user_id", "data.click_screen",
                                                                          "data.click_ts",
                                                                          "data.click_verified",
                                                                          "data.click_xy"])

    def segment_metadata_data(self) -> DataFrame: return self.retrieve_data("data.user_id",
                                                                            ["data.user_id",
                                                                             "metadata.commit-timestamp",
                                                                             "metadata.operation",
                                                                             "metadata.partition-key-type"
                                                                                , "metadata.record-type",
                                                                             "metadata.schema-name",
                                                                             "metadata.stream-position",
                                                                             "metadata.table-name"
                                                                                , "metadata.timestamp",
                                                                             "metadata.transaction-id",
                                                                             "metadata.transaction-record-id"])
