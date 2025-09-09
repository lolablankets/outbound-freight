from __future__ import annotations

from dataclasses import dataclass
from enum import Enum, auto
from pathlib import Path
from typing import Optional, Union


class Vendor(Enum):
    FEDEX = auto()
    UPS = auto()
    USPS = auto()
    UNKNOWN = auto()


PathLike = Union[str, Path]


def detect_vendor(path: PathLike) -> Vendor:
    """Detect vendor from a file path using filename heuristics.

    Initial behavior is filename-based only. Content heuristics can be added later.
    """
    p = Path(path)
    name = p.name.lower()

    # Simple filename heuristics
    if "ups" in name:
        return Vendor.UPS
    if "usps" in name or "stamps" in name:
        return Vendor.USPS
    if name.startswith("fdx") or "fdx" in name or "fedex" in name:
        return Vendor.FEDEX

    return Vendor.UNKNOWN


__all__ = ["Vendor", "detect_vendor"]

