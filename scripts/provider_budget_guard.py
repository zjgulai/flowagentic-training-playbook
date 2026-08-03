#!/usr/bin/env python3
"""Atomically reserve budget before one training-provider network call."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

from provider_budget import BudgetError, money, reserve


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_LEDGER = ROOT / "data" / "experiments" / "provider-budget.yml"


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--ledger", type=Path, default=DEFAULT_LEDGER)
    parser.add_argument("--experiment-id")
    parser.add_argument("--estimated-cost", required=True, type=money)
    parser.add_argument("--provider", required=True, choices=("DeepSeek", "Kimi"))
    parser.add_argument("--model")
    parser.add_argument("--synthetic-data", action="store_true")
    args = parser.parse_args()
    try:
        reservation = reserve(
            args.ledger,
            experiment_id=args.experiment_id,
            provider=args.provider,
            model=args.model,
            maximum_cost=args.estimated_cost,
            synthetic_data=args.synthetic_data,
        )
    except BudgetError as exc:
        print(f"BLOCKED: {exc}", file=sys.stderr)
        return exc.exit_code
    print(
        f"RESERVED: {reservation['experiment_id']}; {reservation['provider']}; "
        f"maximum CNY {reservation['reserved_cost']}. "
        "This pending reservation is the unique authority for one network call."
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
