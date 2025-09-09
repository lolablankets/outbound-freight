"""Analysis modules for calculating weighted average shipping costs."""

from .aggregator import aggregate_shipping_cost_and_item_quantity_data
from .basket import define_unique_basket_combos, count_unique_basket_combo_occurrences
from .shares import (
    calculate_share_of_orders_by_basket_type,
    calculate_share_of_items_by_basket_type, 
    calculate_share_of_all_blankets_by_basket_type
)
from .calculator import (
    calculate_cost_per_product_by_basket_type,
    calculate_weighted_cost_per_product,
    calculate_weighted_cost_per_order,
    calculate_weighted_cost_per_all_blankets
)
from .reporter import generate_outbound_shipping_cost_report

__all__ = [
    "aggregate_shipping_cost_and_item_quantity_data",
    "define_unique_basket_combos",
    "count_unique_basket_combo_occurrences",
    "calculate_share_of_orders_by_basket_type",
    "calculate_share_of_items_by_basket_type",
    "calculate_share_of_all_blankets_by_basket_type", 
    "calculate_cost_per_product_by_basket_type",
    "calculate_weighted_cost_per_product",
    "calculate_weighted_cost_per_order",
    "calculate_weighted_cost_per_all_blankets",
    "generate_outbound_shipping_cost_report"
]