# data-forge

central api for data ingestion, normalization, and distribution

## structure

```
dataforge/
├── core/          # base interfaces
├── connectors/    # data input
├── transformers/  # normalization
├── sinks/         # data output
├── pipeline/      # orchestration
└── api/           # fastapi endpoints

config/            # pipeline configs
scripts/           # cli tools
tests/             # tests
```

## setup

```bash
pip install -e ".[dev]"
```

copy `.env.example` to `.env` and set credentials

## usage

### cli

```bash
python scripts/run_pipeline.py example_pipeline
python scripts/run_pipeline.py my_pipeline
```

### api

```bash
uvicorn dataforge.api.main:app --reload
```

### python

```python
import asyncio
from dataforge.pipeline.executor import PipelineExecutor
from dataforge.pipeline.loader import PipelineLoader

pipelines = PipelineLoader.load_from_file("config/pipelines.yaml")
pipeline = next(p for p in pipelines if p["name"] == "my_pipeline")

executor = PipelineExecutor()
asyncio.run(executor.execute(pipeline))
```

## pipeline config

```yaml
pipelines:
  - name: my_pipeline
    enabled: true
    connector:
      type: http
      config:
        url: https://api.example.com/data
    transformer:
      type: json_normalizer
      config:
        flatten: true
    sinks:
      - type: postgres
        config:
          table: raw_data
      - type: file
        config:
          path: data/output
          format: json
```

## connectors

- http
- rest

## transformers

- json_normalizer

## sinks

- postgres
- duckdb
- file

## extending

implement base interfaces

```python
from dataforge.core.connector import BaseConnector

class MyConnector(BaseConnector):
    def validate_config(self) -> None:
        pass

    async def fetch(self) -> dict:
        pass

    async def close(self) -> None:
        pass
```

## notes

- explicit contracts
- non-silent failures
- declarative configuration
- async-first
- no prints