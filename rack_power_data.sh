#!/usr/bin/env bash
set -euo pipefail

SCRIPT_PATH="/root/collect_rack_power.py"
COLLECTION_NAME="rack_power_collector"

echo "Writing ${SCRIPT_PATH}..."

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
            value = random.uniform(100.0, 900.0)
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

echo "Configuring BCM monitoring via cmsh..."

cmsh <<CMDS
monitoring
standalone
foreach s in rack_1 rack_2 rack_3 do
  ifnotexists \$s then
    add \$s
    set type Rack
    commit
  endif
end

setup
ifnotexists ${COLLECTION_NAME} then
  add collection ${COLLECTION_NAME}
endif

use ${COLLECTION_NAME}
set script ${SCRIPT_PATH}
set format JSON
set interval 30s

nodeexecutionfilters
active
commit
exit

commit
exit
CMDS

echo "Testing script..."
"${SCRIPT_PATH}" --initialize
"${SCRIPT_PATH}"

echo "Done. BCM will start collecting rack_1–rack_3 power metrics."
