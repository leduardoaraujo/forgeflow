from datetime import datetime, timezone
from typing import Any

from forgeflow.core.exceptions import TransformerException
from forgeflow.core.transformer import BaseTransformer


class JsonNormalizer(BaseTransformer):
    def transform(self, data: Any) -> list[dict[str, Any]] | dict[str, Any]:
        # Extrai array de dentro de um envelope (ex: {"results": [...]})
        if isinstance(data, dict) and (key := self.config.get("results_key")):
            data = data.get(key)
            if data is None:
                raise TransformerException(f"Key '{key}' not found in response")

        if isinstance(data, list):
            return [self._transform_item(item) for item in data]
        if not isinstance(data, dict):
            raise TransformerException(f"Expected dict or list, got {type(data).__name__}")
        return self._transform_item(data)

    def _transform_item(self, item: Any) -> dict[str, Any]:
        if not isinstance(item, dict):
            raise TransformerException(f"Expected dict, got {type(item).__name__}")

        normalized = self._flatten_dict(item) if self.config.get("flatten") else dict(item)

        # Seleciona apenas os campos especificados
        if include_fields := self.config.get("include_fields"):
            normalized = {k: normalized[k] for k in include_fields if k in normalized}

        # Converte campos que são listas em string separada por delimitador
        if list_join := self.config.get("list_join"):
            sep = list_join.get("separator", "|")
            for field in list_join.get("fields", []):
                if field in normalized and isinstance(normalized[field], list):
                    normalized[field] = sep.join(str(v) for v in normalized[field])

        if timestamp_field := self.config.get("timestamp_field"):
            if timestamp_field not in normalized:
                normalized[timestamp_field] = datetime.now(timezone.utc).isoformat()

        normalized["_ingested_at"] = datetime.now(timezone.utc).isoformat()

        return normalized

    def _flatten_dict(
        self, data: dict, parent_key: str = "", sep: str = "_"
    ) -> dict[str, Any]:
        items: list[tuple[str, Any]] = []

        for key, value in data.items():
            new_key = f"{parent_key}{sep}{key}" if parent_key else key

            if isinstance(value, dict):
                items.extend(self._flatten_dict(value, new_key, sep).items())
            elif isinstance(value, list):
                items.append((new_key, value))
            else:
                items.append((new_key, value))

        return dict(items)
