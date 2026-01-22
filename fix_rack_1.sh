#!/bin/bash
set -e

SCRIPT_PATH="/root/collect_rack_power.py"

cat > "${SCRIPT_PATH}" << 'EOF'
#!/usr/bin/env python3
import sys
import json
import random

RACKS = ["rack_1", "rack_2", "rack_3"]

def initialize():
    metrics = []
    for rack in RACKS:
        metrics.append({
            "metric": "totalnodepowerusage",
            "entity": rack,
            "unit": "W",
            "class": "Power/Rack",
        })
    return metrics

def sample():
    metrics = []
    for rack in RACKS:
        if rack == "rack_1":
            # updated range: 475–500 W
            value = random.uniform(475.0, 500.0)
        elif rack == "rack_2":
            value = random.uniform(450.0, 460.0)
        else:
            value = random.uniform(475.0, 485.0)
        metrics.append({
            "metric": "totalnodepowerusage",
            "entity": rack,
            "value": value,
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
EOF

chmod +x "${SCRIPT_PATH}"
