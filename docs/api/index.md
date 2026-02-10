# API Reference

Complete API reference for ForgeFlow.

## Core Modules

### Connectors

- [BaseConnector](connectors.md#baseconnector) - Abstract base class for connectors
- [HTTPConnector](connectors.md#httpconnector) - Generic HTTP connector
- [RESTConnector](connectors.md#restconnector) - RESTful API connector

### Transformers

- [BaseTransformer](transformers.md#basetransformer) - Abstract base class
- [JSONNormalizer](transformers.md#jsonnormalizer) - JSON flattening transformer

### Sinks

- [BaseSink](sinks.md#basesink) - Abstract base class for sinks
- [PostgresSink](sinks.md#postgressink) - PostgreSQL sink
- [DuckDBSink](sinks.md#duckdbsink) - DuckDB sink
- [FileSink](sinks.md#filesink) - File-based sink

### Pipeline

- [PipelineLoader](pipeline.md#pipelineloader) - Load pipelines from YAML
- [PipelineExecutor](pipeline.md#pipelineexecutor) - Execute pipelines

### Utilities

- [RetryConfig](utilities.md#retryconfig) - Retry configuration
- [RateLimiter](utilities.md#ratelimiter) - Rate limiting
- [MemoryCache](utilities.md#memorycache) - In-memory caching
- [SchemaValidator](utilities.md#schemavalidator) - Data validation

## Usage Example

```python
import asyncio
from forgeflow.pipeline.loader import PipelineLoader
from forgeflow.pipeline.executor import PipelineExecutor

async def main():
    # Load pipelines
    pipelines = PipelineLoader.load_from_file('config/pipelines.yaml')
    
    # Execute
    executor = PipelineExecutor()
    for pipeline in pipelines:
        if pipeline.get('enabled', True):
            await executor.execute(pipeline)

asyncio.run(main())
```

## CLI Reference

See the [CLI documentation](cli.md) for command-line usage.
