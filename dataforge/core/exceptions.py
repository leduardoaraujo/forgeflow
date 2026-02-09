class DataForgeException(Exception):
    pass


class ConnectorException(DataForgeException):
    pass


class TransformerException(DataForgeException):
    pass


class SinkException(DataForgeException):
    pass


class ConfigurationException(DataForgeException):
    pass


class PipelineException(DataForgeException):
    pass
