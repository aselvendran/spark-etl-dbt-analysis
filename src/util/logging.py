from util.spark import spark_build


class LoggerSpark:
    def __init__(self):
        self.spark = spark_build()

    def get_logger(self):
        conf = self.spark.sparkContext.getConf()
        logging = self.spark._jvm.org.apache.log4j
        application_id = conf.get('spark.app.id')
        application_name = conf.get('spark.app.name')

        return logging.LogManager.getLogger(f"{application_name}_{application_id}")
