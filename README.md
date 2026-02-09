# AI Growth Engine for X, Facebook, and Instagram

A production-ready blueprint and Python implementation for a **self-improving social growth system** that discovers viral patterns, rewrites content originally, schedules safely, tracks outcomes, and adapts strategy daily.

## Application architecture

```text
┌──────────────────────────────────────────────────────────────────┐
│                         Growth Engine Orchestrator              │
└───────────────┬─────────────────────┬───────────────────────────┘
                │                     │
        ┌───────▼────────┐    ┌──────▼─────────┐
        │ Discovery Layer │    │ Rewrite Layer   │
        │ - trend ingest  │    │ - prompt engine │
        │ - velocity rank │    │ - originality   │
        └───────┬────────┘    └──────┬─────────┘
                │                     │
        ┌───────▼─────────────────────▼─────────┐
        │ Scheduling & Safety Layer             │
        │ - randomized timing                   │
        │ - cadence/rate limit control          │
        │ - anti-ban guardrails                 │
        └───────┬───────────────────────────────┘
                │
        ┌───────▼─────────┐
        │ Platform APIs   │
        │ X / FB / IG     │
        └───────┬─────────┘
                │
        ┌───────▼────────────────────────────────┐
        │ Analytics + Strategy Adaptation         │
        │ - per-post metrics                      │
        │ - engagement/follower conversion score  │
        │ - daily winner/loser pattern updates    │
        └──────────────────────────────────────────┘
```

## API integration approach

Use official APIs only (compliance-first):

- **X API v2**: recent search, user tweets, tweet metrics.
- **Meta Graph API (Facebook + Instagram)**: page/media publishing and insights.
- Maintain token vault, request throttling, and endpoint-level retry policies.
- Normalize all inbound signals into `ViralSignal` and all outcomes into `PostMetrics`.

## Core logic pseudocode

```text
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
```

## Prompt templates for rewriting

```text
You are a senior social copywriter.
Task: transform the viral insight into an original {platform} post.

Input
- Topic: {topic}
- Core idea: {core_idea}
- Emotional trigger: {emotional_trigger}
- Hook style: {hook_style}
- Format: {post_format}
- Tone: {tone}

Rules
1) Keep the idea, do not copy source wording.
2) Use natural, conversational language with concrete details.
3) Avoid repetitive patterns and obvious AI phrasing.
4) Include one clear hook in the first line.
5) Keep it platform-native.
6) Do not make unverifiable claims.
7) Return only the final post text.
```

Tones supported: curious, bold, slightly controversial, inspirational, opinionated.

## Analytics decision rules

- Scale formats with engagement score above the 75th percentile and positive follower growth.
- Pause formats below the 25th percentile for 3-day rolling windows.
- Reduce frequency 20% when conversion drops for 2 consecutive days.
- Reserve 20% of slots for exploratory tests (new hooks, new format mix).
- Prioritize topic/format pairs with best follower conversion per impression.

## Safety & anti-ban rules

- Respect platform terms and approved automation use-cases.
- Enforce platform-specific rate limits, jitter, and cooldown windows.
- Require semantic variation checks before enqueueing posts.
- Pause automation on anomaly events (high unfollow spikes, moderation flags, API warnings).
- Add optional human review gate for sensitive or high-risk claims.
- Never use mass-tagging or unsolicited DM spam tactics.

## Project structure

- `src/growth_engine/models.py`: core domain models and scoring.
- `src/growth_engine/connectors.py`: connector interface + API mapping.
- `src/growth_engine/engine.py`: discovery, rewrite, scheduling, adaptation logic.
- `src/growth_engine/prompts.py`: reusable prompt templates.
- `src/growth_engine/main.py`: runnable blueprint output.

## Run

```bash
python -m growth_engine.main
```
