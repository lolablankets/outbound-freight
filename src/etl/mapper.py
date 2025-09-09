"""Schema mapping utilities for converting vendor data to common format."""

import pandas as pd
from ..config import Vendor
from ..vendors.fedex import FedExProcessor
from ..vendors.ups import UPSProcessor
from ..vendors.usps import USPSProcessor


def map_vendor_columns_to_shared_schema(df: pd.DataFrame, vendor: Vendor) -> pd.DataFrame:
    """Map vendor-specific columns to common invoice schema.
    
    Transforms vendor column names to standardized schema defined in
    docs/analysis_schema.md. Handles vendor-specific field mappings.
    
    Args:
        df: DataFrame with vendor-specific columns
        vendor: Vendor type for column mapping selection
        
    Returns:
        DataFrame with standardized column names
        
    Example:
        standardized_df = map_vendor_columns_to_shared_schema(fedex_df, Vendor.FEDEX)
    """
    # Get appropriate processor for vendor
    processor_map = {
        Vendor.FEDEX: FedExProcessor(),
        Vendor.UPS: UPSProcessor(),
        Vendor.USPS: USPSProcessor()
    }
    
    if vendor not in processor_map:
        raise ValueError(f"Unsupported vendor: {vendor}")
    
    processor = processor_map[vendor]
    
    # Use vendor processor to handle the mapping
    return processor.process_dataframe(df)