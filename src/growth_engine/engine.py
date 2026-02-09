from __future__ import annotations

from collections import defaultdict
from dataclasses import dataclass
from datetime import datetime, timedelta, timezone
from random import randint

from .connectors import PlatformConnector
from .models import Draft, Platform, PostFormat, PostMetrics, ScheduledPost, Tone, ViralSignal
from .prompts import REWRITE_PROMPT_TEMPLATE


@dataclass(slots=True)
class StrategyState:
    preferred_tones: dict[Platform, Tone]
    preferred_formats: dict[Platform, list[PostFormat]]
    daily_post_target: dict[Platform, int]


class GrowthEngine:
    def __init__(self, connectors: list[PlatformConnector]):
        self.connectors = {c.platform: c for c in connectors}
        self.state = StrategyState(
            preferred_tones={
                Platform.X: Tone.BOLD,
                Platform.FACEBOOK: Tone.INSPIRATIONAL,
                Platform.INSTAGRAM: Tone.CURIOUS,
            },
            preferred_formats={
                Platform.X: [PostFormat.SHORT, PostFormat.THREAD, PostFormat.QUOTE_HOOK],
                Platform.FACEBOOK: [PostFormat.STORY, PostFormat.QUESTION],
                Platform.INSTAGRAM: [PostFormat.REEL_CAPTION, PostFormat.CAROUSEL_HOOK, PostFormat.SAVE_WORTHY],
            },
            daily_post_target={Platform.X: 5, Platform.FACEBOOK: 3, Platform.INSTAGRAM: 3},
        )

    def discover(self) -> list[ViralSignal]:
        signals: list[ViralSignal] = []
        for connector in self.connectors.values():
            signals.extend(connector.fetch_trending_signals())
        return sorted(signals, key=lambda s: s.velocity_score, reverse=True)

    def rewrite(self, signal: ViralSignal, tone: Tone) -> Draft:
        text = REWRITE_PROMPT_TEMPLATE.format(
            platform=signal.platform.value,
            topic=signal.topic,
            core_idea=signal.core_idea,
            emotional_trigger=signal.emotional_trigger,
            hook_style=signal.hook_style,
            post_format=signal.post_format.value,
            tone=tone.value,
        )
        return Draft(
            platform=signal.platform,
            tone=tone,
            post_format=signal.post_format,
            topic=signal.topic,
            text=text,
            source_ids=[signal.source_id],
            originality_score=0.95,
        )

    def build_schedule(self, drafts: list[Draft], start_at: datetime | None = None) -> list[ScheduledPost]:
        start = start_at or datetime.now(timezone.utc)
        scheduled: list[ScheduledPost] = []
        for draft in drafts:
            jitter = randint(15, 240)
            publish_at = start + timedelta(minutes=jitter)
            scheduled.append(ScheduledPost(platform=draft.platform, publish_at=publish_at, draft=draft))
            start = publish_at + timedelta(minutes=randint(20, 180))
        return scheduled

    def publish(self, posts: list[ScheduledPost]) -> list[str]:
        ids: list[str] = []
        for post in posts:
            ids.append(self.connectors[post.platform].schedule_post(post))
        return ids

    def adapt_strategy(self, metrics: list[PostMetrics]) -> dict[str, str]:
        by_platform: dict[Platform, list[PostMetrics]] = defaultdict(list)
        for row in metrics:
            by_platform[row.platform].append(row)

        summary: dict[str, str] = {}
        for platform, rows in by_platform.items():
            rows = sorted(rows, key=lambda r: r.engagement_score, reverse=True)
            if not rows:
                continue
            winner = rows[0]
            loser = rows[-1]
            self.state.daily_post_target[platform] = max(1, min(8, self.state.daily_post_target[platform] + (1 if winner.follower_delta > 0 else -1)))
            summary[platform.value] = (
                f"prioritize {winner.post_format.value}/{winner.topic}; "
                f"deprioritize {loser.post_format.value}/{loser.topic}; "
                f"new_daily_target={self.state.daily_post_target[platform]}"
            )
        return summary


CORE_LOGIC_PSEUDOCODE = """
loop hourly:
  signals = discover_trending_content(all platforms)
  high_velocity = rank_by_engagement_velocity(signals)
  selected = diversify_topics_and_formats(high_velocity)

  drafts = []
  for signal in selected:
    tone = current_strategy.tone_for(signal.platform)
    draft = rewrite_original(signal, tone, platform_rules)
    if originality_check(draft) and safety_check(draft):
      drafts.append(draft)

  queue = build_randomized_schedule(drafts, rate_limits, cadence_rules)
  publish(queue)

loop daily:
  metrics = collect_post_metrics(last_24h)
  scores = compute_engagement_and_follower_conversion(metrics)
  winners, losers = extract_patterns(scores)
  current_strategy = update_strategy(winners, losers, exploration_budget=0.2)
""".strip()

SAFETY_RULES = [
    "Respect each platform's Terms of Service and automation policies.",
    "Enforce per-platform rate limits and cooldown windows.",
    "Use semantic variation thresholds to avoid duplicate-style posting.",
    "Block posting during anomaly spikes (sudden unfollows, hidden posts, API abuse warnings).",
    "Add human approval for high-risk posts (sensitive topics, legal/health claims).",
    "Never auto-DM or mass-tag users as a growth tactic.",
]

ANALYTICS_DECISION_RULES = [
    "Scale formats with engagement_score above 75th percentile and positive follower_delta.",
    "Pause formats with 3-day rolling engagement_score below 25th percentile.",
    "If comments/impressions ratio rises but shares fall, test stronger takeaways or save hooks.",
    "If follower conversion drops for 2 days, reduce frequency by 20% and refresh topics.",
    "Keep 20% of daily slots for exploration of new hooks and tones.",
]
