from __future__ import annotations

import threading
from dataclasses import dataclass, field
from datetime import datetime
from typing import Dict, List, Optional, Tuple


@dataclass
class EarningEntry:
    worker_id: str
    worker_name: str
    amount: float
    description: str = ""
    timestamp: datetime = field(default_factory=datetime.utcnow)


class WorkerEarningsDashboard:
    """In-memory dashboard to track worker earnings and generate summaries."""

    def __init__(self):
        self._lock = threading.Lock()
        self._earnings: Dict[str, List[EarningEntry]] = {}

    def add_earning(
        self,
        worker_id: str,
        worker_name: str,
        amount: float,
        description: str = "",
        timestamp: Optional[datetime] = None,
    ) -> EarningEntry:
        if amount <= 0:
            raise ValueError("amount must be a positive number")

        received_at = timestamp or datetime.utcnow()
        entry = EarningEntry(
            worker_id=worker_id,
            worker_name=worker_name,
            amount=float(amount),
            description=description,
            timestamp=received_at,
        )

        with self._lock:
            self._earnings.setdefault(worker_id, []).append(entry)

        return entry

    def get_earnings(self, worker_id: str) -> List[EarningEntry]:
        with self._lock:
            return list(self._earnings.get(worker_id, []))

    def get_total_earnings(self, worker_id: str) -> float:
        with self._lock:
            return sum(entry.amount for entry in self._earnings.get(worker_id, []))

    def get_all_worker_totals(self) -> List[Tuple[str, str, float]]:
        with self._lock:
            return [
                (worker_id, entries[0].worker_name if entries else "", sum(e.amount for e in entries))
                for worker_id, entries in self._earnings.items()
            ]

    def get_top_earners(self, limit: int = 5) -> List[Tuple[str, str, float]]:
        totals = self.get_all_worker_totals()
        return sorted(totals, key=lambda t: t[2], reverse=True)[:limit]

    def get_monthly_totals(self, year: int, month: int) -> Dict[str, float]:
        with self._lock:
            result: Dict[str, float] = {}
            for worker_id, entries in self._earnings.items():
                total = sum(
                    e.amount
                    for e in entries
                    if e.timestamp.year == year and e.timestamp.month == month
                )
                if total:
                    result[worker_id] = total
            return result

    def clear(self):
        with self._lock:
            self._earnings.clear()
