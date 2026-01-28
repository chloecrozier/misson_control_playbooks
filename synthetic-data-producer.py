#!/usr/bin/env python3
"""
Synthetic data producer for monitoring metrics.

Setup command (run in cmsh):
    cmsh -c "monitoring; setup; use AggregateNode; set excludeCategories dgx-gb200; commit"
"""
import json
import random
import sys

RACKS = ["A05", "A06", "A07"]
K8S_NODES = ["k8s-worker-01", "k8s-control-plane-01", "k8s-control-plane-02", "k8s-control-plane-03"]
INFRA_NODES = ["a09-p1-ibleaf-04-04", "a10-p1-ibspine-01", "a10-p1-ibspine-02", "a10-p1-ibspine-03"]

RACK_CONFIG = {
    "A05": {
        "power": (130000.0, 135000.0),
        "gpu_temp": (75.0, 85.0),
        "cpu_temp": (55.0, 65.0),
        "cpu_util": (40.0, 70.0),
        "memory_total": 2e12,
        "memory_used_pct": (50.0, 80.0),
    },
    "A06": {
        "power": (60000.0, 65000.0),
        "gpu_temp": (55.0, 65.0),
        "cpu_temp": (45.0, 55.0),
        "cpu_util": (20.0, 50.0),
        "memory_total": 1e12,
        "memory_used_pct": (30.0, 60.0),
    },
    "A07": {
        "power": (55000.0, 60000.0),
        "gpu_temp": (50.0, 60.0),
        "cpu_temp": (40.0, 50.0),
        "cpu_util": (15.0, 40.0),
        "memory_total": 1e12,
        "memory_used_pct": (25.0, 50.0),
    },
}


def initialize():
    """Return metric definitions for all racks and nodes."""
    metrics = []
    for rack in RACKS:
        metrics.extend([
            {"metric": "totalnodepowerusage", "entity": rack, "unit": "W", "class": "Power/Rack"},
            {"metric": "TotalCPUPowerUsage", "entity": rack, "unit": "W", "class": "Total"},
            {"metric": "TotalGPUTemperature", "entity": rack, "unit": "C", "class": "Total"},
            {"metric": "TotalCPUTemperature", "entity": rack, "unit": "C", "class": "Total"},
            {"metric": "TotalCPUUtilization", "entity": rack, "unit": "%", "class": "Total"},
            {"metric": "TotalCPUIdle", "entity": rack, "unit": "%", "class": "Total"},
            {"metric": "TotalCPUUser", "entity": rack, "unit": "%", "class": "Total"},
            {"metric": "TotalCPUSystem", "entity": rack, "unit": "%", "class": "Total"},
            {"metric": "TotalMemory", "entity": rack, "unit": "B", "class": "Total"},
            {"metric": "TotalMemoryUsed", "entity": rack, "unit": "B", "class": "Total"},
            {"metric": "TotalMemoryFree", "entity": rack, "unit": "B", "class": "Total"},
            {"metric": "TotalMemoryUtilization", "entity": rack, "unit": "%", "class": "Total"},
            {"metric": "TotalGPUMemoryUtilization", "entity": rack, "unit": "%", "class": "Total"},
            {"metric": "TotalGPUPowerUsage", "entity": rack, "unit": "W", "class": "Total"},
            {"metric": "TotalGPUUtilization", "entity": rack, "unit": "%", "class": "Total"},
        ])

    for node in K8S_NODES:
        metrics.extend([
            {"metric": "gpu_temperature", "parameter": "average", "entity": node, "unit": "C", "class": "GPU"},
            {"metric": "TotalGPUPowerUsage", "entity": node, "unit": "W", "class": "GPU"},
            {"metric": "CPUUsage", "entity": node, "unit": "%", "class": "OS"},
            {"metric": "MemoryUsed", "entity": node, "unit": "B", "class": "OS"},
        ])

    for node in INFRA_NODES:
        metrics.extend([
            {"metric": "CPUUsage", "entity": node, "unit": "%", "class": "OS"},
            {"metric": "MemoryUsed", "entity": node, "unit": "B", "class": "OS"},
        ])

    # k8s-worker-01 specific - standard GPU metric names like gpu_temperature
    metrics.append({"metric": "gpu_power_usage", "parameter": "total", "entity": "k8s-worker-01", "unit": "W", "class": "GPU"})
    metrics.append({"metric": "gpu_utilization", "parameter": "average", "entity": "k8s-worker-01", "unit": "%", "class": "GPU"})
    metrics.append({"metric": "gpu_mem_utilization", "parameter": "average", "entity": "k8s-worker-01", "unit": "%", "class": "GPU"})
    for gpu_id in range(4):
        metrics.append({"metric": "gpu_memory", "parameter": f"gpu{gpu_id}", "entity": "k8s-worker-01", "unit": "B", "class": "GPU"})
        metrics.append({"metric": "gpu_utilization", "parameter": f"gpu{gpu_id}", "entity": "k8s-worker-01", "unit": "%", "class": "GPU"})
        metrics.append({"metric": "gpu_mem_utilization", "parameter": f"gpu{gpu_id}", "entity": "k8s-worker-01", "unit": "%", "class": "GPU"})
    return metrics


def sample():
    """Return sampled metric values for all racks and nodes."""
    metrics = []
    for rack in RACKS:
        cfg = RACK_CONFIG.get(rack, RACK_CONFIG["A07"])
        power = random.uniform(*cfg["power"])
        cpu_util = random.uniform(*cfg["cpu_util"])
        mem_pct = random.uniform(*cfg["memory_used_pct"])
        mem_used = cfg["memory_total"] * (mem_pct / 100.0)

        metrics.extend([
            {"metric": "totalnodepowerusage", "entity": rack, "value": power},
            {"metric": "TotalCPUPowerUsage", "entity": rack, "value": power * 0.15},
            {"metric": "TotalGPUPowerUsage", "entity": rack, "value": power * 0.70},
            {"metric": "TotalGPUTemperature", "entity": rack, "value": random.uniform(*cfg["gpu_temp"])},
            {"metric": "TotalCPUTemperature", "entity": rack, "value": random.uniform(*cfg["cpu_temp"])},
            {"metric": "TotalCPUUtilization", "entity": rack, "value": cpu_util},
            {"metric": "TotalCPUIdle", "entity": rack, "value": 100.0 - cpu_util},
            {"metric": "TotalCPUUser", "entity": rack, "value": cpu_util * 0.7},
            {"metric": "TotalCPUSystem", "entity": rack, "value": cpu_util * 0.3},
            {"metric": "TotalMemory", "entity": rack, "value": cfg["memory_total"]},
            {"metric": "TotalMemoryUsed", "entity": rack, "value": mem_used},
            {"metric": "TotalMemoryFree", "entity": rack, "value": cfg["memory_total"] - mem_used},
            {"metric": "TotalMemoryUtilization", "entity": rack, "value": mem_pct},
            {"metric": "TotalGPUMemoryUtilization", "entity": rack, "value": random.uniform(30.0, 80.0)},
            {"metric": "TotalGPUUtilization", "entity": rack, "value": random.uniform(20.0, 90.0)},
        ])

    for node in K8S_NODES:
        metrics.extend([
            {"metric": "gpu_temperature", "parameter": "average", "entity": node, "value": random.uniform(50.0, 70.0)},
            {"metric": "TotalGPUPowerUsage", "entity": node, "value": random.uniform(250.0, 350.0)},
            {"metric": "CPUUsage", "entity": node, "value": random.uniform(10.0, 60.0)},
            {"metric": "MemoryUsed", "entity": node, "value": random.uniform(4e9, 12e9)},
        ])

    for node in INFRA_NODES:
        metrics.extend([
            {"metric": "CPUUsage", "entity": node, "value": random.uniform(5.0, 40.0)},
            {"metric": "MemoryUsed", "entity": node, "value": random.uniform(1e9, 8e9)},
        ])

    # k8s-worker-01 specific - report as actual percentages (30.0-80.0) not decimals
    metrics.append({"metric": "gpu_power_usage", "parameter": "total", "entity": "k8s-worker-01", "value": random.uniform(200.0, 350.0)})
    metrics.append({"metric": "gpu_utilization", "parameter": "average", "entity": "k8s-worker-01", "value": random.uniform(30.0, 80.0)})
    metrics.append({"metric": "gpu_mem_utilization", "parameter": "average", "entity": "k8s-worker-01", "value": random.uniform(40.0, 85.0)})
    for gpu_id in range(4):
        metrics.append({"metric": "gpu_memory", "parameter": f"gpu{gpu_id}", "entity": "k8s-worker-01", "value": random.uniform(8e9, 14e9)})
        metrics.append({"metric": "gpu_utilization", "parameter": f"gpu{gpu_id}", "entity": "k8s-worker-01", "value": random.uniform(25.0, 85.0)})
        metrics.append({"metric": "gpu_mem_utilization", "parameter": f"gpu{gpu_id}", "entity": "k8s-worker-01", "value": random.uniform(35.0, 90.0)})
    return metrics


def main():
    """Output metrics as JSON (use --initialize for definitions, otherwise sample values)."""
    print(json.dumps(initialize() if "--initialize" in sys.argv else sample()))


if __name__ == "__main__":
    main()