import threading
import time
import uuid
from dataclasses import dataclass, field
from typing import Callable, Dict, List, Optional


@dataclass
class Notification:
    id: str
    message: str
    level: str = "info"  # info, warning, error, success
    created_at: float = field(default_factory=time.time)
    read: bool = False


class NotificationSystem:
    """In-memory notification system with callback updates."""

    def __init__(self):
        self._lock = threading.Lock()
        self.notifications: Dict[str, Notification] = {}
        self._subscribers: List[Callable[[Notification], None]] = []

    def add_notification(self, message: str, level: str = "info") -> Notification:
        if level not in {"info", "warning", "error", "success"}:
            raise ValueError("level must be one of info, warning, error, success")

        n = Notification(id=str(uuid.uuid4()), message=message, level=level)
        with self._lock:
            self.notifications[n.id] = n

        self._notify_subscribers(n)
        return n

    def _notify_subscribers(self, notification: Notification):
        for callback in list(self._subscribers):
            try:
                callback(notification)
            except Exception:
                continue

    def subscribe(self, callback: Callable[[Notification], None]):
        with self._lock:
            self._subscribers.append(callback)

    def unsubscribe(self, callback: Callable[[Notification], None]):
        with self._lock:
            self._subscribers = [s for s in self._subscribers if s != callback]

    def get_all(self) -> List[Notification]:
        with self._lock:
            return list(self.notifications.values())

    def get_unread(self) -> List[Notification]:
        with self._lock:
            return [n for n in self.notifications.values() if not n.read]

    def mark_as_read(self, notification_id: str) -> Optional[Notification]:
        with self._lock:
            n = self.notifications.get(notification_id)
            if n is None:
                return None
            n.read = True
            return n

    def clear(self):
        with self._lock:
            self.notifications.clear()
