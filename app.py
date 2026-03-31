"""Simple starter script for Indiaproskills- repository."""

from notifications import NotificationSystem
from earnings_dashboard import WorkerEarningsDashboard
from pricing_system import AIPricingSystem
from super_app import WalletService, SubscriptionService, PremiumService


def main():
    notifier = NotificationSystem()

    def listener(notification):
        status = "READ" if notification.read else "UNREAD"
        print(f"[EVENT] {notification.id} {notification.level.upper()} {status}: {notification.message}")

    notifier.subscribe(listener)

    print("Starting notification demo...")
    notifier.add_notification("Welcome to Indiaproskills!", level="success")
    notifier.add_notification("Your setup is complete.", level="info")
    notifier.add_notification("Low disk space", level="warning")

    unread = notifier.get_unread()
    print(f"Unread notifications: {len(unread)}")

    if unread:
        notifier.mark_as_read(unread[0].id)
        print(f"Marked as read: {unread[0].id}")

    print("All notifications:")
    for n in notifier.get_all():
        print(f" - {n.id} [{n.level}] read={n.read} {n.message}")

    print("\nWorker earnings dashboard demo:")
    dashboard = WorkerEarningsDashboard()
    dashboard.add_earning("w1", "Alice", 500.0, "Course creation")
    dashboard.add_earning("w1", "Alice", 250.0, "Consulting")
    dashboard.add_earning("w2", "Bob", 300.0, "Web development")
    dashboard.add_earning("w3", "Carol", 450.0, "Data annotation")

    print("Total by worker:")
    for worker_id, worker_name, amt in dashboard.get_all_worker_totals():
        print(f" - {worker_name} ({worker_id}): ${amt:.2f}")

    top = dashboard.get_top_earners(2)
    print("Top 2 earners:")
    for worker_id, worker_name, amt in top:
        print(f" - {worker_name} ({worker_id}): ${amt:.2f}")

    print("\nAI pricing system demo:")
    pricing = AIPricingSystem()
    pricing.add_usage("usage-1", "gpt-4.1", prompt_tokens=150, completion_tokens=100)
    pricing.add_usage("usage-2", "gpt-3.5", prompt_tokens=300, completion_tokens=200)
    pricing.add_usage("usage-3", "gpt-4.1", prompt_tokens=20, completion_tokens=30, embedding_tokens=10)

    print(f"Total AI costs: ${pricing.get_total_cost():.6f}")
    for model, cost in pricing.get_cost_by_model().items():
        print(f" - {model}: ${cost:.6f}")

    print("\nSuper app wallet/subscription/premium demo:")
    wallet = WalletService()
    wallet.create_account("user1", initial_balance=120.0)
    wallet.create_account("user2", initial_balance=15.0)

    print(f"user1 balance: ${wallet.get_balance('user1'):.2f}")
    print(f"user2 balance: ${wallet.get_balance('user2'):.2f}")

    wallet.transfer("user1", "user2", 30.0)
    print(f"after transfer, user1: ${wallet.get_balance('user1'):.2f}, user2: ${wallet.get_balance('user2'):.2f}")

    subscriptions = SubscriptionService()
    subscriptions.register_plan("premium", monthly_price=50.0)
    premium = PremiumService(wallet, subscriptions)

    premium.subscribe_premium("user1", "premium", promo_code="PREMIUM10")
    print(f"user1 premium active: {premium.is_premium('user1')}")
    print(f"user1 balance after premium subscription: ${wallet.get_balance('user1'):.2f}")

    premium.cancel_premium("user1")
    print(f"user1 premium status after cancel: {premium.is_premium('user1')}")


if __name__ == "__main__":
    main()
