from datetime import datetime

from growth_engine.config import BudgetConfig, EngineConfig, PlatformCredentials
from growth_engine.connectors import PlatformConnector
from growth_engine.engine import GrowthEngine
from growth_engine.models import Platform, PostFormat, PostMetrics, ScheduledPost, ViralSignal
from growth_engine.pipeline import GrowthPipeline


class DemoConnector(PlatformConnector):
    def __init__(self, platform: Platform):
        self.platform = platform

    def fetch_trending_signals(self) -> list[ViralSignal]:
        return [
            ViralSignal(
                platform=self.platform,
                source_id="abc",
                topic="consistency",
                core_idea="consistency beats intensity",
                emotional_trigger="confidence",
                hook_style="direct",
                post_format=PostFormat.SHORT,
                velocity_score=7.2,
            )
        ]

    def schedule_post(self, post: ScheduledPost) -> str:
        return f"{self.platform.value}-ok"

    def collect_metrics(self, since: datetime) -> list[PostMetrics]:
        return [PostMetrics("1", self.platform, "consistency", PostFormat.SHORT, 500, 80, 20, 10, 12)]


def _config() -> EngineConfig:
    creds = PlatformCredentials("", "", "")
    return EngineConfig(
        x=creds,
        facebook=creds,
        instagram=creds,
        budget=BudgetConfig(monthly_limit_usd=10.0, warning_threshold=0.9),
    )


def test_pipeline_hourly_and_daily_runs():
    connectors = [DemoConnector(Platform.X), DemoConnector(Platform.FACEBOOK), DemoConnector(Platform.INSTAGRAM)]
    engine = GrowthEngine(connectors)
    pipeline = GrowthPipeline(engine, _config())

    hourly = pipeline.run_hourly()
    daily = pipeline.run_daily()

    assert hourly.discovered == 3
    assert hourly.published >= 1
    assert not hourly.throttled
    assert daily.metrics_count == 3
    assert isinstance(daily.strategy_summary, dict)
