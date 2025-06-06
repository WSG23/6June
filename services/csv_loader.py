# services/csv_loader.py
"""CSV loading utilities used across the application."""

from typing import Dict, Any, Optional, Union, IO

import pandas as pd
import io

from config.settings import REQUIRED_INTERNAL_COLUMNS
from utils.logging_config import get_logger
from utils.error_handler import handle_data_error, ValidationError, DataProcessingError
from utils.validators import MappingValidator
from utils.input_sanitizer import InputSanitizer

logger = get_logger(__name__)

@handle_data_error
def load_csv_event_log(
    csv_file_obj: Union[str, IO[str]],
    column_mapping: Dict[str, str],
    timestamp_format: Optional[str] = None,
    *,
    return_dict: bool = True,
) -> Union[pd.DataFrame, Dict[str, Any]]:
    """Load an event log CSV using a provided column mapping.

    Parameters
    ----------
    csv_file_obj:
        A file-like object or string containing the CSV data.
    column_mapping:
        Mapping of CSV column headers to display names defined in
        :data:`REQUIRED_INTERNAL_COLUMNS`.
    timestamp_format:
        Optional explicit timestamp format for :func:`pandas.to_datetime`.
    return_dict:
        When ``True`` (default) the function returns a dictionary with a
        ``success`` flag and either a ``result`` DataFrame or an ``error``
        message.  When ``False`` only the DataFrame is returned on success and
        an exception is raised on failure.
    """

    logger.info("Loading CSV data...")

    if isinstance(csv_file_obj, str):
        csv_file_obj = io.StringIO(csv_file_obj)

    try:
        df = pd.read_csv(csv_file_obj, dtype=str)
    except pd.errors.EmptyDataError:
        raise ValidationError("CSV file appears to be empty")
    except Exception as exc:
        raise DataProcessingError(f"Failed to read CSV: {exc}")

    if df.empty:
        raise ValidationError("CSV file appears to be empty")

    # Validate column mapping completeness
    missing_keys = [
        key for key in REQUIRED_INTERNAL_COLUMNS.keys() if key not in column_mapping
    ]
    if missing_keys:
        raise ValidationError(
            f"Missing required column mappings: {', '.join(missing_keys)}"
        )

    # Validate that mapped columns exist in the CSV
    missing_columns = [col for col in column_mapping.keys() if col not in df.columns]
    if missing_columns:
        raise ValidationError(
            f"Mapped CSV columns not found: {', '.join(missing_columns)}"
        )

    MappingValidator.validate_mapping_uniqueness(column_mapping)

    # Apply mapping and sanitize values
    sanitized_data = {}
    for source_col, display_name in column_mapping.items():
        series = df[source_col].astype(str).apply(InputSanitizer.sanitize_string)
        sanitized_data[display_name] = series

    event_df = pd.DataFrame(sanitized_data)

    # Parse timestamps
    timestamp_display = REQUIRED_INTERNAL_COLUMNS["Timestamp"]
    if timestamp_display in event_df.columns:
        event_df[timestamp_display] = pd.to_datetime(
            event_df[timestamp_display], errors="coerce", format=timestamp_format
        )
        event_df.dropna(subset=[timestamp_display], inplace=True)

    logger.info(f"Loaded {len(event_df)} events")

    if return_dict:
        return {"success": True, "result": event_df}
    return event_df
