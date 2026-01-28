#!/usr/bin/env python3
import sys
import json
import random

RACKS = ["A05", "A06", "A07"]
K8S_NODES = ["k8s-worker-01", "k8s-control-plane-01", "k8s-control-plane-02", "k8s-control-plane-03"]

def initialize():
    metrics = []
    for rack in RACKS:
        metrics.append({"metric": "totalnodepowerusage", "entity": rack, "unit": "W", "class": "Power/Rack"})
        metrics.append({"metric": "TotalGPUTemperature", "entity": rack, "unit": "C", "class": "Temperature/Rack"})
    for node in K8S_NODES:
        metrics.append({"metric": "gpu_temperature", "parameter": "average", "entity": node, "unit": "C", "class": "GPU"})
    return metrics

def sample():
    metrics = []
    power_ranges = {"A05": (130000.0, 135000.0), "A06": (60000.0, 65000.0), "A07": (55000.0, 60000.0)}
    temp_ranges = {"A05": (75.0, 85.0), "A06": (55.0, 65.0), "A07": (50.0, 60.0)}
    for rack in RACKS:
        pmin, pmax = power_ranges.get(rack, (50000.0, 60000.0))
        tmin, tmax = temp_ranges.get(rack, (50.0, 65.0))
        metrics.append({"metric": "totalnodepowerusage", "entity": rack, "value": random.uniform(pmin, pmax)})
        metrics.append({"metric": "TotalGPUTemperature", "entity": rack, "value": random.uniform(tmin, tmax)})
    for node in K8S_NODES:
        metrics.append({"metric": "gpu_temperature", "parameter": "average", "entity": node, "value": random.uniform(50.0, 70.0)})
    return metrics

def main():
    if "--initialize" in sys.argv:
        print(json.dumps(initialize()))
    else:
        print(json.dumps(sample()))

if __name__ == "__main__":
    main()