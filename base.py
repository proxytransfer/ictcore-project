from abc import abstractmethod
from typing import List
from core.interfaces import Detector
from core.models import MarketEvent, SemanticEvent

class BaseDetector(Detector):
    concept: str = ""

    @abstractmethod
    def required_concepts(self) -> List[str]: ...

    @abstractmethod
    async def detect(self, events: List[MarketEvent]) -> List[SemanticEvent]: ...
