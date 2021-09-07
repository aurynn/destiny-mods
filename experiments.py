abilities = ["grenade", "melee", "class", "super"]
creates = ["orbs", "heavy", "special"]
stats = ["mobility", "recovery", "resilience", "discipline", "intellect", "strength"]
impacts = {
    "general": {
        "strength": "melee",
        "discipline": "grenade",
        "intellect": "super"
    },
    "warlock": {
        "recovery": "class"
    },
    "titan": {
        "resilience": "class"
    },
    "hunter": {
        "mobility": "class"
    }
}

from models.cwl import cwl_creates, cwl_uses #, cwl_creates_mod, cwl_uses_mod
from schema import SchemaError
import ruamel.yaml as yaml
import sys

with open("./data/cwl_mods.yaml") as f:
    cwl = yaml.safe_load(f.read())

for energy_type in cwl["creates"].keys():
    for mod in cwl["creates"][energy_type]:
        try:
            print(mod["name"])
            cwl_creates.validate(mod)
        except SchemaError as e:
            print(mod)
            print(e)
            sys.exit(1)

for energy_type in cwl["uses"].keys():
    for mod in cwl["uses"][energy_type]:
        try:
            print(mod["name"])
            cwl_uses.validate(mod)
        except SchemaError as e:
            print(mod)
            print(e)
            sys.exit(1)
