from forgeflow.sinks.bigquery import BigQuerySink
from forgeflow.sinks.duckdb import DuckDBSink
from forgeflow.sinks.file import FileSink
from forgeflow.sinks.mongodb import MongoDBSink
from forgeflow.sinks.postgres import PostgresSink
from forgeflow.sinks.s3 import S3Sink

__all__ = [
    "PostgresSink",
    "DuckDBSink",
    "FileSink",
    "BigQuerySink",
    "S3Sink",
    "MongoDBSink",
]
