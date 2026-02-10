<div align="center">
  <img src="logo_forgeflow.svg" alt="DataForge Logo" width="400"/>

  # DataForge

  Modern ETL Framework for API Ingestion and Data Distribution

  [![Python 3.11+](https://img.shields.io/badge/python-3.11+-blue.svg)](https://www.python.org/downloads/)
  [![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
  [![Code style: ruff](https://img.shields.io/badge/code%20style-ruff-000000.svg)](https://github.com/astral-sh/ruff)

</div>

---

## Overview

DataForge is a modern ETL framework designed for API data ingestion, transformation, and distribution. Built with async-first architecture using Python 3.11+, it provides a declarative YAML-based configuration system for building robust data pipelines.

## Key Features

- Flexible connector system for HTTP and REST APIs
- Pluggable transformers for data normalization and processing
- Multiple sink support (PostgreSQL, DuckDB, BigQuery, S3, MongoDB, Snowflake)
- Async-first architecture with httpx and asyncio
- Built-in retry mechanism with exponential backoff
- Rate limiting and caching support
- Rich CLI with interactive commands
- FastAPI REST server for pipeline management
- Apache Airflow integration
- Structured logging with structlog
- Type-safe with full type hints

## Installation

### Basic Installation

```bash
pip install -e .
```

### With Optional Dependencies

```bash
# Database connectors
pip install -e ".[postgres,duckdb]"

# Cloud services
pip install -e ".[bigquery,s3,snowflake]"

# API server and orchestration
pip install -e ".[api,airflow]"

# All features
pip install -e ".[all]"

# Development
pip install -r requirements-dev.txt
```

## Quick Start

### 1. Configure Pipeline

Create `config/pipelines.yaml`:

```yaml
pipelines:
  - name: api_to_duckdb
    enabled: true
    connector:
      type: http
      config:
        url: https://api.example.com/data
        method: GET
        headers:
          Authorization: Bearer YOUR_TOKEN
        timeout: 30
    transformer:
      type: json_normalizer
      config:
        flatten: true
    sinks:
      - type: duckdb
        config:
          database: data/output.duckdb
          table: api_data
      - type: file
        config:
          path: data/json
          format: json
```

### 2. Run Pipeline

```bash
# CLI
dataforge run api_to_duckdb

# Python
python -c "
from dataforge.pipeline.executor import PipelineExecutor
from dataforge.pipeline.loader import PipelineLoader
import asyncio

pipelines = PipelineLoader.load_from_file('config/pipelines.yaml')
pipeline = next(p for p in pipelines if p['name'] == 'api_to_duckdb')

executor = PipelineExecutor()
asyncio.run(executor.execute(pipeline))
"
```

### 3. Query Results

```bash
duckdb data/output.duckdb -c "SELECT * FROM api_data LIMIT 10"
```

## CLI Commands

```bash
dataforge list              # List all configured pipelines
dataforge run <name>        # Execute a pipeline
dataforge test <name>       # Test pipeline connection
dataforge validate          # Validate configuration
dataforge init <name>       # Create new pipeline template
```

## Architecture

```
dataforge/
├── core/                   # Base interfaces and core functionality
│   ├── connector.py        # BaseConnector interface
│   ├── transformer.py      # BaseTransformer interface
│   ├── sink.py             # BaseSink interface
│   ├── retry.py            # Retry logic with tenacity
│   ├── rate_limiter.py     # Rate limiting
│   ├── cache.py            # Caching layer
│   └── validation.py       # Data validation
├── connectors/             # Data source implementations
│   ├── http.py             # Generic HTTP connector
│   └── rest.py             # RESTful API connector
├── transformers/           # Data transformation
│   └── json_normalizer.py  # JSON flattening and normalization
├── sinks/                  # Data destination implementations
│   ├── postgres.py         # PostgreSQL sink
│   ├── duckdb.py           # DuckDB sink
│   └── file.py             # File-based sink
├── pipeline/               # Pipeline orchestration
│   ├── executor.py         # Execution engine
│   └── loader.py           # Configuration loader
├── api/                    # REST API server
│   └── main.py             # FastAPI endpoints
├── airflow/                # Airflow integration
│   ├── operators.py        # Custom operators
│   ├── hooks.py            # Custom hooks
│   └── sensors.py          # Custom sensors
└── cli/                    # Command-line interface
    └── main.py             # CLI implementation
```

## Connectors

| Name | Description | Configuration |
|------|-------------|---------------|
| HTTP | Generic HTTP requests with custom headers and parameters | `url`, `method`, `headers`, `params`, `timeout` |
| REST | RESTful API client with base URL pattern | `base_url`, `endpoint`, `auth` |

## Transformers

| Name | Description | Configuration |
|------|-------------|---------------|
| JSON Normalizer | Flatten nested JSON structures | `flatten`, `separator`, `timestamp_field` |

## Sinks

| Name | Description | Installation |
|------|-------------|--------------|
| PostgreSQL | Relational database storage | `pip install -e ".[postgres]"` |
| DuckDB | Embedded analytical database | `pip install -e ".[duckdb]"` |
| BigQuery | Google Cloud data warehouse | `pip install -e ".[bigquery]"` |
| S3 | AWS object storage | `pip install -e ".[s3]"` |
| MongoDB | NoSQL document database | `pip install -e ".[mongodb]"` |
| Snowflake | Cloud data warehouse | `pip install -e ".[snowflake]"` |
| File | Local file storage (JSON, Parquet, CSV) | Built-in |

## Airflow Integration

```python
from airflow import DAG
from dataforge.airflow.operators import DataForgePipelineOperator
from dataforge.airflow.sensors import DataForgeApiSensor
from datetime import datetime, timedelta

default_args = {
    'owner': 'data-team',
    'retries': 3,
    'retry_delay': timedelta(minutes=5),
}

with DAG(
    'data_ingestion',
    default_args=default_args,
    schedule_interval='@daily',
    start_date=datetime(2024, 1, 1),
    catchup=False,
) as dag:

    check_api = DataForgeApiSensor(
        task_id='check_api_availability',
        pipeline_name='api_to_duckdb',
        timeout=300,
    )

    run_pipeline = DataForgePipelineOperator(
        task_id='ingest_data',
        pipeline_name='api_to_duckdb',
        config_path='config/pipelines.yaml',
    )

    check_api >> run_pipeline
```

## REST API

Start the server:

```bash
uvicorn dataforge.api.main:app --reload
```

Access interactive documentation at `http://localhost:8000/docs`

### Endpoints

- `GET /health` - Health check
- `GET /pipelines` - List all pipelines
- `POST /pipelines/{name}/run` - Execute pipeline
- `GET /pipelines/{name}/status` - Check pipeline status

## Advanced Configuration

### Retry Mechanism

```yaml
connector:
  type: http
  config:
    url: https://api.example.com/data
    retry:
      max_attempts: 3
      backoff_factor: 2
      max_delay: 60
```

### Rate Limiting

```yaml
connector:
  type: http
  config:
    url: https://api.example.com/data
    rate_limit:
      calls: 100
      period: 60
```

### Caching

```yaml
connector:
  type: http
  config:
    url: https://api.example.com/data
    cache:
      enabled: true
      ttl: 3600
      backend: memory
```

### Data Validation

```yaml
transformer:
  type: json_normalizer
  config:
    validate:
      schema: schemas/schema.json
      strict: true
```

## Extending DataForge

### Custom Connector

```python
from dataforge.core.connector import BaseConnector

class CustomConnector(BaseConnector):
    def validate_config(self) -> None:
        required = ["api_key", "endpoint"]
        missing = [k for k in required if k not in self.config]
        if missing:
            raise ValueError(f"Missing config: {missing}")

    async def fetch(self) -> dict:
        # Implementation
        return {}

    async def close(self) -> None:
        # Cleanup
        pass
```

### Custom Transformer

```python
from dataforge.core.transformer import BaseTransformer

class CustomTransformer(BaseTransformer):
    def validate_config(self) -> None:
        pass

    async def transform(self, data: dict) -> dict:
        # Implementation
        return data
```

### Custom Sink

```python
from dataforge.core.sink import BaseSink

class CustomSink(BaseSink):
    def validate_config(self) -> None:
        pass

    async def write(self, data: dict) -> None:
        # Implementation
        pass

    async def close(self) -> None:
        pass
```

## Testing

```bash
# Run all tests
pytest

# With coverage
pytest --cov=dataforge --cov-report=html

# Specific test
pytest tests/test_pipeline_loader.py

# Verbose output
pytest -v
```

## Development

```bash
# Install development dependencies
pip install -r requirements-dev.txt

# Install pre-commit hooks
pre-commit install

# Run linter
ruff check .

# Run formatter
ruff format .

# Type checking
mypy dataforge/
```

## Design Principles

- **Explicit Contracts**: Clear interfaces with type hints
- **Fail Fast**: Immediate errors with detailed messages
- **Declarative Configuration**: YAML-based, version-controlled
- **Async First**: Built on asyncio for performance
- **Structured Logging**: No print statements, structured logs only

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md) for development guidelines.

## License

MIT License - see [LICENSE](LICENSE) file for details.

## Project Status

Version 0.1.0 - Beta

See [CHANGELOG.md](CHANGELOG.md) for version history and roadmap.
