"""
Simplified data processing module for ROI Automation Dashboard.
This module handles loading, preprocessing, and aggregating CSV data at quarter level.
"""

import pandas as pd
import numpy as np

from metric_definitions import METRIC_DEFINITIONS


class DataProcessor:
    def __init__(self, csv_file_path):
        """Initialize the data processor with a CSV file path."""
        self.csv_file_path = csv_file_path
        self.raw_data = pd.read_csv(self.csv_file_path)

    def preprocess_data(self):
        """Preprocess the data for analysis."""

        # Make a copy to avoid modifying the original data
        df = self.raw_data.copy()

        df["dt_month"] = pd.to_datetime(df["dt_month"])
        # have column of quarter and year
        df["quarter"] = df["dt_month"].dt.quarter
        df["year"] = df["dt_month"].dt.year
        df["quarter_year"] = (
            "Q" + df["quarter"].astype(str) + " " + df["year"].astype(str)
        )

        df = df[df["quarter_year"].isin(["Q4 2024", "Q3 2024"])]

        metric_cols = [
            "add_on_num",
            "add_on_den",
            "case_volume",
            "case_minutes",
            "turnover_num",
            "turnover_den",
            "fcots_num",
            "fcots_den",
            "release_minutes",
            "denial_rate_num",
            "denial_rate_den",
            "total_request_minutes",
            "ptu_num",
            "ptu_den",
        ]

        for col in metric_cols:
            df[col] = df[col].astype(float)

        customer_df = df.groupby(["quarter_year"])[metric_cols].sum().reset_index()
        region_df = (
            df.groupby(["quarter_year", "region_name"])[metric_cols].sum().reset_index()
        )

        customer_processed_df = self.process_metrics(customer_df)
        region_processed_df = self.process_metrics(region_df)

        return customer_processed_df, region_processed_df

    def process_metrics(self, data: pd.DataFrame) -> pd.DataFrame:
        data["primetime_utilization_pct"] = data["ptu_num"] / data["ptu_den"]
        data["add_on_pct"] = data["add_on_num"] / data["add_on_den"]
        data["turnover_time"] = data["turnover_num"] / data["turnover_den"]
        data["fcots_pct"] = data["fcots_num"] / data["fcots_den"]
        data["denial_rate_pct"] = data["denial_rate_num"] / data["denial_rate_den"]

        return data

    def process_file(self) -> tuple[dict, dict]:
        """
        Process the CSV file and return region and customer level dictionaries.
        This is the main method to call from outside.
        """

        customer_df, region_df = self.preprocess_data()

        customer_df = customer_df[
            [
                "quarter_year",
                "case_volume",
                "case_minutes",
                "turnover_time",
                "add_on_pct",
                "denial_rate_pct",
                "primetime_utilization_pct",
                "fcots_pct",
            ]
        ]
        region_df = region_df[
            [
                "quarter_year",
                "region_name",
                "case_volume",
                "case_minutes",
                "turnover_time",
                "add_on_pct",
                "denial_rate_pct",
                "primetime_utilization_pct",
                "fcots_pct",
            ]
        ]

        # Sort data by quarter_year to ensure chronological order
        customer_df = customer_df.sort_values("quarter_year")
        region_df = region_df.sort_values(["region_name", "quarter_year"])

        # Calculate quarter-over-quarter changes for customer data
        customer_df["case_volume_qoq"] = customer_df["case_volume"].pct_change() * 100
        customer_df["case_minutes_qoq"] = customer_df["case_minutes"].pct_change() * 100
        customer_df["turnover_time_qoq"] = (
            customer_df["turnover_time"].pct_change() * 100
        )
        customer_df["add_on_pct_qoq"] = (
            customer_df["add_on_pct"].diff() * 100
        )  # Percentage point change
        customer_df["denial_rate_pct_qoq"] = (
            customer_df["denial_rate_pct"].diff() * 100
        )  # Percentage point change
        customer_df["primetime_utilization_pct_qoq"] = (
            customer_df["primetime_utilization_pct"].diff() * 100
        )  # Percentage point change
        customer_df["fcots_pct_qoq"] = (
            customer_df["fcots_pct"].diff() * 100
        )  # Percentage point change

        # Calculate quarter-over-quarter changes for region data
        # Group by region_name to ensure changes are calculated within each region
        for region in region_df["region_name"].unique():
            mask = region_df["region_name"] == region
            region_df.loc[mask, "case_volume_qoq"] = (
                region_df.loc[mask, "case_volume"].pct_change() * 100
            )
            region_df.loc[mask, "case_minutes_qoq"] = (
                region_df.loc[mask, "case_minutes"].pct_change() * 100
            )
            region_df.loc[mask, "turnover_time_qoq"] = (
                region_df.loc[mask, "turnover_time"].pct_change() * 100
            )
            region_df.loc[mask, "add_on_pct_qoq"] = (
                region_df.loc[mask, "add_on_pct"].diff() * 100
            )
            region_df.loc[mask, "denial_rate_pct_qoq"] = (
                region_df.loc[mask, "denial_rate_pct"].diff() * 100
            )
            region_df.loc[mask, "primetime_utilization_pct_qoq"] = (
                region_df.loc[mask, "primetime_utilization_pct"].diff() * 100
            )
            region_df.loc[mask, "fcots_pct_qoq"] = (
                region_df.loc[mask, "fcots_pct"].diff() * 100
            )

        print("CUSTOMER DATA")
        print(customer_df)
        print("REGION DATA")
        print(region_df)
        customer_dict = customer_df.to_dict(orient="records")
        region_dict = region_df.to_dict(orient="records")

        return customer_dict, region_dict
