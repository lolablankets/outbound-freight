"""Vendor detection logic based on filename patterns."""

import re
from pathlib import Path
from ..config import Vendor, get_header_offset


def detect_vendor(filename: str) -> Vendor:
    """Detect shipping vendor from filename patterns.
    
    Uses filename heuristics to identify vendor:
    - FedEx: Contains 'fdx' or 'fedex' (case insensitive)
    - UPS: Contains 'ups' (case insensitive)
    - USPS: Contains 'usps' or 'stamps' (case insensitive)
    
    Args:
        filename: Name of the invoice file
        
    Returns:
        Vendor enum indicating detected vendor or UNKNOWN
        
    Example:
        >>> detect_vendor("FDX_20250802_LOL509.xlsx")
        Vendor.FEDEX
    """
    filename_lower = filename.lower()
    
    # FedEx patterns
    if re.search(r'fdx|fedex', filename_lower):
        return Vendor.FEDEX
    
    # UPS patterns  
    if re.search(r'ups', filename_lower):
        return Vendor.UPS
    
    # USPS patterns
    if re.search(r'usps|stamps', filename_lower):
        return Vendor.USPS
    
    return Vendor.UNKNOWN


def detect_vendor_from_path(filepath: Path) -> Vendor:
    """Detect vendor from file path.
    
    Args:
        filepath: Path object to invoice file
        
    Returns:
        Detected vendor enum
    """
    return detect_vendor(filepath.name)


def get_vendor_patterns() -> dict:
    """Get all vendor detection patterns for reference.
    
    Returns:
        Dictionary mapping vendors to their filename patterns
    """
    return {
        Vendor.FEDEX: ['fdx', 'fedex'],
        Vendor.UPS: ['ups'], 
        Vendor.USPS: ['usps', 'stamps']
    }