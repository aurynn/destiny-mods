from schema import Schema, And, Or, Optional, Use
import copy
from .base import base_mod, TARGETS, ON_EVENTS, _on_effect, _buff, _constraints, _from, _creates

_cwl = {
  Optional("from"): _from, # consumed when the event triggers, if any
  Optional("on"): Or( # not _really_ optional but High Energy Fire doesn't have an `on` so ... ?
    Or(*ON_EVENTS),
    _on_effect,
    [_on_effect]
  ),
  Optional("target"): Or(*TARGETS), # what the effect targets
  Optional("stacks"): bool, # can I have > 1 of this mod
  Optional("buffs"): _buff, # does this create a buff?
  Optional("constraint"): _constraints,

}
cwl_creates = copy.copy(base_mod)
cwl_creates.update(_cwl)
cwl_uses = copy.copy(cwl_creates)

cwl_creates.update({
  "creates": _creates,
  "target": Or(*TARGETS),
})

cwl_uses.update({
  Optional("creates"): _creates
})

cwl_creates = Schema(cwl_creates)
cwl_uses = Schema(cwl_uses)
