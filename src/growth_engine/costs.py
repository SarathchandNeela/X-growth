from __future__ import annotations

from dataclasses import dataclass
from enum import Enum


class BillingUnit(str, Enum):
    API_CALL = "api_call"
    POST_PUBLISH = "post_publish"


@dataclass(slots=True)
class PriceCard:
    discovery_call_usd: float
    publish_call_usd: float
    insight_call_usd: float


@dataclass(slots=True)
class UsageEvent:
    platform: str
    unit: BillingUnit
    quantity: int = 1


@dataclass(slots=True)
class CostSnapshot:
    monthly_limit_usd: float
    month_to_date_spend_usd: float

    @property
    def remaining_usd(self) -> float:
        return max(0.0, self.monthly_limit_usd - self.month_to_date_spend_usd)

    @property
    def exhausted(self) -> bool:
        return self.remaining_usd <= 0


DEFAULT_PRICE_CARDS: dict[str, PriceCard] = {
    "x": PriceCard(discovery_call_usd=0.002, publish_call_usd=0.004, insight_call_usd=0.002),
    "facebook": PriceCard(discovery_call_usd=0.0015, publish_call_usd=0.003, insight_call_usd=0.0015),
    "instagram": PriceCard(discovery_call_usd=0.0015, publish_call_usd=0.003, insight_call_usd=0.0015),
}


class CostManager:
    def __init__(self, monthly_limit_usd: float, warning_threshold: float = 0.8):
        self.monthly_limit_usd = monthly_limit_usd
        self.warning_threshold = warning_threshold
        self.month_to_date_spend_usd = 0.0

    def estimate_event_cost(self, event: UsageEvent) -> float:
        card = DEFAULT_PRICE_CARDS[event.platform]
        if event.unit == BillingUnit.API_CALL:
            # weighted average of read operations
            return event.quantity * ((card.discovery_call_usd + card.insight_call_usd) / 2)
        return event.quantity * card.publish_call_usd

    def record_event(self, event: UsageEvent) -> float:
        cost = self.estimate_event_cost(event)
        self.month_to_date_spend_usd += cost
        return cost

    def snapshot(self) -> CostSnapshot:
        return CostSnapshot(self.monthly_limit_usd, self.month_to_date_spend_usd)

    def should_throttle(self) -> bool:
        return self.month_to_date_spend_usd >= self.monthly_limit_usd * self.warning_threshold

    def can_execute(self, projected_event: UsageEvent) -> bool:
        return (self.month_to_date_spend_usd + self.estimate_event_cost(projected_event)) <= self.monthly_limit_usd
