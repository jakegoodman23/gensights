"""
This module contains definitions for metrics used in the ROI Automation Dashboard.
These metrics are used to analyze data and identify trends.
"""

# Metric definitions dictionary
# Each metric has:
# - description: human-readable explanation of the metric
# - formula: how the metric is calculated (expressed as a string referring to column names)
# - goal: whether higher or lower values are better for this metric
# - format: how to display the metric (percentage, decimal, integer, etc.)
# - category: the type of metric (operational, financial, etc.)

METRIC_DEFINITIONS = {
    "case_volume": {
        "description": "Total number of cases performed",
        "formula": "case_volume",
        "goal": "higher",
        "format": "integer",
        "category": "volume",
    },
    "fcots_pct": {
        "description": "First Case On-Time Start Percentage",
        "formula": "fcots_num / fcots_den",
        "goal": "higher",
        "format": "percentage",
        "category": "efficiency",
    },
    "turnover_time": {
        "description": "Average time between cases (minutes)",
        "formula": "turnover_num / turnover_den",
        "goal": "lower",
        "format": "decimal",
        "category": "efficiency",
    },
    "utilization_pct": {
        "description": "Room utilization percentage",
        "formula": "ptu_num / ptu_den",
        "goal": "higher",
        "format": "percentage",
        "category": "efficiency",
    },
    "add_on_pct": {
        "description": "Percentage of cases that were added on",
        "formula": "add_on_num / add_on_den",
        "goal": "lower",
        "format": "percentage",
        "category": "scheduling",
    },
    "denial_rate_pct": {
        "description": "Percentage of requests that were denied",
        "formula": "denial_rate_num / denial_rate_den",
        "goal": "lower",
        "format": "percentage",
        "category": "scheduling",
    },
}


def get_metric_names():
    """Return a list of all metric names."""
    return list(METRIC_DEFINITIONS.keys())


def get_metric_info(metric_name):
    """Return detailed information about a specific metric."""
    return METRIC_DEFINITIONS.get(metric_name, None)


def get_metrics_by_category(category):
    """Return all metrics belonging to a specific category."""
    return {
        k: v for k, v in METRIC_DEFINITIONS.items() if v.get("category") == category
    }


def get_metric_categories():
    """Return a list of all unique metric categories."""
    return list(set(metric["category"] for metric in METRIC_DEFINITIONS.values()))
