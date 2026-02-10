# ForgeFlow Documentation

Welcome to **ForgeFlow** - A modern ETL framework for API ingestion, data transformation, and distribution.

## 🎯 What is ForgeFlow?

ForgeFlow is a Python framework designed to simplify the process of:
- Fetching data from REST APIs
- Transforming and normalizing JSON data
- Loading data into various sinks (PostgreSQL, DuckDB, files)
- Orchestrating data pipelines with Apache Airflow

Built with async-first architecture using Python 3.11+, ForgeFlow provides a declarative YAML-based configuration system for building robust data pipelines.

## 📚 Documentation Structure

- **[Getting Started](guides/getting-started.md)** - Installation and quick start
- **[User Guide](guides/user-guide.md)** - Comprehensive usage guide
- **[Configuration](guides/configuration.md)** - YAML configuration reference
- **[API Reference](api/index.md)** - Detailed API documentation
- **[Examples](examples/index.md)** - Real-world examples and tutorials
- **[Contributing](../CONTRIBUTING.md)** - How to contribute

## ⚡ Quick Start

### Installation

```bash
pip install forgeflow
```

### Basic Usage

Create a `config/pipelines.yaml`:

```yaml
pipelines:
  - name: my_first_pipeline
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
      - type: duckdb
        config:
          database: data/output.duckdb
          table: api_data
```

Run it:

```bash
forgeflow run my_first_pipeline
```

## 🚀 Features

- ✅ **Async-first** - Built on asyncio for high performance
- ✅ **Type-safe** - Full type hints with Pydantic models
- ✅ **Extensible** - Easy to add custom connectors, transformers, and sinks
- ✅ **Airflow Integration** - Native support for Apache Airflow
- ✅ **Rich CLI** - Beautiful command-line interface
- ✅ **Multiple Sinks** - PostgreSQL, DuckDB, Files (JSON, Parquet)

## 📖 Learn More

Check out our comprehensive guides:

1. [Installation Guide](guides/getting-started.md)
2. [Core Concepts](guides/core-concepts.md)
3. [Pipeline Configuration](guides/configuration.md)
4. [Extending ForgeFlow](guides/extending.md)

## 🤝 Community

- **GitHub**: [leduardoaraujo/forgeflow](https://github.com/leduardoaraujo/forgeflow)
- **Issues**: [Report bugs or request features](https://github.com/leduardoaraujo/forgeflow/issues)

## 📄 License

ForgeFlow is released under the MIT License. See [LICENSE](../LICENSE) for details.
