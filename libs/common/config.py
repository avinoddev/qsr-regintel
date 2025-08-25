
import os, yaml

def load_yaml(path: str):
    with open(path, 'r') as f:
        return yaml.safe_load(f)

CONFIG_DIR = os.getenv("CONFIG_DIR", "infra/config")

JURISDICTIONS = load_yaml(f"{CONFIG_DIR}/jurisdictions.yaml")
FAMILIES = load_yaml(f"{CONFIG_DIR}/families.yaml")
PRECEDENCE = load_yaml(f"{CONFIG_DIR}/precedence.yaml")
CADENCES = load_yaml(f"{CONFIG_DIR}/cadences.yaml")
