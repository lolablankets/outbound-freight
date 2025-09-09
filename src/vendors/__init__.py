"""Vendor-specific processing modules for shipping invoice data."""

from .detector import detect_vendor, detect_vendor_from_path, get_vendor_patterns
from .base import VendorProcessor
from .fedex import FedExProcessor
from .ups import UPSProcessor
from .usps import USPSProcessor

__all__ = [
    "detect_vendor", 
    "detect_vendor_from_path", 
    "get_vendor_patterns",
    "VendorProcessor",
    "FedExProcessor",
    "UPSProcessor", 
    "USPSProcessor"
]