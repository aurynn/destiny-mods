from schema import Schema, And, Or, Optional, Use
import copy

STATS = ["mobility", "recovery", "resilience", "discipline", "intellect", "strength"]
ABILITIES = ["grenade", "melee", "class", "super"]
ON_EVENTS = [
  'kill',
  'grenade',
  'super',
  'melee',
  'pickup',
  'cwl',
  'damage',
  "shield break",
  "assist",
  "reload",
  "ready",
  # "weapon", # using a weapon?
  "finisher", # using your finisher
  "revive", # reviving an ally
  "fire" # firing your weapon
]
CREATES = [
  "cwl",
  "healing",
  "grenade",
  "damage",
  "orb",
  "melee",
  "stacks",
  "special ammo",
  "super",
  "heavy ammo"
]

TARGETS = ["self", "allies", "enemy"]

FROM_SOURCES = ["orb", "super", "cwl", "grenade", "weapon", "melee", "stacks"]

ELEMENTS = ["void", "solar", "arc", "stasis", "kinetic"]

BUFF_TYPES = ["damage", "reload speed", "stats", "resistance"]

CONSTRAINT_MATCHES = ["weapon", "enemy", "ability", "element"]

_constraint = {
  # what, if anything, we're matching
  "match": Or(*CONSTRAINT_MATCHES),
  # what types of things we're matching
  Optional("types"): Or(str, [str])
}

_constraints = Schema(
  Or(
    _constraint,
    [_constraint]
  )
)

_from_dict = Schema(
  {
    "source": Or(*FROM_SOURCES),
    Optional("element"): Or(*ELEMENTS),
    Optional("amount"): Or(str, int),
    Optional("constraint"): _constraints
  }
)

_from = Schema(
  Or(
    # either one of the from_source strings
    Or(*FROM_SOURCES),
    # or a single dict
    _from_dict,
    # or a list of dicts
    [_from_dict]
  )
)

_generic_buff = Schema({
  "type": Or(*BUFF_TYPES),
  Optional("until"): str,
  Optional("duration"): Or(str, int)
})

_stat_buff = Schema({
  "type": "stats",
  "stats": {
    Optional("mobility"): int,
    Optional("recovery"): int,
    Optional("resilience"): int,
    Optional("discipline"): int,
    Optional("intellect"): int,
    Optional("strength"): int,
  },
})

_damage_buff = Schema({
  "type": "damage",
  Optional("duration"): int,
  Optional("constraint"): _constraints,
  Optional("until"): str
})

_buff = Schema(
  Or(
    # either a single buff object, or a list of buff objects
    Or(_stat_buff, _damage_buff, _generic_buff),
    [_stat_buff, _damage_buff, _generic_buff]
  )
)



_on_effect = Schema(
  {
    "event": Or(*ON_EVENTS), # what triggers the effect
    Optional("from"): _from, # the source of the effect
    Optional("target"): Or(*TARGETS), # what the effect targets
    Optional("element"): str, # is an element involved?
    Optional("random"): bool,
    Optional("cumulative"): bool,
    Optional("constraint"): _constraints,
    Optional("buffs"): _buff
  }
)

_creates_damage = Schema({
  "type": "damage",
  "damage": {
    Optional("range"): str,
    Optional("element"): Or(*ELEMENTS)
  },
  Optional("constraint"): _constraints
})

_create_ability = Schema({
  "type": Or(*ABILITIES),
  Optional("amount"): int,
  Optional("max"): int

})

_creates = Schema(
  Or(
    *CREATES,
    _creates_damage,
    _create_ability
  )
)


_base_mod = {
  "name": str, # mods must have a name
  # Mods must be >= 1
  # and less than 10
  "cost": And(int, lambda i: i > 0, lambda i: i <= 10), # mods must have a cost
  Optional("stacks"): bool # should default to false
}
