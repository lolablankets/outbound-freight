"""Integration modules for connecting with external data sources and matching."""

from .snowflake import get_snowflake_connection, run_order_query, extract_date_range_from_invoices
from .matcher import parse_shopify_order_codes, join_shopify_data_with_invoice_data
from .quality import quality_check_shopify_data_join
from .fallback import perform_fallback_join_strategies

__all__ = [
    "get_snowflake_connection",
    "run_order_query", 
    "extract_date_range_from_invoices",
    "parse_shopify_order_codes",
    "join_shopify_data_with_invoice_data",
    "quality_check_shopify_data_join",
    "perform_fallback_join_strategies"
]