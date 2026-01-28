#!/usr/bin/env python3
"""
Synthetic Data Producer for BCM Baseview Dashboards

Generates fake metrics for:
1. Rack-level power and temperature (A05, A06, A07 standalone racks)
2. Node-level GPU temperature for real DGX nodes
3. Switch health status for network switches
"""
import sys
import json
import random

# =============================================================================
# CONFIGURATION - Edit these lists to match your environment
# =============================================================================

# Standalone rack entities (will be created via cmsh monitoring standalone)
RACKS = ["A05", "A06", "A07"]

# Real DGX nodes in your cluster (for node-level GPU metrics)
DGX_NODES = [
    "a05-p1-dgx-01-c01",
    "a05-p1-dgx-01-c02",
    "a05-p1-dgx-01-c03",
    "a05-p1-dgx-01-c04",
    "a05-p1-dgx-01-c05",
    "a05-p1-dgx-01-c06",
    "a05-p1-dgx-01-c07",
    "a05-p1-dgx-01-c08",
    "a05-p1-dgx-01-c09",
    "a05-p1-dgx-01-c10",
    "a05-p1-dgx-01-c11",
    "a05-p1-dgx-01-c12",
    "a05-p1-dgx-01-c13",
    "a05-p1-dgx-01-c14",
    "a05-p1-dgx-01-c15",
    "a05-p1-dgx-01-c16",
    "a05-p1-dgx-01-c17",
    "a05-p1-dgx-01-c18",
]

# Network switches for health checks
SWITCHES = [
    "a03-p1-btor-01",
    "a03-p1-ftor-01",
    "a03-p1-tor-01",
    "a04-p1-spine-01",
    "a04-p1-stor-01",
    "a04-p1-tor-02",
]

# =============================================================================
# METRIC DEFINITIONS
# =============================================================================


def initialize():
    """
    Define all metrics that will be collected.
    This MUST match exactly what sample() outputs.
    """
    metrics = []

    # Rack-level power and temperature for standalone racks
    for rack in RACKS:
        metrics.append({
            "metric": "totalnodepowerusage",
            "entity": rack,
            "unit": "W",
            "class": "Power/Rack",
        })
        metrics.append({
            "metric": "TotalGPUTemperature",
            "entity": rack,
            "unit": "C",
            "class": "Temperature/Rack",
        })

    # Node-level GPU temperature average for real DGX nodes
    for node in DGX_NODES:
        metrics.append({
            "metric": "gpu_temperature:average",
            "entity": node,
            "unit": "C",
            "class": "GPU",
        })

    # Switch health status (DeviceStatusOk = 1 means healthy)
    for switch in SWITCHES:
        metrics.append({
            "metric": "DeviceStatusOk",
            "entity": switch,
            "class": "Internal",
        })

    return metrics


def sample():
    """
    Generate sample values for all metrics.
    This MUST match exactly what initialize() defines.
    """
    metrics = []

    # Rack-level metrics with varying power consumption
    power_ranges = {
        "A05": (130000.0, 135000.0),  # High power rack (many GPUs)
        "A06": (60000.0, 65000.0),    # Medium power rack
        "A07": (55000.0, 60000.0),    # Medium power rack
    }
    temp_ranges = {
        "A05": (75.0, 85.0),  # Higher temp due to higher load
        "A06": (55.0, 65.0),
        "A07": (50.0, 60.0),
    }

    for rack in RACKS:
        power_min, power_max = power_ranges.get(rack, (50000.0, 60000.0))
        temp_min, temp_max = temp_ranges.get(rack, (50.0, 65.0))

        metrics.append({
            "metric": "totalnodepowerusage",
            "entity": rack,
            "value": random.uniform(power_min, power_max),
        })
        metrics.append({
            "metric": "TotalGPUTemperature",
            "entity": rack,
            "value": random.uniform(temp_min, temp_max),
        })

    # Node-level GPU temperature for real DGX nodes
    for node in DGX_NODES:
        metrics.append({
            "metric": "gpu_temperature:average",
            "entity": node,
            "value": random.uniform(45.0, 75.0),
        })

    # Switch health - always healthy (1 = PASS)
    for switch in SWITCHES:
        metrics.append({
            "metric": "DeviceStatusOk",
            "entity": switch,
            "value": 1,
        })

    return metrics


def main():
    args = sys.argv[1:]
    is_init = any(a == "--initialize" for a in args)

    if is_init:
        data = initialize()
    else:
        data = sample()

    print(json.dumps(data))


if __name__ == "__main__":
    main()