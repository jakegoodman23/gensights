"""
Test script for the simplified DataProcessor class.
"""

import os
import sys
from data_processor import DataProcessor
import pandas as pd
import json


def create_sample_csv():
    """Create a sample CSV file for testing the DataProcessor."""
    # Create sample data
    data = {
        "dt_month": [
            "2023-01-01",
            "2023-01-01",
            "2023-01-01",
            "2023-02-01",
            "2023-02-01",
            "2023-02-01",
            "2023-03-01",
            "2023-03-01",
            "2023-03-01",
            "2023-04-01",
            "2023-04-01",
            "2023-04-01",
        ],
        "location_name": [
            "Loc1",
            "Loc2",
            "Loc3",
            "Loc1",
            "Loc2",
            "Loc3",
            "Loc1",
            "Loc2",
            "Loc3",
            "Loc1",
            "Loc2",
            "Loc3",
        ],
        "region_name": [
            "East",
            "West",
            "East",
            "East",
            "West",
            "East",
            "East",
            "West",
            "East",
            "East",
            "West",
            "East",
        ],
        "case_volume": [100, 150, 120, 105, 145, 125, 110, 140, 130, 115, 135, 135],
        "fcots_num": [80, 120, 100, 85, 115, 105, 90, 110, 110, 95, 105, 115],
        "fcots_den": [100, 150, 120, 105, 145, 125, 110, 140, 130, 115, 135, 135],
        "turnover_num": [
            1500,
            2100,
            1800,
            1550,
            2050,
            1850,
            1600,
            2000,
            1900,
            1650,
            1950,
            1950,
        ],
        "turnover_den": [100, 150, 120, 105, 145, 125, 110, 140, 130, 115, 135, 135],
        "ptu_num": [800, 1200, 1000, 850, 1150, 1050, 900, 1100, 1100, 950, 1050, 1150],
        "ptu_den": [
            1000,
            1500,
            1200,
            1050,
            1450,
            1250,
            1100,
            1400,
            1300,
            1150,
            1350,
            1350,
        ],
        "add_on_num": [10, 15, 12, 11, 14, 13, 12, 13, 14, 13, 12, 15],
        "add_on_den": [100, 150, 120, 105, 145, 125, 110, 140, 130, 115, 135, 135],
        "denial_rate_num": [5, 8, 6, 5, 7, 6, 6, 7, 7, 6, 6, 8],
        "denial_rate_den": [100, 150, 120, 105, 145, 125, 110, 140, 130, 115, 135, 135],
    }

    # Create DataFrame and save to CSV
    df = pd.DataFrame(data)
    test_file = "test_data.csv"
    df.to_csv(test_file, index=False)
    print(f"Created test file: {test_file}")
    return test_file


def test_data_processor():
    """Test the DataProcessor class with sample data."""
    # Create test data
    test_file = create_sample_csv()

    # Process the data
    processor = DataProcessor(test_file)
    region_dict, customer_dict = processor.process_file()

    # Print the results
    if region_dict is not None and customer_dict is not None:
        print("Successfully processed data!")

        # Print sample of region dictionary
        print("\nSample of region dictionary:")
        for region, data in region_dict.items():
            print(f"Region: {region}")
            print(f"Number of quarters: {len(data)}")
            print("First quarter data:")
            print(json.dumps(data[0], indent=2))
            break

        # Print sample of customer dictionary
        print("\nSample of customer dictionary:")
        print(f"Number of quarters: {len(customer_dict['overall'])}")
        print("First quarter data:")
        print(json.dumps(customer_dict["overall"][0], indent=2))

        return True
    else:
        print("Failed to process data!")
        return False


if __name__ == "__main__":
    print("Testing DataProcessor...")
    success = test_data_processor()
    if success:
        print("\nTest completed successfully!")
    else:
        print("\nTest failed!")
        sys.exit(1)
