from __future__ import annotations
from datetime import datetime
from typing import List

def to_ym(dt: datetime) -> str:
    return dt.strftime("%Y-%m")

def get_relative_past_months(target_month: str, months_back: int = 4) -> List[str]:
    """Return a list of past months (YYYY-MM) from M-months_back to M-1."""
    base = datetime.strptime(target_month, "%Y-%m")
    months = []
    y, m = base.year, base.month
    for i in range(months_back, 0, -1):
        mm = m - i
        yy = y
        while mm <= 0:
            mm += 12
            yy -= 1
        months.append(f"{yy}-{mm:02d}")
    return months
