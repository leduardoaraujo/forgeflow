# Core Concepts

Understanding ForgeFlow's architecture and core concepts will help you build better data pipelines.

## Architecture Overview

ForgeFlow follows a simple, composable architecture:

```
┌─────────────┐
│  Connector  │ ──> Fetch data from source
└──────┬──────┘
       │
       ▼
┌─────────────┐
│ Transformer │ ──> Transform and normalize data
└──────┬──────┘
       │
       ▼
┌─────────────┐
│    Sink     │ ──> Load data to destination
└─────────────┘
```

## Components

### 1. Connectors

Connectors are responsible for **fetching data** from external sources.

**Built-in Connectors:**
- `http` - Generic HTTP requests
- `rest` - RESTful API client with base URL patterns

**Example:**
```yaml
connector:
  type: http
  config:
    url: https://api.example.com/data
    method: GET
    headers:
      Authorization: Bearer ${API_TOKEN}
```

### 2. Transformers

Transformers **process and normalize** the fetched data.

**Built-in Transformers:**
- `json_normalizer` - Flatten nested JSON structures

**Example:**
```yaml
transformer:
  type: json_normalizer
  config:
    flatten: true
    separator: "_"
```

### 3. Sinks

Sinks **write data** to destinations.

**Built-in Sinks:**
- `postgres` - PostgreSQL database
- `duckdb` - DuckDB analytical database
- `file` - Local files (JSON, JSONL, Parquet)

**Example:**
```yaml
sinks:
  - type: duckdb
    config:
      database: data/warehouse.duckdb
      table: users
      mode: append
```

## Pipeline Lifecycle

1. **Configuration Loading** - Parse YAML and validate
2. **Connector Initialization** - Setup connection to source
3. **Data Fetching** - Retrieve data asynchronously
4. **Transformation** - Process data through transformer
5. **Writing** - Load data to all configured sinks
6. **Cleanup** - Close connections and cleanup resources

## Async-First Design

ForgeFlow is built with `asyncio` for better performance:

```python
import asyncio
from forgeflow.pipeline.executor import PipelineExecutor
from forgeflow.pipeline.loader import PipelineLoader

async def main():
    pipelines = PipelineLoader.load_from_file('config/pipelines.yaml')
    executor = PipelineExecutor()
    
    for pipeline in pipelines:
        await executor.execute(pipeline)

asyncio.run(main())
```

## Configuration as Code

Pipelines are defined in YAML for:
- **Version Control** - Track changes in git
- **Declarative** - What, not how
- **Readable** - Non-programmers can understand
- **Portable** - Easy to share and deploy

## Error Handling

ForgeFlow includes built-in utilities:

- **Retry Logic** - Automatic retries with exponential backoff
- **Rate Limiting** - Respect API rate limits
- **Validation** - Schema validation with Pydantic
- **Structured Logging** - Debug-friendly logs

## Next Steps

- [Configuration Reference](configuration.md)
- [Building Custom Components](extending.md)
- [Airflow Integration](airflow.md)
