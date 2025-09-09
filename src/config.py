"""Configuration constants and utilities for the outbound freight pipeline."""

from pathlib import Path
from enum import Enum
from datetime import datetime, timedelta

# Configuration Constants
DATA_PATH = "data/"
EXPORT_PATH = "exports/"
TEMP_PATH = "temp/processing/current_batch"
TEMP_PATH_BACKUP = "temp/processing/last_batch"

# Vendor-specific header offsets (0-indexed row numbers)
FEDEX_HEADER_OFFSET = 3  # FedEx headers start at row 4 (0-indexed: 3)
UPS_HEADER_OFFSET = 1    # UPS headers start at row 2 (0-indexed: 1)
USPS_HEADER_OFFSET = 1   # USPS headers start at row 2 (0-indexed: 1)

# Date range buffer for Snowflake queries (days)
SNOWFLAKE_DATE_BUFFER_DAYS = 60


class Vendor(Enum):
    """Supported shipping vendors"""
    FEDEX = "fedex"
    UPS = "ups"
    USPS = "usps"
    UNKNOWN = "unknown"


def get_period_data_path(analysis_period: str) -> Path:
    """Get data directory path for specific analysis period.
    
    Args:
        analysis_period: Period like "2025/08"
        
    Returns:
        Path to data/{analysis_period}/ directory
    """
    return Path(DATA_PATH) / analysis_period


def get_period_export_path(analysis_period: str) -> Path:
    """Get export directory path for specific analysis period.
    
    Args:
        analysis_period: Period like "2025/08"
        
    Returns:
        Path to exports/{analysis_period}/ directory
    """
    return Path(EXPORT_PATH) / analysis_period


def get_header_offset(vendor: Vendor) -> int:
    """Get header row offset for specific vendor.
    
    Args:
        vendor: Vendor enum value
        
    Returns:
        Header row offset (0-indexed)
        
    Raises:
        ValueError: If vendor is unknown
    """
    offset_map = {
        Vendor.FEDEX: FEDEX_HEADER_OFFSET,
        Vendor.UPS: UPS_HEADER_OFFSET,
        Vendor.USPS: USPS_HEADER_OFFSET,
    }
    
    if vendor not in offset_map:
        raise ValueError(f"Unknown vendor: {vendor}")
        
    return offset_map[vendor]


def get_buffered_date_range(start_date: datetime, end_date: datetime) -> tuple:
    """Apply date buffer for Snowflake queries.
    
    Args:
        start_date: Invoice data start date
        end_date: Invoice data end date
        
    Returns:
        Tuple of (buffered_start, buffered_end) dates
    """
    buffer = timedelta(days=SNOWFLAKE_DATE_BUFFER_DAYS)
    return (start_date - buffer, end_date + buffer)