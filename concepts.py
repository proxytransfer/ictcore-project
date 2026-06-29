from dataclasses import dataclass, field
from typing import List

@dataclass
class Concept:
    name: str
    description: str
    requires: List[str] = field(default_factory=list)
    produces: List[str] = field(default_factory=list)
    parameters: dict = field(default_factory=dict)
    invalidation_rules: List[str] = field(default_factory=list)

CONCEPTS = {
    "Displacement": Concept("Displacement", "Movimento direcional forte"),
    "FVG": Concept("FVG", "Fair Value Gap", requires=["Displacement"], produces=["EntryZone"]),
    "MSS": Concept("MSS", "Market Structure Shift", requires=["Sweep"], produces=["FVG"]),
    "Sweep": Concept("Sweep", "Liquidity Sweep", produces=["MSS"]),
    "SMT": Concept("SMT", "Smart Money Technique", requires=["Divergence"]),
    # Adicione outros conceitos conforme a ontologia completa
}
