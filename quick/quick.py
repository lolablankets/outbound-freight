import pandas as pd
import polars as pl

data_path = "data/2025/08"
fedex_header_offset = 3
ups_header_offset = 1

def backup_processing_files():
    pass

def determine_file_vendor():
    pass

def read_file_into_memory():
    pass

def merge_same_vendor_files():
    pass

def convert_dollar_to_float():
    pass

def convert_string_to_date():
    pass

def map_vendor_columns_to_shared_schema():
    pass

def combine_vendor_files():
    pass

def parse_shopify_order_codes():
    pass

def get_snowflake_connection():
    pass

def run_order_query():
    pass

def join_shopify_data_with_invoice_data():
    pass

def quality_check_shopify_data_join():
    pass

def perform_fallback_join_strategies():
    pass

def dedupe_order_shipping_rows():
    pass

def aggregate_shipping_cost_and_item_quantity_data():
    pass

def define_unique_basket_combos():
    pass

def count_unique_basket_combo_occurrences():
    pass

def calculate_share_of_orders_by_basket_type():
    pass

def calculate_share_of_items_by_basket_type():
    pass

def calculate_cost_per_product_by_basket_type():
    pass

def calculate_share_of_all_blankets_by_basket_type():
    pass

def calculate_weighted_cost_per_product():
    pass

def calculate_weighted_cost_per_order():
    pass

def calculate_weighted_cost_per_all_blankets():
    pass

def run_invoice_etl():
    pass

def perform_share_and_cost_analysis():
    pass

def generate_outbound_shipping_cost_report():
    pass

def run_outbound_shipping_pipeline():
    pass

