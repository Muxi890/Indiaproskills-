import pytest

from pricing_system import AIPricingSystem


def test_register_and_estimate_cost():
    pricing = AIPricingSystem()
    pricing.register_model("custom-ai", prompt_price=0.001, completion_price=0.002, embedding_price=0.0005)

    cost = pricing.estimate_cost("custom-ai", prompt_tokens=100, completion_tokens=200, embedding_tokens=50, request_units=10)
    assert cost == pytest.approx(100 * 0.001 + 200 * 0.002 + 50 * 0.0005 + 10 * 0.0005, rel=1e-9)


def test_add_usage_and_total_cost():
    pricing = AIPricingSystem()
    pricing.add_usage("u1", "gpt-3.5", 100, 100)
    pricing.add_usage("u2", "gpt-3.5", 50, 50)

    assert pricing.get_total_cost() == pytest.approx(pricing.get_total_cost("gpt-3.5"))
    assert pricing.get_total_cost() > 0


def test_get_usage_filters_by_model():
    pricing = AIPricingSystem()
    pricing.add_usage("u1", "gpt-4.1", 10, 10)
    pricing.add_usage("u2", "gpt-3.5", 10, 10)

    all_usage = pricing.get_usage()
    assert len(all_usage) == 2

    gpt35_usage = pricing.get_usage("gpt-3.5")
    assert len(gpt35_usage) == 1
    assert gpt35_usage[0].model == "gpt-3.5"


def test_get_cost_by_model():
    pricing = AIPricingSystem()
    pricing.add_usage("u1", "gpt-4.1", 100, 0)
    pricing.add_usage("u2", "gpt-4.1", 0, 100)
    pricing.add_usage("u3", "gpt-3.5", 200, 0)

    costs = pricing.get_cost_by_model()
    assert "gpt-4.1" in costs and "gpt-3.5" in costs
    assert costs["gpt-4.1"] > costs["gpt-3.5"]


def test_invalid_pricing_raises_error():
    pricing = AIPricingSystem()
    with pytest.raises(ValueError):
        pricing.register_model("bad", prompt_price=-0.1, completion_price=0.1)

    with pytest.raises(ValueError):
        pricing.estimate_cost("gpt-3.5", -1, 0)

    with pytest.raises(KeyError):
        pricing.estimate_cost("unregistered", 1, 1)
