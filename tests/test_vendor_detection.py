import pytest
from pathlib import Path
from outbound_freight.vendor_detection import Vendor, detect_vendor


class TestVendorDetection:
    """Test suite for vendor detection from filenames."""

    def test_fedex_detection_fdx_lowercase(self):
        """Test FedEx detection with 'fdx' keyword."""
        assert detect_vendor("fdx_invoice_123.xlsx") == Vendor.FEDEX

    def test_fedex_detection_fdx_uppercase(self):
        """Test FedEx detection with 'FDX' keyword."""
        assert detect_vendor("FDX_20250802_LOL509.xlsx") == Vendor.FEDEX

    def test_fedex_detection_fedex_lowercase(self):
        """Test FedEx detection with 'fedex' keyword."""
        assert detect_vendor("fedex_invoice_123.xlsx") == Vendor.FEDEX

    def test_fedex_detection_fedex_uppercase(self):
        """Test FedEx detection with 'FEDEX' keyword."""
        assert detect_vendor("FEDEX_INVOICE_123.xlsx") == Vendor.FEDEX

    def test_fedex_detection_mixed_case(self):
        """Test FedEx detection with mixed case."""
        assert detect_vendor("FdX_Invoice_123.xlsx") == Vendor.FEDEX

    def test_ups_detection_lowercase(self):
        """Test UPS detection with 'ups' keyword."""
        assert detect_vendor("ups_invoice_123.xlsx") == Vendor.UPS

    def test_ups_detection_uppercase(self):
        """Test UPS detection with 'UPS' keyword."""
        assert detect_vendor("UPS_LOL509_08022025.xlsx") == Vendor.UPS

    def test_ups_detection_mixed_case(self):
        """Test UPS detection with mixed case."""
        assert detect_vendor("Ups_Invoice_123.xlsx") == Vendor.UPS

    def test_usps_detection_usps_lowercase(self):
        """Test USPS detection with 'usps' keyword."""
        assert detect_vendor("usps_invoice_123.xlsx") == Vendor.USPS

    def test_usps_detection_usps_uppercase(self):
        """Test USPS detection with 'USPS' keyword."""
        assert detect_vendor("USPS_INVOICE_123.xlsx") == Vendor.USPS

    def test_usps_detection_stamps_lowercase(self):
        """Test USPS detection with 'stamps' keyword."""
        assert detect_vendor("stamps_invoice_123.xlsx") == Vendor.USPS

    def test_usps_detection_stamps_uppercase(self):
        """Test USPS detection with 'STAMPS' keyword."""
        assert detect_vendor("STAMPS_INVOICE_123.xlsx") == Vendor.USPS

    def test_unknown_vendor_fallback(self):
        """Test unknown vendor fallback for unrecognized filenames."""
        assert detect_vendor("random_invoice_123.xlsx") == Vendor.UNKNOWN
        assert detect_vendor("invoice.csv") == Vendor.UNKNOWN
        assert detect_vendor("data_file.txt") == Vendor.UNKNOWN

    def test_multiple_vendor_keywords(self):
        """Test handling of multiple vendor keywords - should return first match priority."""
        # FedEx should take priority over UPS if both present
        assert detect_vendor("fdx_ups_combined.xlsx") == Vendor.FEDEX
        assert detect_vendor("ups_fedex_combined.xlsx") == Vendor.UPS

    def test_special_characters_in_filename(self):
        """Test handling of special characters and numbers."""
        assert detect_vendor("FDX-20250809_LOL509.xlsx") == Vendor.FEDEX
        assert detect_vendor("UPS_LOL509_08/02/2025.xlsx") == Vendor.UPS
        assert detect_vendor("fdx@invoice#123.xlsx") == Vendor.FEDEX

    def test_empty_filename(self):
        """Test handling of empty filename."""
        assert detect_vendor("") == Vendor.UNKNOWN

    def test_none_filename(self):
        """Test handling of None filename."""
        assert detect_vendor(None) == Vendor.UNKNOWN

    def test_actual_sample_files(self):
        """Test against actual sample files in data/2025/08/."""
        data_dir = Path("data/2025/08/")
        if data_dir.exists():
            sample_files = list(data_dir.glob("*.xlsx"))
            
            # Test each sample file
            for file_path in sample_files:
                filename = file_path.name
                vendor = detect_vendor(filename)
                
                if "FDX" in filename.upper():
                    assert vendor == Vendor.FEDEX, f"File {filename} should be detected as FEDEX"
                elif "UPS" in filename.upper():
                    assert vendor == Vendor.UPS, f"File {filename} should be detected as UPS"
                elif "USPS" in filename.upper() or "STAMPS" in filename.upper():
                    assert vendor == Vendor.USPS, f"File {filename} should be detected as USPS"
                else:
                    # If no clear pattern, could be UNKNOWN
                    assert vendor in [Vendor.FEDEX, Vendor.UPS, Vendor.USPS, Vendor.UNKNOWN]

    def test_case_insensitive_matching(self):
        """Test that matching is truly case insensitive."""
        test_cases = [
            ("fdx", Vendor.FEDEX),
            ("FDX", Vendor.FEDEX),
            ("FdX", Vendor.FEDEX),
            ("fedex", Vendor.FEDEX),
            ("FEDEX", Vendor.FEDEX),
            ("FedEx", Vendor.FEDEX),
            ("ups", Vendor.UPS),
            ("UPS", Vendor.UPS),
            ("Ups", Vendor.UPS),
            ("usps", Vendor.USPS),
            ("USPS", Vendor.USPS),
            ("UsPs", Vendor.USPS),
            ("stamps", Vendor.USPS),
            ("STAMPS", Vendor.USPS),
            ("Stamps", Vendor.USPS),
        ]
        
        for keyword, expected_vendor in test_cases:
            filename = f"{keyword}_test_file.xlsx"
            assert detect_vendor(filename) == expected_vendor, f"Failed for keyword: {keyword}"