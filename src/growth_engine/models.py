from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum


class Platform(str, Enum):
    X = "x"
    FACEBOOK = "facebook"
    INSTAGRAM = "instagram"


class Tone(str, Enum):
    CURIOUS = "curious"
    BOLD = "bold"
    CONTROVERSIAL = "slightly_controversial"
    INSPIRATIONAL = "inspirational"
    OPINIONATED = "opinionated"


class PostFormat(str, Enum):
    SHORT = "short"
    THREAD = "thread"
    QUOTE_HOOK = "quote_hook"
    STORY = "story"
    QUESTION = "question"
    REEL_CAPTION = "reel_caption"
    CAROUSEL_HOOK = "carousel_hook"
    SAVE_WORTHY = "save_worthy"


@dataclass(slots=True)
class ViralSignal:
    platform: Platform
    source_id: str
    topic: str
    core_idea: str
    emotional_trigger: str
    hook_style: str
    post_format: PostFormat
    velocity_score: float
    collected_at: datetime = field(default_factory=datetime.utcnow)


@dataclass(slots=True)
class Draft:
    platform: Platform
    tone: Tone
    post_format: PostFormat
    topic: str
    text: str
    source_ids: list[str]
    originality_score: float


@dataclass(slots=True)
class ScheduledPost:
    platform: Platform
    publish_at: datetime
    draft: Draft


@dataclass(slots=True)
class PostMetrics:
    post_id: str
    platform: Platform
    topic: str
    post_format: PostFormat
    impressions: int
    likes: int
    shares: int
    comments: int
    follower_delta: int

    @property
    def engagement_score(self) -> float:
        base = self.impressions or 1
        weighted = self.likes + (self.shares * 2) + (self.comments * 1.2)
        conversion = self.follower_delta * 3
        return (weighted + conversion) / base
