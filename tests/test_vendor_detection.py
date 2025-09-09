import os
from pathlib import Path

import pytest

from outbound_freight import Vendor, detect_vendor


def test_detect_vendor_by_filename_fedex_variants(tmp_path: Path):
    cases = [
        "FDX_20250802_LOL509.xlsx",
        "fdx-20250809_lol509.xlsx",
        "FedEx_invoice_aug.csv",
    ]
    for name in cases:
        p = tmp_path / name
        p.write_text("dummy")
        assert detect_vendor(p) is Vendor.FEDEX


def test_detect_vendor_by_filename_ups_variants(tmp_path: Path):
    cases = [
        "UPS_LOL509_08022025.xlsx",
        "ups_lol509_08092025.xlsx",
        "2025-08-ups-billing.csv",
    ]
    for name in cases:
        p = tmp_path / name
        p.write_text("dummy")
        assert detect_vendor(p) is Vendor.UPS


def test_detect_vendor_by_filename_usps_variants(tmp_path: Path):
    cases = [
        "USPS_aug_week1.csv",
        "usps-2025-08-report.xlsx",
        "stamps_com_export.csv",
    ]
    for name in cases:
        p = tmp_path / name
        p.write_text("dummy")
        assert detect_vendor(p) is Vendor.USPS


def test_detect_vendor_unknown(tmp_path: Path):
    p = tmp_path / "random_file.xlsx"
    p.write_text("dummy")
    assert detect_vendor(p) is Vendor.UNKNOWN


@pytest.mark.parametrize(
    "path,expected",
    [
        (Path("data/2025/08/FDX_20250802_LOL509.xlsx"), Vendor.FEDEX),
        (Path("data/2025/08/FDX-20250809_LOL509.xlsx"), Vendor.FEDEX),
        (Path("data/2025/08/FDX-20250816_LOL509.xlsx"), Vendor.FEDEX),
        (Path("data/2025/08/FDX-20250823_LOL509.xlsx"), Vendor.FEDEX),
        (Path("data/2025/08/FDX-20250830_LOL509.xlsx"), Vendor.FEDEX),
        (Path("data/2025/08/UPS_LOL509_08022025.xlsx"), Vendor.UPS),
        (Path("data/2025/08/UPS_LOL509_08092025.xlsx"), Vendor.UPS),
        (Path("data/2025/08/UPS_LOL509_08162025.xlsx"), Vendor.UPS),
        (Path("data/2025/08/UPS_LOL509_08232025.xlsx"), Vendor.UPS),
        (Path("data/2025/08/UPS_LOL509_08302025.xlsx"), Vendor.UPS),
    ],
)
def test_detect_vendor_against_repository_samples(path: Path, expected: Vendor):
    # Ensure the sample file exists in the repository so the test is meaningful.
    assert path.exists(), f"Missing expected sample: {path}"
    assert detect_vendor(path) is expected

