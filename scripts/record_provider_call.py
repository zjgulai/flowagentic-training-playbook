#!/usr/bin/env python3
"""Settle or safely release a pre-call provider budget reservation."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

from provider_budget import BudgetError, money, release, settle


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_LEDGER = ROOT / "data" / "experiments" / "provider-budget.yml"


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--ledger", type=Path, default=DEFAULT_LEDGER)
    parser.add_argument("--action", choices=("settle", "release"), default="settle")
    parser.add_argument("--experiment-id", required=True)
    parser.add_argument("--provider", choices=("DeepSeek", "Kimi"))
    parser.add_argument("--model")
    parser.add_argument("--input-tokens", type=int)
    parser.add_argument("--output-tokens", type=int)
    parser.add_argument("--latency-ms", type=int)
    parser.add_argument("--actual-cost", type=money)
    parser.add_argument("--status", choices=("success", "failed"))
    parser.add_argument("--synthetic-data", action="store_true")
    parser.add_argument("--release-reason")
    parser.add_argument("--network-call-not-started", action="store_true")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    try:
        if args.action == "release":
            reservation = release(
                args.ledger,
                experiment_id=args.experiment_id,
                reason=args.release_reason or "",
                network_call_not_started=args.network_call_not_started,
            )
            print(
                f"released {reservation['experiment_id']}; "
                f"reserved CNY {reservation['reserved_cost']} returned to availability"
            )
            return 0

        required = {
            "provider": args.provider,
            "model": args.model,
            "input-tokens": args.input_tokens,
            "output-tokens": args.output_tokens,
            "latency-ms": args.latency_ms,
            "status": args.status,
        }
        missing = [name for name, value in required.items() if value is None]
        if args.actual_cost is None:
            missing.append("actual-cost")
        if missing:
            raise BudgetError(f"settlement is missing required fields: {', '.join(missing)}")
        receipt = settle(
            args.ledger,
            experiment_id=args.experiment_id,
            provider=args.provider,
            model=args.model,
            input_tokens=args.input_tokens,
            output_tokens=args.output_tokens,
            latency_ms=args.latency_ms,
            actual_cost=args.actual_cost,
            call_status=args.status,
            synthetic_data=args.synthetic_data,
        )
        print(
            f"settled {receipt['experiment_id']}; actual CNY {receipt['actual_cost']}; "
            f"reserved maximum CNY {receipt['reserved_cost']}"
        )
        return 0
    except BudgetError as exc:
        print(f"BLOCKED: {exc}", file=sys.stderr)
        return exc.exit_code


if __name__ == "__main__":
    raise SystemExit(main())
