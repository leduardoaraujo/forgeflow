# Getting Started with ForgeFlow

This guide will help you get started with ForgeFlow in just a few minutes.

## Installation

### Requirements

- Python 3.11 or higher
- pip or uv package manager

### Basic Installation

```bash
pip install forgeflow
```

### Installation with Optional Dependencies

ForgeFlow supports multiple sinks and integrations. Install what you need:

```bash
# PostgreSQL support
pip install forgeflow[postgres]

# DuckDB support
pip install forgeflow[duckdb]

# API server
pip install forgeflow[api]

# Airflow integration
pip install forgeflow[airflow]

# Everything
pip install forgeflow[all]
```

## Your First Pipeline

### 1. Create Configuration Directory

```bash
mkdir -p config
```

### 2. Create Pipeline Configuration

Create `config/pipelines.yaml`:

```yaml
pipelines:
  - name: hello_forgeflow
    enabled: true
    connector:
      type: http
      config:
        url: https://jsonplaceholder.typicode.com/users
        method: GET
        timeout: 30
    transformer:
      type: json_normalizer
      config:
        flatten: true
    sinks:
      - type: file
        config:
          path: data/output
          format: json
```

### 3. Run Your Pipeline

```bash
forgeflow run hello_forgeflow
```

### 4. View Results

```bash
cat data/output/hello_forgeflow.json
```

## CLI Commands

ForgeFlow provides several CLI commands:

```bash
# List all pipelines
forgeflow list

# Run a specific pipeline
forgeflow run <pipeline-name>

# Validate configuration
forgeflow validate

# Create new pipeline template
forgeflow init <pipeline-name>

# Test pipeline connection
forgeflow test <pipeline-name>
```

## Next Steps

Now that you have ForgeFlow running, explore:

- [Core Concepts](core-concepts.md) - Understand ForgeFlow architecture
- [Configuration Guide](configuration.md) - Deep dive into YAML configuration
- [Examples](../examples/index.md) - Real-world use cases
- [Extending ForgeFlow](extending.md) - Build custom components

## Troubleshooting

### Command not found: forgeflow

Make sure your Python scripts directory is in PATH:

```bash
# Linux/Mac
export PATH="$HOME/.local/bin:$PATH"

# Windows
# Add %USERPROFILE%\AppData\Local\Programs\Python\Python3XX\Scripts to PATH
```

### Import errors

Make sure you installed ForgeFlow in your active virtual environment:

```bash
pip list | grep forgeflow
```

### Need Help?

- Check the [User Guide](user-guide.md)
- Search [GitHub Issues](https://github.com/leduardoaraujo/forgeflow/issues)
- Create a new issue if you found a bug
