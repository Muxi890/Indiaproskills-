from __future__ import annotations

import threading
import uuid
from dataclasses import dataclass, field
from datetime import datetime, timedelta
from typing import Dict, List, Optional


@dataclass
class WalletAccount:
    user_id: str
    balance: float = 0.0
    currency: str = "USD"


class WalletService:
    """In-memory wallet service for account balances, transfers, and charges."""

    def __init__(self):
        self._lock = threading.Lock()
        self._accounts: Dict[str, WalletAccount] = {}

    def create_account(self, user_id: str, initial_balance: float = 0.0, currency: str = "USD") -> WalletAccount:
        if initial_balance < 0:
            raise ValueError("initial_balance must be non-negative")

        with self._lock:
            if user_id in self._accounts:
                raise ValueError(f"Account for user_id '{user_id}' already exists")

            account = WalletAccount(user_id=user_id, balance=float(initial_balance), currency=currency)
            self._accounts[user_id] = account

        return account

    def get_account(self, user_id: str) -> Optional[WalletAccount]:
        with self._lock:
            return self._accounts.get(user_id)

    def get_balance(self, user_id: str) -> float:
        account = self.get_account(user_id)
        if not account:
            raise KeyError(f"Account for user_id '{user_id}' not found")
        return account.balance

    def deposit(self, user_id: str, amount: float) -> WalletAccount:
        if amount <= 0:
            raise ValueError("Deposit amount must be positive")

        with self._lock:
            account = self._accounts.get(user_id)
            if not account:
                raise KeyError(f"Account for user_id '{user_id}' not found")
            account.balance += float(amount)
        return account

    def withdraw(self, user_id: str, amount: float) -> WalletAccount:
        if amount <= 0:
            raise ValueError("Withdrawal amount must be positive")

        with self._lock:
            account = self._accounts.get(user_id)
            if not account:
                raise KeyError(f"Account for user_id '{user_id}' not found")
            if account.balance < amount:
                raise ValueError("Insufficient balance")
            account.balance -= float(amount)
        return account

    def transfer(self, from_user_id: str, to_user_id: str, amount: float):
        if amount <= 0:
            raise ValueError("Transfer amount must be positive")

        with self._lock:
            sender = self._accounts.get(from_user_id)
            receiver = self._accounts.get(to_user_id)
            if not sender:
                raise KeyError(f"Account for from_user_id '{from_user_id}' not found")
            if not receiver:
                raise KeyError(f"Account for to_user_id '{to_user_id}' not found")
            if sender.balance < amount:
                raise ValueError("Insufficient balance")
            sender.balance -= float(amount)
            receiver.balance += float(amount)

    def clear(self):
        with self._lock:
            self._accounts.clear()


@dataclass
class SubscriptionPlan:
    name: str
    monthly_price: float
    interval_days: int = 30


@dataclass
class Subscription:
    id: str
    user_id: str
    plan_name: str
    status: str
    start_date: datetime
    current_period_end: datetime
    cancel_date: Optional[datetime] = None


class SubscriptionService:
    """In-memory subscriptions with lifecycle management."""

    def __init__(self):
        self._lock = threading.Lock()
        self._plans: Dict[str, SubscriptionPlan] = {}
        self._subscriptions: Dict[str, Subscription] = {}

    def register_plan(self, name: str, monthly_price: float, interval_days: int = 30) -> SubscriptionPlan:
        if monthly_price < 0 or interval_days <= 0:
            raise ValueError("price must be non-negative and interval_days must be positive")

        plan = SubscriptionPlan(name=name, monthly_price=float(monthly_price), interval_days=int(interval_days))
        with self._lock:
            self._plans[name] = plan
        return plan

    def get_plan(self, name: str) -> SubscriptionPlan:
        with self._lock:
            plan = self._plans.get(name)
        if not plan:
            raise KeyError(f"Subscription plan '{name}' not found")
        return plan

    def subscribe(self, user_id: str, plan_name: str, start_date: Optional[datetime] = None) -> Subscription:
        plan = self.get_plan(plan_name)
        now = start_date or datetime.utcnow()

        with self._lock:
            existing = self._subscriptions.get(user_id)
            if existing and self.is_active(user_id):
                raise ValueError("User already has an active subscription")

            sub = Subscription(
                id=str(uuid.uuid4()),
                user_id=user_id,
                plan_name=plan_name,
                status="active",
                start_date=now,
                current_period_end=now + timedelta(days=plan.interval_days),
                cancel_date=None,
            )
            self._subscriptions[user_id] = sub

        return sub

    def cancel(self, user_id: str, cancel_date: Optional[datetime] = None) -> Subscription:
        with self._lock:
            sub = self._subscriptions.get(user_id)
            if not sub:
                raise KeyError(f"No subscription found for user_id '{user_id}'")
            if sub.status != "active":
                raise ValueError("Subscription is not active")
            sub.status = "cancelled"
            sub.cancel_date = cancel_date or datetime.utcnow()
        return sub

    def is_active(self, user_id: str, at_date: Optional[datetime] = None) -> bool:
        at_date = at_date or datetime.utcnow()
        with self._lock:
            sub = self._subscriptions.get(user_id)
            if not sub:
                return False
            if sub.status == "active" and at_date < sub.current_period_end:
                return True
            if sub.status == "cancelled" and sub.cancel_date and at_date < sub.current_period_end:
                return True
            return False

    def renew(self, user_id: str, renew_date: Optional[datetime] = None) -> Subscription:
        with self._lock:
            sub = self._subscriptions.get(user_id)
            if not sub:
                raise KeyError(f"No subscription found for user_id '{user_id}'")
            if not self.is_active(user_id):
                raise ValueError("Cannot renew inactive subscription")
            plan = self.get_plan(sub.plan_name)
            now = renew_date or datetime.utcnow()
            if now < sub.current_period_end:
                raise ValueError("Can only renew at or after current period end")
            sub.current_period_end = now + timedelta(days=plan.interval_days)
            sub.status = "active"
            sub.cancel_date = None
        return sub

    def get_subscription(self, user_id: str) -> Optional[Subscription]:
        with self._lock:
            return self._subscriptions.get(user_id)

    def get_all_subscriptions(self) -> List[Subscription]:
        with self._lock:
            return list(self._subscriptions.values())

    def clear(self):
        with self._lock:
            self._subscriptions.clear()
            self._plans.clear()


class PremiumService:
    """Premium feature controller for wallet-powered subscription upgrades."""

    def __init__(self, wallet: WalletService, subscription: SubscriptionService):
        self.wallet = wallet
        self.subscription = subscription
        self._promo_codes: Dict[str, float] = {
            "PREMIUM10": 0.10,
            "PREMIUM20": 0.20,
            "WELCOME50": 0.50,
        }

    def subscribe_premium(self, user_id: str, plan_name: str = "premium", promo_code: Optional[str] = None) -> Subscription:
        plan = self.subscription.get_plan(plan_name)

        discount = 0.0
        if promo_code:
            discount = self._promo_codes.get(promo_code.upper(), 0.0)

        price = plan.monthly_price * (1.0 - discount)

        self.wallet.withdraw(user_id, price)
        return self.subscription.subscribe(user_id, plan_name)

    def cancel_premium(self, user_id: str) -> Subscription:
        return self.subscription.cancel(user_id)

    def is_premium(self, user_id: str, at_date: Optional[datetime] = None) -> bool:
        return self.subscription.is_active(user_id, at_date)

    def get_subscription(self, user_id: str) -> Optional[Subscription]:
        return self.subscription.get_subscription(user_id)

    def add_promo_code(self, code: str, discount: float):
        if discount < 0 or discount > 1:
            raise ValueError("discount must be between 0 and 1")
        self._promo_codes[code.upper()] = discount

    def clear(self):
        self._promo_codes.clear()
