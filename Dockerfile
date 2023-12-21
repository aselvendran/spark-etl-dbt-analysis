FROM gcr.io/datamechanics/spark:platform-3.1-dm14

USER root

WORKDIR /opt/application/

RUN wget  https://jdbc.postgresql.org/download/postgresql-42.7.0.jar
RUN mv postgresql-42.7.0.jar /opt/spark/jars

COPY src src/.
ENV PYTHONPATH "${PYTHONPATH}:/opt/application/src"
RUN pip3 install pyspark==3.5.0

ENTRYPOINT ["/bin/bash", "-l", "-c"]
