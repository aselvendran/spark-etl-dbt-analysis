import time
import os

from util.logging import LoggerSpark

class TransferData:
    def __init__(self):
        pass

    def save_data(self, df, table_name, save_mode="append"):
        logging = LoggerSpark().get_logger()
        start_time = time.time()

        logging.info(f"saving data.. {table_name}")

        df.write.format("jdbc") \
            .option("url", f"jdbc:postgresql://{os.environ.get('POSTGRES_HOST','')}:{os.environ.get('POSTGRES_PORT','5432')}/{os.environ.get('POSTGRES_DB','')}") \
            .option("driver", "org.postgresql.Driver").mode(save_mode).option("dbtable", table_name) \
            .option("user", os.environ.get('POSTGRES_USER','')).option("password", os.environ.get('POSTGRES_PASSWORD','')).save()

        logging.info(f"data saved.. {table_name}. Took {round(time.time() - start_time, 2)} seconds.")
