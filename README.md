# Indiaproskills-

## Notification system

This project now includes a simple notification system in `notifications.py`.

Usage:

- `NotificationSystem.add_notification(message, level)`
- `NotificationSystem.get_all()`
- `NotificationSystem.get_unread()`
- `NotificationSystem.mark_as_read(notification_id)`
- `NotificationSystem.clear()`
- `NotificationSystem.subscribe(callback)`

## Worker earnings dashboard

This project now includes a worker earnings dashboard in `earnings_dashboard.py`.

Usage:

- `WorkerEarningsDashboard.add_earning(worker_id, worker_name, amount, description="", timestamp=None)`
- `WorkerEarningsDashboard.get_earnings(worker_id)`
- `WorkerEarningsDashboard.get_total_earnings(worker_id)`
- `WorkerEarningsDashboard.get_all_worker_totals()`
- `WorkerEarningsDashboard.get_top_earners(limit=5)`
- `WorkerEarningsDashboard.get_monthly_totals(year, month)`
- `WorkerEarningsDashboard.clear()`

## AI pricing system

This project now includes an AI pricing system in `pricing_system.py` for tracking and estimating model usage costs.

Usage:

- `AIPricingSystem.register_model(model, prompt_price, completion_price, embedding_price=0.0)`
- `AIPricingSystem.estimate_cost(model, prompt_tokens=0, completion_tokens=0, embedding_tokens=0, request_units=0.0)`
- `AIPricingSystem.add_usage(usage_id, model, prompt_tokens, completion_tokens, embedding_tokens=0, request_units=0.0, timestamp=None)`
- `AIPricingSystem.get_usage(model=None)`
- `AIPricingSystem.get_total_cost(model=None)`
- `AIPricingSystem.get_cost_by_model()`
- `AIPricingSystem.clear()`

## Super app features (wallet, subscriptions, premium)

This project now includes a Super App module in `super_app.py` with wallet and subscription management.

Usage:

- `WalletService.create_account(user_id, initial_balance=0.0, currency="USD")`
- `WalletService.deposit(user_id, amount)`
- `WalletService.withdraw(user_id, amount)`
- `WalletService.transfer(from_user_id, to_user_id, amount)`
- `WalletService.get_balance(user_id)`
- `WalletService.clear()`

- `SubscriptionService.register_plan(name, monthly_price, interval_days=30)`
- `SubscriptionService.subscribe(user_id, plan_name, start_date=None)`
- `SubscriptionService.cancel(user_id, cancel_date=None)`
- `SubscriptionService.is_active(user_id, at_date=None)`
- `SubscriptionService.renew(user_id, renew_date=None)`
- `SubscriptionService.get_subscription(user_id)`
- `SubscriptionService.clear()`

- `PremiumService.subscribe_premium(user_id, plan_name="premium", promo_code=None)`
- `PremiumService.cancel_premium(user_id)`
- `PremiumService.is_premium(user_id, at_date=None)`
- `PremiumService.add_promo_code(code, discount)`
- `PremiumService.clear()`

Demo:

```bash
python app.py
```

Testing:

```bash
pip install pytest
pytest -q
```
