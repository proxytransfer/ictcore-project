import asyncio
from core.container import Container
from detectors.motor_adapter import MotorDetectorAdapter
from motores import (
    SwingEngine, PivotEngine, StructureEngine, DisplacementEngine,
    LiquidityEngine, FVGEngine, IFVGEngine, OrderBlockEngine,
    BreakerEngine, MitigationEngine, PDArrayEngine, SMTEngine,
    CISDEngine, QuarterlyEngine, PO3Engine, KillZoneEngine,
    SessionEngine, DrawEngine, BiasEngine, NarrativeEngine,
    ExecutionEngine, TargetEngine, RiskEngine, ValidationEngine
)

async def main():
    container = Container()

    # Registra todos os motores como detectores
    container.register_detector("Swing", MotorDetectorAdapter(SwingEngine()))
    container.register_detector("Pivot", MotorDetectorAdapter(PivotEngine()))
    container.register_detector("Structure", MotorDetectorAdapter(StructureEngine()))
    container.register_detector("Displacement", MotorDetectorAdapter(DisplacementEngine()))
    container.register_detector("Liquidity", MotorDetectorAdapter(LiquidityEngine()))
    container.register_detector("FVG", MotorDetectorAdapter(FVGEngine()))
    container.register_detector("IFVG", MotorDetectorAdapter(IFVGEngine()))
    container.register_detector("OrderBlock", MotorDetectorAdapter(OrderBlockEngine()))
    container.register_detector("Breaker", MotorDetectorAdapter(BreakerEngine()))
    container.register_detector("Mitigation", MotorDetectorAdapter(MitigationEngine()))
    container.register_detector("PDArray", MotorDetectorAdapter(PDArrayEngine()))
    container.register_detector("SMT", MotorDetectorAdapter(SMTEngine()))
    container.register_detector("CISD", MotorDetectorAdapter(CISDEngine()))
    container.register_detector("Quarterly", MotorDetectorAdapter(QuarterlyEngine()))
    container.register_detector("PO3", MotorDetectorAdapter(PO3Engine()))
    container.register_detector("KillZone", MotorDetectorAdapter(KillZoneEngine()))
    container.register_detector("Session", MotorDetectorAdapter(SessionEngine()))
    container.register_detector("Draw", MotorDetectorAdapter(DrawEngine()))
    container.register_detector("Bias", MotorDetectorAdapter(BiasEngine()))
    container.register_detector("Narrative", MotorDetectorAdapter(NarrativeEngine()))
    container.register_detector("Execution", MotorDetectorAdapter(ExecutionEngine()))
    container.register_detector("Target", MotorDetectorAdapter(TargetEngine()))
    container.register_detector("Risk", MotorDetectorAdapter(RiskEngine()))
    container.register_detector("Validation", MotorDetectorAdapter(ValidationEngine()))

    # Inicializa provider e event bus
    provider = container.provider()
    await provider.connect()
    bus = container.event_bus()

    # Exemplo de fluxo
    print("Sistema ICT inicializado. Todos os motores registrados.")
    # Aqui entraria o loop principal de ingestão e processamento.

if __name__ == "__main__":
    asyncio.run(main())
