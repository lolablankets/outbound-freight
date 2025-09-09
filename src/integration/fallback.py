"""Fallback matching strategies for unmatched orders."""

import pandas as pd


def perform_fallback_join_strategies(unmatched_invoices: pd.DataFrame, full_order_df: pd.DataFrame) -> pd.DataFrame:
    """Apply progressive fallback matching for unmatched invoice records.
    
    Args:
        unmatched_invoices: Invoice records that failed primary join
        full_order_df: Complete Shopify order dataset for matching
        
    Returns:
        DataFrame with recovered matches and confidence scores
    """
    # Implementation will go here - fuzzy matching, confidence scoring
    pass