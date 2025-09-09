"""FedEx-specific invoice processing."""

from typing import Dict
import pandas as pd
from .base import VendorProcessor
from ..config import Vendor


class FedExProcessor(VendorProcessor):
    """FedEx invoice processor with vendor-specific logic."""
    
    def __init__(self):
        super().__init__(Vendor.FEDEX)
    
    def get_column_mapping(self) -> Dict[str, str]:
        """Get FedEx column mapping to standard schema.
        
        Based on FedEx schema documentation in docs/fedex_schema.md
        """
        return {
            'Tracking Number': 'tracking_number',
            'Invoice Date': 'invoice_date', 
            'Ship Date': 'ship_date',
            'Service Type': 'service_type',
            'Net Charge': 'shipping_cost',  # FedEx uses "Net Charge"
            'Actual Weight': 'actual_weight',
            'Billed Weight': 'billed_weight',
            'Recipient Company': 'recipient_name',
            'Recipient State': 'recipient_state',
            'Recipient Zipcode': 'recipient_zip',
            'Recipient Country': 'recipient_country',
            'Reference 1': 'reference_1',  # M-numbers
            'Reference 2': 'reference_2',  # #-numbers
            'Reference 4': 'reference_4',  # LOL509 account identifier
            'Zone': 'zone',
            'Dim Length': 'package_length',
            'Dim Width': 'package_width', 
            'Dim Height': 'package_height'
        }
    
    def preprocess_dataframe(self, df: pd.DataFrame) -> pd.DataFrame:
        """Apply FedEx-specific preprocessing.
        
        Args:
            df: Raw FedEx DataFrame
            
        Returns:
            Preprocessed DataFrame
        """
        # Remove currency symbols from Net Charge
        if 'Net Charge' in df.columns:
            df['Net Charge'] = df['Net Charge'].astype(str).str.replace('$', '').str.replace(',', '')
            df['Net Charge'] = pd.to_numeric(df['Net Charge'], errors='coerce')
        
        # Normalize weight fields
        for weight_col in ['Actual Weight', 'Billed Weight']:
            if weight_col in df.columns:
                df[weight_col] = pd.to_numeric(df[weight_col], errors='coerce')
        
        # Clean up reference fields (remove extra whitespace)
        for ref_col in ['Reference 1', 'Reference 2', 'Reference 4']:
            if ref_col in df.columns:
                df[ref_col] = df[ref_col].astype(str).str.strip()
        
        return df
    
    def validate_required_fields(self, df: pd.DataFrame) -> bool:
        """Validate FedEx required fields.
        
        Args:
            df: FedEx DataFrame to validate
            
        Returns:
            True if all required fields present
        """
        required_fields = [
            'Tracking Number',
            'Ship Date', 
            'Net Charge',
            'Recipient State',
            'Service Type'
        ]
        
        missing_fields = [field for field in required_fields if field not in df.columns]
        
        if missing_fields:
            print(f"Missing required FedEx fields: {missing_fields}")
            return False
            
        return True