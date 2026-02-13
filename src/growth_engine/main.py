from .config import load_config
from .connectors import API_INTEGRATION_GUIDE, MockConnector
from .engine import ANALYTICS_DECISION_RULES, CORE_LOGIC_PSEUDOCODE, SAFETY_RULES, GrowthEngine
from .models import Platform
from .pipeline import GrowthPipeline


def build_engine() -> GrowthEngine:
    connectors = [MockConnector(Platform.X), MockConnector(Platform.FACEBOOK), MockConnector(Platform.INSTAGRAM)]
    return GrowthEngine(connectors)


def print_blueprint() -> None:
    config = load_config()
    engine = build_engine()
    pipeline = GrowthPipeline(engine=engine, config=config)

    print("=== Runtime Mode ===")
    print("- live_api_credentials_configured:", config.has_live_api_credentials)
    print("- monthly_budget_usd:", config.budget.monthly_limit_usd)
    print("- budget_warning_threshold:", config.budget.warning_threshold)

    print("\n=== API Integration Approach ===")
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

    hourly = pipeline.run_hourly()
    daily = pipeline.run_daily()
    print("\n=== Pipeline Dry-Run ===")
    print(f"- hourly_result: {hourly}")
    print(f"- daily_result: {daily}")


if __name__ == "__main__":
    print_blueprint()
