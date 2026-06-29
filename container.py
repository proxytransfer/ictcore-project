from typing import Dict, Type
from .interfaces import BaseProvider, EventBus, Detector, InferenceEngine, MotorICT

class Container:
    def __init__(self):
        self._provider: BaseProvider = None
        self._event_bus: EventBus = None
        self._detectors: Dict[str, Detector] = {}
        self._inference_engine: InferenceEngine = None

    def set_provider(self, provider: BaseProvider):
        self._provider = provider

    def provider(self) -> BaseProvider:
        if not self._provider:
            from ingestion.providers.yahoo import YahooProvider
            self._provider = YahooProvider()
        return self._provider

    def set_event_bus(self, bus: EventBus):
        self._event_bus = bus

    def event_bus(self) -> EventBus:
        if not self._event_bus:
            from eventbus.inmemory import InMemoryEventBus
            self._event_bus = InMemoryEventBus()
        return self._event_bus

    def register_detector(self, name: str, detector: Detector):
        self._detectors[name] = detector

    def get_detector(self, name: str) -> Detector:
        return self._detectors.get(name)

    def all_detectors(self) -> Dict[str, Detector]:
        return self._detectors

    def set_inference_engine(self, engine: InferenceEngine):
        self._inference_engine = engine

    def inference_engine(self) -> InferenceEngine:
        if not self._inference_engine:
            from inference.engine import ForwardChainingEngine
            self._inference_engine = ForwardChainingEngine([])
        return self._inference_engine
