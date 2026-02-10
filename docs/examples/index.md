# Examples

Real-world examples and tutorials for ForgeFlow.

## Basic Examples

### Example 1: Fetch JSON from API

Fetch user data from JSONPlaceholder API and save to file:

```yaml
pipelines:
  - name: fetch_users
    enabled: true
    connector:
      type: http
      config:
        url: https://jsonplaceholder.typicode.com/users
        method: GET
    transformer:
      type: json_normalizer
      config:
        flatten: false
    sinks:
      - type: file
        config:
          path: data/users
          format: json
```

### Example 2: Load to DuckDB

Fetch and load data into DuckDB for analytics:

```yaml
pipelines:
  - name: api_to_duckdb
    enabled: true
    connector:
      type: http
      config:
        url: https://api.example.com/sales
        headers:
          Authorization: Bearer ${API_TOKEN}
    transformer:
      type: json_normalizer
      config:
        flatten: true
    sinks:
      - type: duckdb
        config:
          database: analytics.duckdb
          table: sales
          mode: replace
```

### Example 3: Multiple Sinks

Write to multiple destinations simultaneously:

```yaml
pipelines:
  - name: multi_sink_pipeline
    enabled: true
    connector:
      type: rest
      config:
        base_url: https://api.example.com
        endpoint: /data
    transformer:
      type: json_normalizer
      config:
        flatten: true
    sinks:
      - type: postgres
        config:
          host: localhost
          database: warehouse
          table: raw_data
      - type: file
        config:
          path: backup/data
          format: parquet
      - type: duckdb
        config:
          database: analytics.duckdb
          table: processed_data
```

## Advanced Examples

### Airflow Integration

See [airflow_dag_example.py](../../examples/airflow_dag_example.py) for a complete example.

### Custom Connector

```python
from forgeflow.core.connector import BaseConnector

class MyCustomConnector(BaseConnector):
    def validate_config(self) -> None:
        required = ["api_key"]
        missing = [k for k in required if k not in self.config]
        if missing:
            raise ValueError(f"Missing: {missing}")
    
    async def fetch(self) -> dict:
        # Your implementation
        return {"data": []}
    
    async def close(self) -> None:
        pass
```

## Tutorials

Coming soon:
- Building a complete ETL pipeline
- Scheduling with Airflow
- Monitoring and logging
- Testing pipelines
