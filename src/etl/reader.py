"""File reading utilities with dynamic header detection."""

from pathlib import Path
import pandas as pd
from ..config import Vendor, get_header_offset
from ..vendors.detector import detect_vendor_from_path


def read_vendor_file(filepath: Path, vendor: Vendor = None) -> pd.DataFrame:
    """Read vendor invoice file with dynamic header detection.
    
    Handles Excel/CSV files with vendor-specific header offsets:
    - FedEx: Headers at row 4 (offset 3)
    - UPS: Headers at row 2 (offset 1) 
    - USPS: Headers at row 2 (offset 1)
    
    Args:
        filepath: Path to invoice file
        vendor: Detected vendor for header offset selection (auto-detected if None)
        
    Returns:
        DataFrame with invoice data
        
    Example:
        df = read_vendor_file(Path("data/FDX_file.xlsx"), Vendor.FEDEX)
    """
    if vendor is None:
        vendor = detect_vendor_from_path(filepath)
        if vendor == Vendor.UNKNOWN:
            print(f"Warning: Could not detect vendor for {filepath.name}, using default offset")
            header_offset = 0
        else:
            header_offset = get_header_offset(vendor)
    else:
        header_offset = get_header_offset(vendor)
    
    print(f"Reading {filepath.name} as {vendor.value} with header offset {header_offset}")
    
    try:
        if filepath.suffix.lower() in ['.xlsx', '.xls']:
            df = _read_excel_file(filepath, header_offset)
        elif filepath.suffix.lower() == '.csv':
            df = _read_csv_file(filepath, header_offset)
        else:
            raise ValueError(f"Unsupported file format: {filepath.suffix}")
        
        print(f"Successfully read {len(df)} rows from {filepath.name}")
        return df
        
    except Exception as e:
        print(f"Error reading {filepath.name}: {str(e)}")
        raise


def _read_excel_file(filepath: Path, header_offset: int) -> pd.DataFrame:
    """Read Excel file with specific header offset.
    
    Args:
        filepath: Path to Excel file
        header_offset: Row number where headers start (0-indexed)
        
    Returns:
        DataFrame with data
    """
    # Read Excel file with header at specified row
    df = pd.read_excel(filepath, header=header_offset)
    
    # Clean up column names (remove extra whitespace)
    df.columns = df.columns.astype(str).str.strip()
    
    # Remove completely empty rows
    df = df.dropna(how='all')
    
    return df


def _read_csv_file(filepath: Path, header_offset: int) -> pd.DataFrame:
    """Read CSV file with specific header offset.
    
    Args:
        filepath: Path to CSV file
        header_offset: Row number where headers start (0-indexed)
        
    Returns:
        DataFrame with data
    """
    # For CSV files, we need to skip rows before the header
    if header_offset > 0:
        df = pd.read_csv(filepath, skiprows=header_offset)
    else:
        df = pd.read_csv(filepath)
    
    # Clean up column names
    df.columns = df.columns.astype(str).str.strip()
    
    # Remove completely empty rows
    df = df.dropna(how='all')
    
    return df


def preview_file_structure(filepath: Path, num_rows: int = 10) -> None:
    """Preview file structure to help with header detection.
    
    Args:
        filepath: Path to file to preview
        num_rows: Number of rows to show
    """
    print(f"\\nPreviewing structure of {filepath.name}:")
    print("=" * 50)
    
    try:
        if filepath.suffix.lower() in ['.xlsx', '.xls']:
            # Read first few rows without header detection
            df_preview = pd.read_excel(filepath, header=None, nrows=num_rows)
        else:
            df_preview = pd.read_csv(filepath, header=None, nrows=num_rows)
        
        # Display with row numbers
        for idx, row in df_preview.iterrows():
            print(f"Row {idx}: {list(row)}")
            
    except Exception as e:
        print(f"Error previewing file: {str(e)}")


def detect_actual_header_row(filepath: Path, max_rows: int = 10) -> int:
    """Attempt to detect the actual header row in a file.
    
    Args:
        filepath: Path to file
        max_rows: Maximum rows to scan
        
    Returns:
        Estimated header row (0-indexed)
    """
    try:
        if filepath.suffix.lower() in ['.xlsx', '.xls']:
            df_preview = pd.read_excel(filepath, header=None, nrows=max_rows)
        else:
            df_preview = pd.read_csv(filepath, header=None, nrows=max_rows)
        
        # Look for row with text that looks like column headers
        for idx, row in df_preview.iterrows():
            row_str = ' '.join(str(cell).lower() for cell in row if pd.notna(cell))
            
            # Common header indicators
            header_indicators = [
                'tracking', 'invoice', 'date', 'cost', 'charge', 
                'recipient', 'service', 'weight', 'reference'
            ]
            
            if any(indicator in row_str for indicator in header_indicators):
                print(f"Detected likely header row at index {idx}: {list(row)}")
                return idx
        
        # Default to row 0 if no clear header detected
        return 0
        
    except Exception:
        return 0