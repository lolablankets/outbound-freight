"""File discovery and backup utilities for invoice processing."""

import shutil
from pathlib import Path
from typing import List
from ..config import get_period_data_path, TEMP_PATH, TEMP_PATH_BACKUP


def discover_invoice_files(analysis_period: str) -> List[Path]:
    """Find all invoice files for specific analysis period.
    
    Scans data/{analysis_period}/ directory for vendor invoice files.
    Validates file existence and formats before processing.
    
    Args:
        analysis_period: Period path like "2025/08" for data/2025/08/
        
    Returns:
        List of Path objects for all invoice files in the period
        
    Raises:
        FileNotFoundError: If analysis period directory doesn't exist
        ValueError: If no valid invoice files found in period
        
    Example:
        files = discover_invoice_files("2025/08")
        # Returns paths to all .xlsx/.csv files in data/2025/08/
    """
    period_path = get_period_data_path(analysis_period)
    
    if not period_path.exists():
        raise FileNotFoundError(f"Analysis period directory not found: {period_path}")
    
    # Supported file extensions
    supported_extensions = {'.xlsx', '.xls', '.csv'}
    
    # Find all invoice files
    invoice_files = []
    for file_path in period_path.iterdir():
        if file_path.is_file() and file_path.suffix.lower() in supported_extensions:
            invoice_files.append(file_path)
    
    if not invoice_files:
        raise ValueError(f"No valid invoice files found in period: {analysis_period}")
    
    # Sort by filename for consistent processing order
    invoice_files.sort(key=lambda x: x.name)
    
    print(f"Found {len(invoice_files)} invoice files for period {analysis_period}")
    for file_path in invoice_files:
        print(f"  - {file_path.name}")
    
    return invoice_files


def validate_file_format(filepath: Path) -> bool:
    """Validate that file can be processed.
    
    Args:
        filepath: Path to invoice file
        
    Returns:
        True if file format is supported
    """
    supported_extensions = {'.xlsx', '.xls', '.csv'}
    return filepath.suffix.lower() in supported_extensions


def backup_processing_files(analysis_period: str) -> None:
    """Backup processing files for specific analysis period.
    
    Moves files from current_batch to last_batch directory before
    processing new period. Ensures recovery capability if processing fails.
    
    Args:
        analysis_period: Period being processed like "2025/08"
        
    Example:
        backup_processing_files("2025/08")
    """
    current_path = Path(TEMP_PATH)
    backup_path = Path(TEMP_PATH_BACKUP)
    
    # Create backup directory if it doesn't exist
    backup_path.mkdir(parents=True, exist_ok=True)
    
    # If current processing directory exists, move it to backup
    if current_path.exists():
        # Remove existing backup if present
        if backup_path.exists():
            shutil.rmtree(backup_path)
        
        # Move current to backup
        shutil.move(str(current_path), str(backup_path))
        print(f"Backed up previous processing files to {backup_path}")
    
    # Create fresh current processing directory
    current_path.mkdir(parents=True, exist_ok=True)
    print(f"Created fresh processing directory for period {analysis_period}")


def get_file_stats(analysis_period: str) -> dict:
    """Get statistics about files in analysis period.
    
    Args:
        analysis_period: Period to analyze
        
    Returns:
        Dictionary with file statistics
    """
    try:
        files = discover_invoice_files(analysis_period)
    except (FileNotFoundError, ValueError):
        return {"file_count": 0, "total_size_mb": 0, "file_types": {}}
    
    stats = {
        "file_count": len(files),
        "total_size_mb": 0,
        "file_types": {}
    }
    
    for file_path in files:
        # Add to size total
        size_mb = file_path.stat().st_size / (1024 * 1024)
        stats["total_size_mb"] += size_mb
        
        # Count by extension
        ext = file_path.suffix.lower()
        stats["file_types"][ext] = stats["file_types"].get(ext, 0) + 1
    
    stats["total_size_mb"] = round(stats["total_size_mb"], 2)
    
    return stats