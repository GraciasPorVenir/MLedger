from dataclasses import dataclass, field
from datetime import datetime
from decimal import Decimal


@dataclass
class ViewTransaction:
    id: int = field()
    metadata_id: int = field()
    category_id: int = field()
    cents: int = field()
    category: str = field()
    frequency: int = field(default=0)
    reason: str | None = field(default=None)
    currency: str = field(default="USD")
    is_income: int = field(default=1)
    installments: int = field(default=1)
    created_at: str = field(
        default_factory=lambda: datetime.now().isoformat(sep=" ", timespec="seconds")
    )

    @property
    def amount(self) -> Decimal:
        return Decimal(self.cents) / Decimal(100)

    @property
    def b_is_income(self) -> bool:
        return bool(self.is_income)

    @property
    def d_created_at(self) -> datetime:
        return datetime.fromisoformat(self.created_at)
