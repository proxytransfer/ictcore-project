from transitions import Machine
from enum import Enum
from core.models import SemanticEvent

class MarketState(Enum):
    ACCUMULATION = 1
    SWEEP = 2
    REPRICING = 3
    DELIVERY = 4
    MITIGATION = 5
    REVERSAL = 6

class NarrativeFSM:
    states = list(MarketState)

    def __init__(self):
        self.machine = Machine(model=self, states=MarketState, initial=MarketState.ACCUMULATION)
        self.machine.add_transition('on_sweep', MarketState.ACCUMULATION, MarketState.SWEEP)
        self.machine.add_transition('on_mss', MarketState.SWEEP, MarketState.REPRICING)
        self.machine.add_transition('on_fvg', MarketState.REPRICING, MarketState.DELIVERY)
        # Adicione outras transições conforme necessário

    def process_semantic_event(self, event: SemanticEvent):
        concept = event.concept
        if concept == "Sweep" and self.state == MarketState.ACCUMULATION:
            self.on_sweep()
        elif concept == "MSS" and self.state == MarketState.SWEEP:
            self.on_mss()
        # Demais transições...
