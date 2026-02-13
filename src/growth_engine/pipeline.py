from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, timedelta, timezone

from .config import EngineConfig
from .costs import BillingUnit, CostManager, UsageEvent
from .engine import GrowthEngine
from .models import Draft, PostMetrics


@dataclass(slots=True)
class HourlyRunResult:
    discovered: int
    drafted: int
    scheduled: int
    published: int
    budget_spend_usd: float
    throttled: bool


@dataclass(slots=True)
class DailyRunResult:
    metrics_count: int
    strategy_summary: dict[str, str]
    spend_remaining_usd: float


class GrowthPipeline:
    def __init__(self, engine: GrowthEngine, config: EngineConfig):
        self.engine = engine
        self.config = config
        self.costs = CostManager(
            monthly_limit_usd=config.budget.monthly_limit_usd,
            warning_threshold=config.budget.warning_threshold,
        )

    def run_hourly(self) -> HourlyRunResult:
        if self.costs.should_throttle():
            return HourlyRunResult(0, 0, 0, 0, 0.0, throttled=True)

        signals = self.engine.discover()
        spend = 0.0
        drafts: list[Draft] = []

        for signal in signals[:12]:
            projected = UsageEvent(platform=signal.platform.value, unit=BillingUnit.API_CALL, quantity=1)
            if not self.costs.can_execute(projected):
                break
            spend += self.costs.record_event(projected)
            drafts.append(self.engine.rewrite(signal, self.engine.state.preferred_tones[signal.platform]))

        schedule = self.engine.build_schedule(drafts, start_at=datetime.now(timezone.utc) + timedelta(minutes=5))

        published_ids: list[str] = []
        for item in schedule:
            projected = UsageEvent(platform=item.platform.value, unit=BillingUnit.POST_PUBLISH, quantity=1)
            if not self.costs.can_execute(projected):
                break
            spend += self.costs.record_event(projected)
            published_ids.extend(self.engine.publish([item]))

        return HourlyRunResult(
            discovered=len(signals),
            drafted=len(drafts),
            scheduled=len(schedule),
            published=len(published_ids),
            budget_spend_usd=round(spend, 4),
            throttled=False,
        )

    def run_daily(self) -> DailyRunResult:
        since = datetime.now(timezone.utc) - timedelta(hours=24)
        all_metrics: list[PostMetrics] = []
        for connector in self.engine.connectors.values():
            all_metrics.extend(connector.collect_metrics(since))

        summary = self.engine.adapt_strategy(all_metrics)
        snapshot = self.costs.snapshot()

        return DailyRunResult(
            metrics_count=len(all_metrics),
            strategy_summary=summary,
            spend_remaining_usd=round(snapshot.remaining_usd, 2),
        )
