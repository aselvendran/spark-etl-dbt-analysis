import os

from extract_data import ExtractData
from transform_data import Transformations
from load_data import TransferData


def main():
    """ETL process to load data from an arbitrary location and then segment the data into 4 dimensions; users, clicks,
    application and metadata. Finally we save the data into a relational database.

    :return: None
    """

    extraction = ExtractData()
    raw_data = extraction.get_data_from_storage(os.environ.get('DATA_FILE_PATH', ''))

    # Log Corrupt Record.
    extraction.log_corrupt_data(raw_data, os.environ.get('DATA_FILE_PATH', ''))
    # Log Error if data quality is bad.
    extraction.log_error_for_bad_data_pull(raw_data)

    tf = Transformations(raw_data)
    segment_users = tf.segment_user_data()
    segment_application = tf.segment_application_data()
    segment_click = tf.segment_click_data()
    segment_metadata = tf.segment_metadata_data()

    transfer_data = TransferData()
    transfer_data.save_data(segment_users, 'users')
    transfer_data.save_data(segment_application, 'applications')
    transfer_data.save_data(segment_click, 'clicks')
    transfer_data.save_data(segment_metadata, 'metadata')


if __name__ == '__main__':
    main()
