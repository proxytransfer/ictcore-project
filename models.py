from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional, List, Dict, Any

class MarketEvent(BaseModel):
    """Evento de mercado normalizado."""
    timestamp: datetime
    symbol: str
    open: float
    high: float
    low: float
    close: float
    volume: Optional[float] = None
    provider: str
    quality: float = Field(..., ge=0.0, le=1.0)
    timezone: str = "UTC"

class LayerOutput(BaseModel):
    """Saída dos motores ICT (contrato unificado)."""
    id: str
    timestamp: datetime
    layer_name: str
    semantic_type: str
    confidence: float
    valid: bool
    evidence: List[str] = Field(default_factory=list)
    payload: Dict[str, Any] = Field(default_factory=dict)

    def to_semantic_event(self, symbol: str) -> 'SemanticEvent':
        """Converte para SemanticEvent (usado no pipeline principal)."""
        return SemanticEvent(
            concept=self.semantic_type,
            symbol=symbol,
            start_time=self.timestamp,
            confidence=self.confidence,
            metadata={
                "engine": self.layer_name,
                "payload": self.payload,
                "evidence": self.evidence
            }
        )

class SemanticEvent(BaseModel):
    """Evento semântico usado pelos detectores e inferência."""
    concept: str
    symbol: str
    start_time: datetime
    end_time: Optional[datetime] = None
    confidence: float = 1.0
    metadata: Dict[str, Any] = Field(default_factory=dict)
    evidence: List[MarketEvent] = Field(default_factory=list)
    invalidated_by: List[str] = Field(default_factory=list)

class Hypothesis(BaseModel):
    """Hipótese gerada pelo motor de inferência."""
    statement: str
    confidence: float
    supporting_events: List[SemanticEvent] = Field(default_factory=list)
    contradictory_events: List[SemanticEvent] = Field(default_factory=list)
    trace: Dict[str, Any] = Field(default_factory=dict)
