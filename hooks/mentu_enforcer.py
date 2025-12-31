#!/usr/bin/env python3
# /// script
# requires-python = ">=3.9"
# dependencies = []
# ///
"""
Mentu Protocol Enforcer Hook (Plugin Version v1.0).

Verifies SPECIFIC commitments are submitted (in_review or closed) with evidence
before allowing agent to stop.

ACTIVATION (REQUIRED):
  Environment variable: MENTU_ENFORCER=true

WITHOUT MENTU_ENFORCER=true:
  This hook does nothing. All agents can stop freely.
  The ledger is just a work ledger - not everything needs to be a commitment.

WITH MENTU_ENFORCER=true:
  The hook checks for claimed commitments by this actor.
  If any commitments are still open/claimed, agent cannot stop.
  Commitments must be in_review or closed before stopping.

TYPICAL WORKFLOW:
  1. Start with: MENTU_ACTOR=agent:my-task MENTU_ENFORCER=true claude ...
  2. Agent creates and claims commitments
  3. Agent must submit those commitments before stopping

ENVIRONMENT VARIABLES:
  - MENTU_ENFORCER=true   Required to activate this hook
  - MENTU_ACTOR=agent:x   Set actor identity
"""

import json
import os
import subprocess
import sys
from pathlib import Path
from typing import List, Tuple, Any, Optional


def run_mentu(args: List[str]) -> Tuple[bool, str, Any]:
    """Run mentu command, return (success, output, parsed_json)."""
    try:
        result = subprocess.run(
            ["mentu"] + args + ["--json"],
            capture_output=True,
            text=True,
            timeout=30
        )
        if result.returncode != 0:
            return False, result.stderr, None
        try:
            data = json.loads(result.stdout)
            return True, result.stdout, data
        except json.JSONDecodeError:
            return True, result.stdout, None
    except FileNotFoundError:
        return False, "mentu not found in PATH", None
    except subprocess.TimeoutExpired:
        return False, "mentu command timed out", None


def check_workspace_exists() -> Tuple[bool, str]:
    """Verify .mentu/ workspace exists."""
    if not Path(".mentu").exists():
        return False, "No .mentu/ workspace. Run: mentu init"
    if not Path(".mentu/ledger.jsonl").exists():
        return False, "No ledger found. Run: mentu init"
    return True, "Mentu workspace exists"


def get_commitments_by_actor(actor: str) -> List[dict]:
    """Get all commitments owned/claimed by an actor."""
    ok, _, data = run_mentu(["list", "commitments"])
    if not ok or not data:
        return []
    if isinstance(data, list):
        return [c for c in data if c.get("owner") == actor]
    return []


def check_actor_commitments_submitted(actor: str) -> Tuple[bool, str]:
    """Verify all commitments by actor are submitted (in_review or closed)."""
    commitments = get_commitments_by_actor(actor)

    if not commitments:
        # No commitments = agent hasn't started, allow stop
        return True, f"No commitments by {actor}"

    # Only open/claimed are incomplete
    # in_review means agent has done its part
    incomplete = [c for c in commitments if c.get("state") in ("open", "claimed")]
    if incomplete:
        ids = ", ".join(c["id"] for c in incomplete[:3])
        more = f" (+{len(incomplete)-3} more)" if len(incomplete) > 3 else ""
        return False, f"{actor} has incomplete commitments: {ids}{more}. Submit with evidence."

    # Count in_review + closed as complete
    complete_count = len([c for c in commitments if c.get("state") in ("in_review", "closed")])
    return True, f"{actor}: {complete_count} commitment(s) submitted"


def main():
    """Main hook entry point."""
    # Read hook input from stdin
    try:
        input_data = json.load(sys.stdin)
    except json.JSONDecodeError:
        input_data = {}

    # FIRST: Check if MENTU_ENFORCER=true is set
    # Without this env var, the hook does nothing
    enforcer_enabled = os.environ.get("MENTU_ENFORCER", "").lower() == "true"
    if not enforcer_enabled:
        # Hook not activated - allow stop immediately
        print(json.dumps({}))
        sys.exit(0)

    # Check workspace exists
    ok, msg = check_workspace_exists()
    if not ok:
        # No workspace = allow stop
        print(json.dumps({}))
        sys.exit(0)

    # Get actor identity
    actor = os.environ.get("MENTU_ACTOR", "agent:claude-code")

    # Check if all actor's commitments are submitted
    complete, message = check_actor_commitments_submitted(actor)

    if complete:
        # Allow stop
        print(json.dumps({}))
        sys.exit(0)
    else:
        # Block stop, continue working
        print(json.dumps({
            "decision": "block",
            "reason": f"[Mentu Protocol] {message}\n\nComplete your commitments before stopping."
        }))
        sys.exit(0)


if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        # Fail-safe: on any error, allow stop
        sys.stderr.write(f"Mentu enforcer error: {e}\n")
        print(json.dumps({}))
        sys.exit(0)
