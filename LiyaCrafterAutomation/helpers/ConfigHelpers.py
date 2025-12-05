"""
Configuration and environment helpers.
"""

import os
import json
import yaml
from typing import Dict, Any, Optional, Union
from pathlib import Path

__all__ = [
    "load_db_config",
    "get_connection_string",
    "get_environment",
    "load_json_config",
    "load_yaml_config",
]


def load_db_config(db_name: str, env: Optional[str] = None) -> Dict[str, Any]:
    """Load database config from environment or config files."""
    env = env or get_environment()

    # Try environment variables first
    conn_str = os.getenv(f"{db_name.upper()}_CONN_STR")
    if conn_str:
        return {"connection_string": conn_str, "type": db_name.lower()}

    # Try config files
    config = _load_config_file(env)
    db_configs = config.get("databases", {})

    if db_name not in db_configs:
        raise ValueError(f"Database '{db_name}' not found in config")

    return db_configs[db_name]


def get_connection_string(db_config: Dict[str, Any]) -> str:
    """Build connection string from config dict."""
    db_type = db_config.get("type", "").lower()

    if db_type == "azure_sql":
        return db_config["connection_string"]
    elif db_type == "snowflake":
        conn_params = "user={user}&password={password}&account={account}".format(**db_config)
        if "warehouse" in db_config:
            conn_params += f"&warehouse={db_config['warehouse']}"
        return f"snowflake://{conn_params}"
    else:
        raise ValueError(f"Unsupported DB type: {db_type}")


def get_environment() -> str:
    """Get current environment (dev/qa/prod)."""
    return os.getenv("ENVIRONMENT", "dev").lower()


def load_json_config(file_path: Union[str, Path]) -> Dict[str, Any]:
    """Load JSON config file."""
    with open(file_path) as f:
        return json.load(f)


def load_yaml_config(file_path: Union[str, Path]) -> Dict[str, Any]:
    """Load YAML config file."""
    with open(file_path) as f:
        return yaml.safe_load(f)


def _load_config_file(env: str) -> Dict[str, Any]:
    """Load config file for specific environment."""
    config_paths = [
        Path(f"config/{env}.json"),
        Path(f"config/{env}.yaml"),
        Path("config.json"),
        Path("config.yaml"),
    ]

    for config_path in config_paths:
        if config_path.exists():
            if config_path.suffix == ".json":
                return load_json_config(config_path)
            elif config_path.suffix == ".yaml":
                return load_yaml_config(config_path)

    raise FileNotFoundError(f"No config file found for environment: {env}")
