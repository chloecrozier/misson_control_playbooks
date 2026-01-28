# Synthetic Data Producer for BCM Monitoring

Ansible playbook to deploy synthetic monitoring metrics for Bright Cluster Manager. Generates data for 3 racks (A05/A06/A07), 4 K8S nodes with GPU metrics, and 4 infrastructure nodes. Deploy with: `ansible-playbook -i inventory.ini deploy-synthetic-data-producer.yaml`
