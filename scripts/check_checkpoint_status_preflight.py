#!/usr/bin/env python3
"""Fast, read-only preflight for the selected reconstruction checkpoints.

This is intentionally not a proof of binary equivalence. It verifies that the
status manifest points to files that exist and that recorded candidate hashes
match the checked-in bytes. Run the deeper identity/differential tests separately.
"""
import argparse
import hashlib
import json
from pathlib import Path


def check(root: Path):
    status = json.loads((root / "repro/status.json").read_text())
    results = {}
    for program, entry in sorted(status.items()):
        if not isinstance(entry, dict) or "candidate_artifact" not in entry:
            continue
        name = entry["candidate_artifact"]
        path = root / name
        row = {"candidate": name, "exists": path.is_file()}
        expected = entry.get("candidate_sha256")
        if path.is_file() and expected:
            actual = hashlib.sha256(path.read_bytes()).hexdigest()
            row.update(expected_sha256=expected, actual_sha256=actual, hash_matches=actual == expected)
        elif expected:
            row["hash_matches"] = False
        row["passed"] = row["exists"] and (not expected or row["hash_matches"])
        results[program] = row
    return results


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=Path(__file__).resolve().parents[1])
    parser.add_argument("--json", action="store_true", help="Print machine-readable output")
    args = parser.parse_args()
    results = check(args.root)
    if args.json:
        print(json.dumps(results, indent=2, sort_keys=True))
    else:
        for name, row in results.items():
            state = "PASS" if row["passed"] else "FAIL"
            reason = "hash mismatch" if row.get("hash_matches") is False and row["exists"] else ("missing artifact" if not row["exists"] else "artifact present")
            print(f"{state} {name}: {reason} ({row['candidate']})")
    return 0 if results and all(row["passed"] for row in results.values()) else 1


if __name__ == "__main__":
    raise SystemExit(main())
