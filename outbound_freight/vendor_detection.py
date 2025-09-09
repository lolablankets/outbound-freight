"""
Vendor detection from invoice filenames.

Identifies shipping vendors (FedEx, UPS, USPS) based on filename patterns.
"""

from enum import Enum
from typing import List, Optional, Tuple


class Vendor(Enum):
    """Enumeration of supported shipping vendors."""
    FEDEX = "fedex"
    UPS = "ups" 
    USPS = "usps"
    UNKNOWN = "unknown"


# Vendor keyword mappings - easily extensible for new patterns
VENDOR_KEYWORDS = {
    Vendor.FEDEX: ["fdx", "fedex"],
    Vendor.UPS: ["ups"],
    Vendor.USPS: ["usps", "stamps"],
}


def _find_earliest_keyword_position(text: str, keywords: List[str]) -> int:
    """
    Find the position of the earliest occurring keyword in text.
    
    Args:
        text: The text to search in (should be lowercase)
        keywords: List of keywords to search for
        
    Returns:
        Position of earliest keyword, or -1 if none found
    """
    positions = [text.find(keyword) for keyword in keywords if keyword in text]
    return min(positions) if positions else -1


def detect_vendor(filename: Optional[str]) -> Vendor:
    """
    Detect shipping vendor from filename using keyword patterns.
    
    Args:
        filename: The filename to analyze (case insensitive)
        
    Returns:
        Vendor enum value based on filename patterns
        
    Note:
        When multiple vendor keywords are present, the order of appearance
        in the filename determines priority (first match wins).
        
    Examples:
        >>> detect_vendor("FDX_20250802_LOL509.xlsx")
        <Vendor.FEDEX: 'fedex'>
        >>> detect_vendor("UPS_LOL509_08022025.xlsx") 
        <Vendor.UPS: 'ups'>
        >>> detect_vendor("unknown_file.xlsx")
        <Vendor.UNKNOWN: 'unknown'>
    """
    if not filename:
        return Vendor.UNKNOWN
        
    filename_lower = filename.lower()
    
    # Find earliest position for each vendor's keywords
    vendor_positions: List[Tuple[int, Vendor]] = []
    
    for vendor, keywords in VENDOR_KEYWORDS.items():
        position = _find_earliest_keyword_position(filename_lower, keywords)
        if position != -1:
            vendor_positions.append((position, vendor))
    
    # Return vendor with earliest keyword position, or UNKNOWN if none found
    if not vendor_positions:
        return Vendor.UNKNOWN
        
    # Sort by position and return the vendor with the earliest match
    vendor_positions.sort(key=lambda x: x[0])
    return vendor_positions[0][1]