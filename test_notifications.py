import pytest
from notifications import NotificationSystem


def test_add_and_get_notifications():
    system = NotificationSystem()
    n = system.add_notification("Test message", level="info")
    all_n = system.get_all()
    assert len(all_n) == 1
    assert all_n[0].id == n.id
    assert all_n[0].message == "Test message"
    assert not all_n[0].read


def test_unread_and_mark_as_read():
    system = NotificationSystem()
    n1 = system.add_notification("Hello 1", level="success")
    n2 = system.add_notification("Hello 2", level="warning")

    unread = system.get_unread()
    assert len(unread) == 2
    assert system.mark_as_read(n1.id).read is True
    unread_after = system.get_unread()
    assert len(unread_after) == 1
    assert unread_after[0].id == n2.id


def test_invalid_level_raises_error():
    system = NotificationSystem()
    with pytest.raises(ValueError):
        system.add_notification("bad", level="fatal")


def test_clear_removes_all():
    system = NotificationSystem()
    system.add_notification("x", level="info")
    system.clear()
    assert system.get_all() == []


def test_subscribe_callback():
    system = NotificationSystem()
    calls = []

    def cb(notification):
        calls.append(notification.id)

    system.subscribe(cb)
    n = system.add_notification("test event", level="info")
    assert calls == [n.id]
