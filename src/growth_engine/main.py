from .connectors import API_INTEGRATION_GUIDE, MockConnector
from .engine import ANALYTICS_DECISION_RULES, CORE_LOGIC_PSEUDOCODE, SAFETY_RULES, GrowthEngine
from .models import Platform


def build_engine() -> GrowthEngine:
    connectors = [MockConnector(Platform.X), MockConnector(Platform.FACEBOOK), MockConnector(Platform.INSTAGRAM)]
    return GrowthEngine(connectors)


def print_blueprint() -> None:
    print("=== API Integration Approach ===")
    for platform, info in API_INTEGRATION_GUIDE.items():
        print(f"- {platform}: {info}")
    print("\n=== Core Logic Pseudocode ===")
    print(CORE_LOGIC_PSEUDOCODE)
    print("\n=== Analytics Decision Rules ===")
    for rule in ANALYTICS_DECISION_RULES:
        print(f"- {rule}")
    print("\n=== Safety & Anti-Ban Rules ===")
    for rule in SAFETY_RULES:
        print(f"- {rule}")


if __name__ == "__main__":
    print_blueprint()
