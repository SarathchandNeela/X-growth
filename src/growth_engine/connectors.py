from __future__ import annotations

from abc import ABC, abstractmethod
from datetime import datetime

from .models import Platform, PostMetrics, ScheduledPost, ViralSignal


class PlatformConnector(ABC):
    platform: Platform

    @abstractmethod
    def fetch_trending_signals(self) -> list[ViralSignal]:
        raise NotImplementedError

    @abstractmethod
    def schedule_post(self, post: ScheduledPost) -> str:
        raise NotImplementedError

    @abstractmethod
    def collect_metrics(self, since: datetime) -> list[PostMetrics]:
        raise NotImplementedError


class MockConnector(PlatformConnector):
    def __init__(self, platform: Platform):
        self.platform = platform

    def fetch_trending_signals(self) -> list[ViralSignal]:
        return []

    def schedule_post(self, post: ScheduledPost) -> str:
        return f"{self.platform.value}-{int(post.publish_at.timestamp())}"

    def collect_metrics(self, since: datetime) -> list[PostMetrics]:
        return []


API_INTEGRATION_GUIDE = {
    "x": {
        "endpoint_examples": ["/2/tweets/search/recent", "/2/users/:id/tweets"],
        "notes": "Use official X API; store per-app and per-user limits; respect automation rules.",
    },
    "facebook": {
        "endpoint_examples": ["/{page-id}/feed", "/{post-id}/insights"],
        "notes": "Use Meta Graph API with Page access tokens and app review-compliant scopes.",
    },
    "instagram": {
        "endpoint_examples": ["/{ig-user-id}/media", "/{ig-media-id}/insights"],
        "notes": "Use Instagram Graph API for Business/Creator accounts only.",
    },
}
