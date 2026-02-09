from datetime import datetime, timezone

from growth_engine.connectors import MockConnector
from growth_engine.engine import GrowthEngine
from growth_engine.models import Platform, PostFormat, PostMetrics, Tone, ViralSignal


def build_signal() -> ViralSignal:
    return ViralSignal(
        platform=Platform.X,
        source_id="s1",
        topic="habits",
        core_idea="tiny steps compound",
        emotional_trigger="hope",
        hook_style="counterintuitive",
        post_format=PostFormat.SHORT,
        velocity_score=9.9,
    )


def test_rewrite_builds_draft():
    engine = GrowthEngine([MockConnector(Platform.X)])
    draft = engine.rewrite(build_signal(), Tone.BOLD)
    assert draft.platform == Platform.X
    assert draft.originality_score >= 0.9
    assert "Topic" in draft.text


def test_adapt_strategy_updates_targets():
    engine = GrowthEngine([MockConnector(Platform.X)])
    metrics = [
        PostMetrics("1", Platform.X, "habits", PostFormat.SHORT, 1000, 90, 20, 30, 40),
        PostMetrics("2", Platform.X, "sleep", PostFormat.THREAD, 1000, 10, 1, 2, -1),
    ]
    summary = engine.adapt_strategy(metrics)
    assert "x" in summary
    assert engine.state.daily_post_target[Platform.X] >= 1


def test_build_schedule_randomized_nonempty():
    engine = GrowthEngine([MockConnector(Platform.X)])
    draft = engine.rewrite(build_signal(), Tone.CURIOUS)
    queue = engine.build_schedule([draft], start_at=datetime.now(timezone.utc))
    assert len(queue) == 1
    assert queue[0].publish_at is not None
