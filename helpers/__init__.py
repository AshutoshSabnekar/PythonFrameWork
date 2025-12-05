"""
Helpers package for semantic view and Power BI validations.
Contains reusable utility functions for data processing, configuration,
logging, and Power BI interactions.
"""

__version__ = "1.0.0"
__all__ = []

# Import commonly used functions (keep minimal)
from .DataHelpers import (
    normalize_column_names,
    safe_to_datetime,
    assert_non_empty,
    compare_floats,
    __all__ as data_helpers_all,
)
__all__.extend(data_helpers_all)

from .ConfigHelpers import (
    load_db_config,
    get_connection_string,
    __all__ as config_helpers_all,
)
__all__.extend(config_helpers_all)

# Optional: conditional imports for optional dependencies
try:
    from .PowerBiHelpers import (
        build_powerbi_report_url,
        get_powerbi_access_token,
        __all__ as powerbi_helpers_all,
    )
    __all__.extend(powerbi_helpers_all)
except ImportError:
    pass  # Power BI helpers optional

# Export the full list for IDE auto-completion
__all__ = sorted(set(__all__))
