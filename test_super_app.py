from datetime import datetime, timedelta

import pytest

from super_app import WalletService, SubscriptionService, PremiumService


def test_wallet_account_lifecycle():
    wallet = WalletService()
    wallet.create_account("u1", initial_balance=100.0)

    assert wallet.get_balance("u1") == 100.0

    wallet.deposit("u1", 50.0)
    assert wallet.get_balance("u1") == 150.0

    wallet.withdraw("u1", 30.0)
    assert wallet.get_balance("u1") == 120.0

    wallet.create_account("u2", initial_balance=20.0)
    wallet.transfer("u1", "u2", 40.0)

    assert wallet.get_balance("u1") == 80.0
    assert wallet.get_balance("u2") == 60.0


def test_wallet_insufficient_funds():
    wallet = WalletService()
    wallet.create_account("u1", initial_balance=10.0)
    with pytest.raises(ValueError):
        wallet.withdraw("u1", 20.0)


def test_subscription_lifecycle():
    subs = SubscriptionService()
    subs.register_plan("premium", monthly_price=50.0, interval_days=30)

    sub = subs.subscribe("u1", "premium", start_date=datetime.utcnow())
    assert subs.is_active("u1")

    cancelled = subs.cancel("u1")
    assert cancelled.status == "cancelled"
    assert subs.is_active("u1")

    future = sub.current_period_end + timedelta(days=1)
    assert not subs.is_active("u1", at_date=future)


def test_premium_service_upgrade_and_status():
    wallet = WalletService()
    wallet.create_account("u1", initial_balance=100.0)

    subs = SubscriptionService()
    subs.register_plan("premium", monthly_price=50.0, interval_days=30)

    premium = PremiumService(wallet, subs)
    premium.subscribe_premium("u1", "premium", promo_code="PREMIUM20")

    assert wallet.get_balance("u1") == 50.0
    assert premium.is_premium("u1")

    premium.cancel_premium("u1")
    assert premium.is_premium("u1")

    after = subs.get_subscription("u1").current_period_end + timedelta(days=1)
    assert not premium.is_premium("u1", at_date=after)


def test_premium_promocode_addition():
    wallet = WalletService()
    wallet.create_account("u2", initial_balance=100.0)

    subs = SubscriptionService()
    subs.register_plan("premium", monthly_price=40.0, interval_days=30)

    premium = PremiumService(wallet, subs)
    premium.add_promo_code("HALFOFF", 0.5)
    premium.subscribe_premium("u2", "premium", promo_code="HALFOFF")

    assert wallet.get_balance("u2") == 80.0
