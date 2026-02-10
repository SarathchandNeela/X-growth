from __future__ import annotations

from dataclasses import dataclass
import os


@dataclass(slots=True)
class PlatformCredentials:
    app_id: str
    app_secret: str
    access_token: str

    @property
    def configured(self) -> bool:
        return all([self.app_id, self.app_secret, self.access_token])


@dataclass(slots=True)
class BudgetConfig:
    monthly_limit_usd: float = 250.0
    warning_threshold: float = 0.8


@dataclass(slots=True)
class EngineConfig:
    x: PlatformCredentials
    facebook: PlatformCredentials
    instagram: PlatformCredentials
    budget: BudgetConfig

    @property
    def has_live_api_credentials(self) -> bool:
        return any([self.x.configured, self.facebook.configured, self.instagram.configured])



def _platform(prefix: str) -> PlatformCredentials:
    return PlatformCredentials(
        app_id=os.getenv(f"{prefix}_APP_ID", ""),
        app_secret=os.getenv(f"{prefix}_APP_SECRET", ""),
        access_token=os.getenv(f"{prefix}_ACCESS_TOKEN", ""),
    )



def load_config() -> EngineConfig:
    return EngineConfig(
        x=_platform("X"),
        facebook=_platform("FACEBOOK"),
        instagram=_platform("INSTAGRAM"),
        budget=BudgetConfig(
            monthly_limit_usd=float(os.getenv("MONTHLY_BUDGET_USD", "250")),
            warning_threshold=float(os.getenv("BUDGET_WARNING_THRESHOLD", "0.8")),
        ),
    )
