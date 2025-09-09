"""UPS-specific invoice processing."""

from typing import Dict
import pandas as pd
from .base import VendorProcessor
from ..config import Vendor


class UPSProcessor(VendorProcessor):
    """UPS invoice processor with vendor-specific logic."""
    
    def __init__(self):
        super().__init__(Vendor.UPS)
    
    def get_column_mapping(self) -> Dict[str, str]:
        """Get UPS column mapping to standard schema.
        
        Based on UPS schema documentation in docs/ups_schema.md
        """
        return {
            'Tracking Number': 'tracking_number',
            'Carrier Invoice Date': 'invoice_date',
            'Pickup Date': 'ship_date', 
            'Service': 'service_type',
            'Shipping Cost': 'shipping_cost',  # UPS uses "Shipping Cost"
            'Billed Weight': 'billed_weight',
            'Recipient Name': 'recipient_name',
            'Recipient State': 'recipient_state',
            'Recipient Postal Code': 'recipient_zip',
            'Recipient Country': 'recipient_country',
            'Origin State': 'origin_state',
            'Reference 1': 'reference_1',  # LOLAID codes
            'Reference 2': 'reference_2'   # #-numbers
        }
    
    def preprocess_dataframe(self, df: pd.DataFrame) -> pd.DataFrame:
        """Apply UPS-specific preprocessing.
        
        Args:
            df: Raw UPS DataFrame
            
        Returns:
            Preprocessed DataFrame
        """
        # Remove currency symbols from Shipping Cost
        if 'Shipping Cost' in df.columns:
            df['Shipping Cost'] = df['Shipping Cost'].astype(str).str.replace('$', '').str.replace(',', '')
            df['Shipping Cost'] = pd.to_numeric(df['Shipping Cost'], errors='coerce')
        
        # Normalize weight fields
        if 'Billed Weight' in df.columns:
            df['Billed Weight'] = pd.to_numeric(df['Billed Weight'], errors='coerce')
        
        # Clean up reference fields
        for ref_col in ['Reference 1', 'Reference 2']:
            if ref_col in df.columns:
                df[ref_col] = df[ref_col].astype(str).str.strip()
        
        # Normalize postal codes
        if 'Recipient Postal Code' in df.columns:
            df['Recipient Postal Code'] = df['Recipient Postal Code'].astype(str).str.strip()
        
        return df
    
    def validate_required_fields(self, df: pd.DataFrame) -> bool:
        """Validate UPS required fields.
        
        Args:
            df: UPS DataFrame to validate
            
        Returns:
            True if all required fields present
        """
        required_fields = [
            'Tracking Number',
            'Pickup Date',
            'Shipping Cost', 
            'Recipient State',
            'Service'
        ]
        
        missing_fields = [field for field in required_fields if field not in df.columns]
        
        if missing_fields:
            print(f"Missing required UPS fields: {missing_fields}")
            return False
            
        return True