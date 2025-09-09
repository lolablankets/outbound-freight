"""Data cleaning utilities for invoice processing."""

from typing import List
import pandas as pd
import numpy as np
from datetime import datetime


def convert_dollar_to_float(df: pd.DataFrame, columns: List[str]) -> pd.DataFrame:
    """Convert currency strings to float values.
    
    Removes currency symbols ($, commas) and converts to numeric format.
    Handles negative values and missing data appropriately.
    
    Args:
        df: DataFrame with currency columns
        columns: List of column names containing currency values
        
    Returns:
        DataFrame with numeric currency columns
        
    Example:
        df = convert_dollar_to_float(df, ['shipping_cost', 'net_charge'])
    """
    df = df.copy()
    
    for column in columns:
        if column not in df.columns:
            print(f"Warning: Column '{column}' not found in DataFrame")
            continue
            
        # Convert to string first to handle mixed types
        df[column] = df[column].astype(str)
        
        # Remove currency symbols and commas
        df[column] = df[column].str.replace('$', '', regex=False)
        df[column] = df[column].str.replace(',', '', regex=False)
        df[column] = df[column].str.replace('(', '-', regex=False)  # Handle negative in parentheses
        df[column] = df[column].str.replace(')', '', regex=False)
        df[column] = df[column].str.strip()
        
        # Replace empty strings and 'nan' with NaN
        df[column] = df[column].replace(['', 'nan', 'NaN', 'null'], np.nan)
        
        # Convert to numeric
        df[column] = pd.to_numeric(df[column], errors='coerce')
        
        print(f"Converted {column}: {df[column].notna().sum()} valid values, {df[column].isna().sum()} NaN values")
    
    return df


def convert_string_to_date(df: pd.DataFrame, columns: List[str]) -> pd.DataFrame:
    """Convert string dates to datetime format.
    
    Handles multiple date formats and ensures consistent datetime format
    across all vendor data sources.
    
    Args:
        df: DataFrame with date columns
        columns: List of column names containing date strings
        
    Returns:
        DataFrame with datetime columns
        
    Example:
        df = convert_string_to_date(df, ['ship_date', 'invoice_date'])
    """
    df = df.copy()
    
    for column in columns:
        if column not in df.columns:
            print(f"Warning: Column '{column}' not found in DataFrame")
            continue
        
        # Try multiple date formats
        original_count = df[column].notna().sum()
        
        # Convert to datetime with flexible parsing
        df[column] = pd.to_datetime(df[column], errors='coerce', infer_datetime_format=True)
        
        converted_count = df[column].notna().sum()
        failed_count = original_count - converted_count
        
        if failed_count > 0:
            print(f"Warning: {failed_count} dates failed to parse in column '{column}'")
        
        print(f"Converted {column}: {converted_count} valid dates, {df[column].isna().sum()} NaN values")
    
    return df


def normalize_zip_codes(df: pd.DataFrame, zip_column: str = 'recipient_zip') -> pd.DataFrame:
    """Normalize ZIP codes to consistent format.
    
    Args:
        df: DataFrame with ZIP code column
        zip_column: Name of ZIP code column
        
    Returns:
        DataFrame with normalized ZIP codes
    """
    if zip_column not in df.columns:
        print(f"Warning: Column '{zip_column}' not found in DataFrame")
        return df
    
    df = df.copy()
    
    # Convert to string and clean
    df[zip_column] = df[zip_column].astype(str).str.strip()
    
    # Remove non-numeric characters except hyphens
    df[zip_column] = df[zip_column].str.replace(r'[^0-9-]', '', regex=True)
    
    # Ensure 5-digit or 9-digit format
    def normalize_zip(zip_code):
        if pd.isna(zip_code) or zip_code == 'nan':
            return None
        
        # Remove hyphens for processing
        clean_zip = zip_code.replace('-', '')
        
        if len(clean_zip) >= 5:
            if len(clean_zip) >= 9:
                # 9-digit ZIP+4 format
                return f"{clean_zip[:5]}-{clean_zip[5:9]}"
            else:
                # 5-digit ZIP
                return clean_zip[:5]
        else:
            # Invalid ZIP code
            return None
    
    df[zip_column] = df[zip_column].apply(normalize_zip)
    
    valid_zips = df[zip_column].notna().sum()
    print(f"Normalized {zip_column}: {valid_zips} valid ZIP codes")
    
    return df


def normalize_state_codes(df: pd.DataFrame, state_column: str = 'recipient_state') -> pd.DataFrame:
    """Normalize state codes to consistent 2-letter format.
    
    Args:
        df: DataFrame with state column
        state_column: Name of state column
        
    Returns:
        DataFrame with normalized state codes
    """
    if state_column not in df.columns:
        print(f"Warning: Column '{state_column}' not found in DataFrame")
        return df
    
    df = df.copy()
    
    # Convert to uppercase and strip whitespace
    df[state_column] = df[state_column].astype(str).str.upper().str.strip()
    
    # Validate 2-letter state codes
    valid_states = {
        'AL', 'AK', 'AZ', 'AR', 'CA', 'CO', 'CT', 'DE', 'FL', 'GA',
        'HI', 'ID', 'IL', 'IN', 'IA', 'KS', 'KY', 'LA', 'ME', 'MD',
        'MA', 'MI', 'MN', 'MS', 'MO', 'MT', 'NE', 'NV', 'NH', 'NJ',
        'NM', 'NY', 'NC', 'ND', 'OH', 'OK', 'OR', 'PA', 'RI', 'SC',
        'SD', 'TN', 'TX', 'UT', 'VT', 'VA', 'WA', 'WV', 'WI', 'WY',
        'DC', 'PR', 'VI'  # Include DC and territories
    }
    
    # Mark invalid state codes as None
    df[state_column] = df[state_column].apply(
        lambda x: x if x in valid_states else None
    )
    
    valid_states_count = df[state_column].notna().sum()
    print(f"Normalized {state_column}: {valid_states_count} valid state codes")
    
    return df


def clean_tracking_numbers(df: pd.DataFrame, tracking_column: str = 'tracking_number') -> pd.DataFrame:
    """Clean and validate tracking numbers.
    
    Args:
        df: DataFrame with tracking number column
        tracking_column: Name of tracking number column
        
    Returns:
        DataFrame with cleaned tracking numbers
    """
    if tracking_column not in df.columns:
        print(f"Warning: Column '{tracking_column}' not found in DataFrame")
        return df
    
    df = df.copy()
    
    # Convert to string and remove whitespace
    df[tracking_column] = df[tracking_column].astype(str).str.strip()
    
    # Remove any non-alphanumeric characters
    df[tracking_column] = df[tracking_column].str.replace(r'[^A-Za-z0-9]', '', regex=True)
    
    # Mark empty or 'nan' as None
    df[tracking_column] = df[tracking_column].replace(['', 'nan', 'NaN'], None)
    
    valid_tracking = df[tracking_column].notna().sum()
    print(f"Cleaned {tracking_column}: {valid_tracking} valid tracking numbers")
    
    return df