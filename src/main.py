"""CLI entry point for outbound freight analysis pipeline."""

import sys
import argparse
from .pipeline import run_outbound_shipping_pipeline


def main():
    """Main CLI entry point with argument parsing."""
    parser = argparse.ArgumentParser(
        description="Outbound Freight Processing Pipeline",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python -m src.main 2025/08              # Analyze August 2025
  python -m src.main 2025/07              # Analyze July 2025 
  python -m src.main --period 2025/09     # Analyze September 2025
        """
    )
    
    parser.add_argument(
        'period',
        nargs='?',
        default='2025/08',
        help='Analysis period in YYYY/MM format (default: 2025/08)'
    )
    
    parser.add_argument(
        '--period',
        dest='period_flag',
        help='Alternative way to specify analysis period'
    )
    
    parser.add_argument(
        '--version',
        action='version',
        version='Outbound Freight Pipeline v0.1.0'
    )
    
    args = parser.parse_args()
    
    # Use --period flag if provided, otherwise use positional argument
    analysis_period = args.period_flag if args.period_flag else args.period
    
    print("=" * 60)
    print("Outbound Freight Processing Pipeline")
    print("=" * 60)
    print(f"Analysis Period: {analysis_period}")
    print("=" * 60)
    
    try:
        run_outbound_shipping_pipeline(analysis_period)
    except KeyboardInterrupt:
        print("\\n\\n⚠️  Pipeline interrupted by user")
        sys.exit(1)
    except Exception as e:
        print(f"\\n\\n❌ Pipeline failed: {str(e)}")
        sys.exit(1)


if __name__ == "__main__":
    main()