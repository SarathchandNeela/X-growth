from growth_engine.costs import BillingUnit, CostManager, UsageEvent


def test_cost_manager_records_spend_and_threshold():
    mgr = CostManager(monthly_limit_usd=1.0, warning_threshold=0.5)
    mgr.record_event(UsageEvent(platform="x", unit=BillingUnit.API_CALL, quantity=400))
    assert mgr.month_to_date_spend_usd > 0
    assert mgr.should_throttle()


def test_cost_manager_rejects_over_budget_projected_event():
    mgr = CostManager(monthly_limit_usd=0.01, warning_threshold=0.9)
    can_execute = mgr.can_execute(UsageEvent(platform="x", unit=BillingUnit.POST_PUBLISH, quantity=10))
    assert not can_execute
