from __future__ import annotations

import threading
from dataclasses import dataclass, field
from datetime import datetime
from typing import Dict, List, Optional


@dataclass
class AIUsageEntry:
    id: str
    model: str
    prompt_tokens: int
    completion_tokens: int
    embedding_tokens: int
    request_units: float
    cost: float
    timestamp: datetime = field(default_factory=datetime.utcnow)


class AIPricingSystem:
    """In-memory AI usage pricing system with model-based cost estimates."""

    def __init__(self):
        self._lock = threading.Lock()
        self._usage: List[AIUsageEntry] = []
        self._models: Dict[str, Dict[str, float]] = {}

        # default pricing (cost per token in USD)
        self.register_model("gpt-4.1", prompt_price=0.0015, completion_price=0.002, embedding_price=0.0001)
        self.register_model("gpt-4o", prompt_price=0.0009, completion_price=0.0013, embedding_price=0.00008)
        self.register_model("gpt-3.5", prompt_price=0.0004, completion_price=0.0006, embedding_price=0.00004)

    def register_model(
        self,
        model: str,
        prompt_price: float,
        completion_price: float,
        embedding_price: float = 0.0,
    ) -> None:
        if prompt_price < 0 or completion_price < 0 or embedding_price < 0:
            raise ValueError("pricing rates must be non-negative")

        with self._lock:
            self._models[model] = {
                "prompt_price": float(prompt_price),
                "completion_price": float(completion_price),
                "embedding_price": float(embedding_price),
            }

    def estimate_cost(
        self,
        model: str,
        prompt_tokens: int = 0,
        completion_tokens: int = 0,
        embedding_tokens: int = 0,
        request_units: float = 0.0,
    ) -> float:
        if prompt_tokens < 0 or completion_tokens < 0 or embedding_tokens < 0 or request_units < 0:
            raise ValueError("token counts and request units must be non-negative")

        with self._lock:
            if model not in self._models:
                raise KeyError(f"Model '{model}' is not registered")
            rates = self._models[model]

        cost = (
            prompt_tokens * rates["prompt_price"]
            + completion_tokens * rates["completion_price"]
            + embedding_tokens * rates["embedding_price"]
            + request_units * 0.0005
        )
        return round(cost, 8)

    def add_usage(
        self,
        usage_id: str,
        model: str,
        prompt_tokens: int,
        completion_tokens: int,
        embedding_tokens: int = 0,
        request_units: float = 0.0,
        timestamp: Optional[datetime] = None,
    ) -> AIUsageEntry:
        cost = self.estimate_cost(model, prompt_tokens, completion_tokens, embedding_tokens, request_units)

        entry = AIUsageEntry(
            id=usage_id,
            model=model,
            prompt_tokens=prompt_tokens,
            completion_tokens=completion_tokens,
            embedding_tokens=embedding_tokens,
            request_units=request_units,
            cost=cost,
            timestamp=timestamp or datetime.utcnow(),
        )

        with self._lock:
            self._usage.append(entry)

        return entry

    def get_usage(self, model: Optional[str] = None) -> List[AIUsageEntry]:
        with self._lock:
            if model is None:
                return list(self._usage)
            return [u for u in self._usage if u.model == model]

    def get_total_cost(self, model: Optional[str] = None) -> float:
        with self._lock:
            entries = self._usage if model is None else [u for u in self._usage if u.model == model]
            return round(sum(u.cost for u in entries), 8)

    def get_cost_by_model(self) -> Dict[str, float]:
        with self._lock:
            totals: Dict[str, float] = {}
            for u in self._usage:
                totals[u.model] = totals.get(u.model, 0.0) + u.cost
            return {m: round(c, 8) for m, c in totals.items()}

    def clear(self) -> None:
        with self._lock:
            self._usage.clear()
