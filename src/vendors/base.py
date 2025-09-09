"""Base classes and interfaces for vendor-specific processing."""

from abc import ABC, abstractmethod
from typing import Dict, Any
import pandas as pd
from ..config import Vendor


class VendorProcessor(ABC):
    """Abstract base class for vendor-specific invoice processing."""
    
    def __init__(self, vendor: Vendor):
        self.vendor = vendor
    
    @abstractmethod
    def get_column_mapping(self) -> Dict[str, str]:
        """Get mapping from vendor columns to standard schema.
        
        Returns:
            Dictionary mapping vendor column names to standard field names
        """
        pass
    
    @abstractmethod
    def preprocess_dataframe(self, df: pd.DataFrame) -> pd.DataFrame:
        """Apply vendor-specific preprocessing before mapping.
        
        Args:
            df: Raw vendor DataFrame
            
        Returns:
            Preprocessed DataFrame ready for column mapping
        """
        pass
    
    @abstractmethod
    def validate_required_fields(self, df: pd.DataFrame) -> bool:
        """Validate that required vendor fields are present.
        
        Args:
            df: Vendor DataFrame to validate
            
        Returns:
            True if all required fields present, False otherwise
        """
        pass
    
    def process_dataframe(self, df: pd.DataFrame) -> pd.DataFrame:
        """Complete processing pipeline for vendor data.
        
        Args:
            df: Raw vendor DataFrame
            
        Returns:
            Processed DataFrame with standard schema
        """
        # Validate input
        if not self.validate_required_fields(df):
            raise ValueError(f"Missing required fields for {self.vendor.value}")
        
        # Apply vendor-specific preprocessing
        df = self.preprocess_dataframe(df)
        
        # Apply column mapping
        mapping = self.get_column_mapping()
        df = df.rename(columns=mapping)
        
        # Add vendor identification
        df['vendor'] = self.vendor.value
        
        return df