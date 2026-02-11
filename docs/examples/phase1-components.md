# New Components Examples

This document provides examples for the newly implemented components in ForgeFlow.

## 🎯 New Sinks

### BigQuery Sink

Write data to Google BigQuery data warehouse.

```yaml
pipelines:
  - name: api_to_bigquery
    enabled: true
    connector:
      type: http
      config:
        url: https://api.example.com/users
        method: GET
    transformer:
      type: json_normalizer
      config:
        flatten: true
    sinks:
      - type: bigquery
        config:
          project_id: my-gcp-project
          dataset_id: raw_data
          table_id: users
          location: US
          credentials_path: /path/to/credentials.json  # Optional
```

**Features:**
- Auto-creates datasets and tables
- Schema inference from data
- Supports nested JSON fields
- Configurable location (US, EU, etc.)

---

### S3 Sink

Write data to AWS S3 in multiple formats.

```yaml
pipelines:
  - name: api_to_s3_json
    enabled: true
    connector:
      type: rest
      config:
        base_url: https://api.example.com
        endpoint: /data
    sinks:
      - type: s3
        config:
          bucket: my-data-bucket
          prefix: raw/api_data
          format: json  # json, jsonl, or parquet
          batch_size: 100
          partition_by_date: true
          filename_pattern: "{timestamp}"
          region_name: us-east-1
          # Optional: for explicit credentials
          # aws_access_key_id: YOUR_KEY
          # aws_secret_access_key: YOUR_SECRET
```

**Formats Supported:**
- **JSON**: Batched array of objects
- **JSONL**: Line-delimited JSON (one object per line)
- **Parquet**: Columnar format (requires `pandas` and `pyarrow`)

**Parquet Example:**
```yaml
sinks:
  - type: s3
    config:
      bucket: analytics-bucket
      prefix: parquet/users
      format: parquet
      batch_size: 1000
      compression: snappy  # or gzip, zstd
```

---

### MongoDB Sink

Write data to MongoDB collections with optional upsert.

```yaml
pipelines:
  - name: api_to_mongodb
    enabled: true
    connector:
      type: http
      config:
        url: https://api.example.com/products
    sinks:
      - type: mongodb
        config:
          connection_string: mongodb://localhost:27017
          database: ecommerce
          collection: products
          upsert: true
          upsert_key: product_id
          indexes:
            - product_id
            - fields:
                - [category, 1]
                - [price, -1]
              name: category_price_idx
```

**Features:**
- Insert or upsert modes
- Automatic index creation
- Connection string or component-based config
- Async operations with Motor

**Alternative Config (without connection string):**
```yaml
config:
  host: localhost
  port: 27017
  username: admin
  password: secret
  database: mydb
  collection: mycollection
```

---

## 🔄 New Transformers

### Filter Transformer

Filter data based on conditions with AND/OR logic.

```yaml
pipelines:
  - name: filter_active_users
    enabled: true
    connector:
      type: http
      config:
        url: https://api.example.com/users
    transformer:
      type: filter
      config:
        conditions:
          - field: status
            operator: eq
            value: active
          - field: age
            operator: gte
            value: 18
        logic: AND  # or OR
    sinks:
      - type: file
        config:
          path: data/active_users
          format: json
```

**Supported Operators:**
- `eq` - Equal to
- `ne` - Not equal to
- `gt` - Greater than
- `gte` - Greater than or equal
- `lt` - Less than
- `lte` - Less than or equal
- `contains` - Contains value (for strings/lists)
- `not_contains` - Does not contain
- `in` - Value in list
- `not_in` - Value not in list
- `is_null` - Field is null
- `is_not_null` - Field is not null
- `startswith` - String starts with
- `endswith` - String ends with

**Nested Fields Example:**
```yaml
transformer:
  type: filter
  config:
    conditions:
      - field: user.profile.role
        operator: eq
        value: admin
      - field: user.settings.notifications
        operator: eq
        value: true
    logic: AND
```

**OR Logic Example:**
```yaml
transformer:
  type: filter
  config:
    conditions:
      - field: priority
        operator: eq
        value: high
      - field: status
        operator: eq
        value: urgent
    logic: OR  # Passes if ANY condition is true
```

---

### Schema Mapper Transformer

Transform data between different schemas with field mapping and type conversion.

```yaml
pipelines:
  - name: map_user_schema
    enabled: true
    connector:
      type: rest
      config:
        base_url: https://api.example.com
        endpoint: /users
    transformer:
      type: schema_mapper
      config:
        mappings:
          # Simple rename
          - source: firstName
            target: first_name

          # With type conversion
          - source: age
            target: age
            type: int

          # With default value
          - source: country
            target: country
            default: Unknown

          # Nested field flattening
          - source: address.city
            target: city

          # Computed field
          - target: full_name
            expression: "{firstName} {lastName}"

          # Nested target
          - source: email
            target: contact.email

        exclude_fields:
          - password
          - internal_id

        include_unmapped: false
        strict: false
    sinks:
      - type: postgres
        config:
          table: users_normalized
```

**Type Conversions:**
- `string` - Convert to string
- `int` - Convert to integer
- `float` - Convert to float
- `bool` - Convert to boolean
- `list` - Convert to list
- `dict` - Convert to dictionary

**Advanced Example - API Response Normalization:**
```yaml
transformer:
  type: schema_mapper
  config:
    mappings:
      # Flatten nested API response
      - source: data.user.id
        target: user_id
        type: int

      - source: data.user.attributes.name
        target: name

      - source: data.user.attributes.email
        target: email

      # Computed fields
      - target: full_address
        expression: "{data.user.address.street}, {data.user.address.city}"

      # Type conversion with default
      - source: data.user.verified
        target: is_verified
        type: bool
        default: false
        required: true

    strict: true  # Fail if required fields are missing
    include_unmapped: false
```

---

## 📋 Complete Pipeline Examples

### Example 1: API → BigQuery with Filtering

```yaml
pipelines:
  - name: active_orders_to_bigquery
    enabled: true
    connector:
      type: rest
      config:
        base_url: https://api.store.com
        endpoint: /orders
        headers:
          Authorization: Bearer ${API_TOKEN}

    transformer:
      type: filter
      config:
        conditions:
          - field: status
            operator: in
            value: [pending, processing, shipped]
          - field: total_amount
            operator: gt
            value: 100
        logic: AND

    sinks:
      - type: bigquery
        config:
          project_id: my-analytics-project
          dataset_id: sales
          table_id: active_orders
          location: US
```

### Example 2: API → Schema Mapping → MongoDB + S3

```yaml
pipelines:
  - name: products_multi_sink
    enabled: true
    connector:
      type: http
      config:
        url: https://api.products.com/v2/catalog
        method: GET

    transformer:
      type: schema_mapper
      config:
        mappings:
          - source: product_id
            target: id
            type: int

          - source: product_name
            target: name

          - source: price_usd
            target: price
            type: float

          - source: inventory.warehouse_a
            target: stock_count
            type: int
            default: 0

          - target: product_url
            expression: "https://store.com/p/{product_id}"

        exclude_fields:
          - internal_notes
          - cost_price

    sinks:
      # MongoDB for operational queries
      - type: mongodb
        config:
          connection_string: ${MONGO_URL}
          database: products
          collection: catalog
          upsert: true
          upsert_key: id

      # S3 for analytics
      - type: s3
        config:
          bucket: data-lake
          prefix: products/catalog
          format: parquet
          batch_size: 500
          partition_by_date: true
```

### Example 3: Chained Transformers

```yaml
pipelines:
  - name: complex_transformation
    enabled: true
    connector:
      type: rest
      config:
        base_url: https://api.example.com
        endpoint: /events

    # Note: Currently single transformer is supported
    # For chained transformations, use pipeline composition
    transformer:
      type: schema_mapper
      config:
        mappings:
          - source: event.type
            target: event_type
          - source: event.timestamp
            target: timestamp
          - source: user.id
            target: user_id

    sinks:
      - type: duckdb
        config:
          database: data/analytics.duckdb
          table: events
```

---

## 🚀 Installation

Install the required extras for the new components:

```bash
# BigQuery
pip install -e ".[bigquery]"

# S3
pip install -e ".[s3]"

# MongoDB
pip install -e ".[mongodb]"

# All new components
pip install -e ".[bigquery,s3,mongodb]"

# Everything
pip install -e ".[all]"
```

---

## 📝 Notes

- **Filter Transformer** returns `None` for filtered-out data, which prevents it from being written to sinks
- **Schema Mapper** can be used for data cleaning, normalization, and API response transformation
- **S3 Sink** automatically batches data for JSON and Parquet formats to reduce API calls
- **BigQuery Sink** automatically infers schema and creates tables if they don't exist
- **MongoDB Sink** supports both insert and upsert modes for handling updates

For more examples, see the `examples/` directory in the repository.
