"""Order matching utilities for joining invoice and Shopify data."""

import pandas as pd


def parse_shopify_order_codes(df: pd.DataFrame) -> pd.DataFrame:
    """Extract and normalize Shopify order references from vendor tracking data.
    
    Args:
        df: DataFrame with reference columns (reference_1, reference_2, reference_4)
        
    Returns:
        DataFrame with additional parsed columns
    """
    # Implementation will go here - extract M-numbers, LOLAID, #-numbers
    pass


def join_shopify_data_with_invoice_data(invoice_df: pd.DataFrame, order_df: pd.DataFrame) -> pd.DataFrame:
    """Join invoice data with Shopify order data using local pandas merge.
    
    Args:
        invoice_df: Processed invoice data with parsed order reference codes
        order_df: Complete Shopify order dataset downloaded via date range query
        
    Returns:
        DataFrame combining invoice and order data
    """
    # Implementation will go here - multi-strategy local pandas joins
    pass